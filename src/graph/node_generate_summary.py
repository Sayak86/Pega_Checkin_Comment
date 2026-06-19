from graph.state import GenCommentState
from datetime import datetime
import logging
from pathlib import Path
from langchain_core.prompts import ChatPromptTemplate
from llm.llmclient import get_consolidation_client
from config import load_config

logger = logging.getLogger("uvicorn")


def node_generate_summary(state: GenCommentState) -> dict:
    """
    This node generates a final consolidated summary after all chunks are processed.
    It collects all the summaries from each chunk, passes them through a consolidation LLM,
    which merges, deduplicates, and polishes them into a single check-in comment.
    """
    start_time = datetime.now()
    logger.debug("[Consolidation] Starting final summary consolidation")

    summaries = state.get("summaries", [])
    ruleType = state.get("ruleType", "UnknownRuleType")

    # Step 1: Concatenate all chunk summaries
    chunk_summaries_text = ""
    for i, summary in enumerate(summaries):
        summary_text = summary.get("summaryText", "")
        chunk_summaries_text += f"Chunk {i+1}:\n{summary_text}\n\n"
        logger.debug(f"Chunk ID: {summary.get('chunkId')} Summary: {summary_text}")

    logger.debug(f"[Consolidation] Concatenated {len(summaries)} chunk summaries")

    try:
        # Step 2: Load consolidation prompt
        root_dir = Path(__file__).parent.parent
        config = load_config()
        prompts_dir = Path(config["prompts"]["prompts_path"])
        consolidation_prompt_file = root_dir / prompts_dir / "consolidation_prompt.md"

        if not consolidation_prompt_file.exists():
            raise FileNotFoundError(f"Consolidation prompt file {consolidation_prompt_file} does not exist.")

        with open(consolidation_prompt_file, "r", encoding="utf-8") as f:
            consolidation_prompt_content = f.read()

        prompt_template = ChatPromptTemplate.from_template(consolidation_prompt_content)

        # Step 3: Invoke consolidation LLM
        llm = get_consolidation_client()
        chain = prompt_template | llm

        result = chain.invoke({
            "ruleType": ruleType,
            "chunk_summaries": chunk_summaries_text,
        })

        # Step 4: Extract consolidated comment
        if hasattr(result, 'model_dump'):
            result = result.model_dump()

        final_summary = result.get("checkin_comment", "")

        end_time = datetime.now()
        logger.debug(f"[Consolidation] Done. Duration: {end_time - start_time}")
        logger.debug(f"[Consolidation] Final Summary:\n{final_summary}\n")

        return {"final_summary": final_summary}

    except Exception as e:
        logger.error(f"[Consolidation] Error during consolidation: {str(e)}")
        # Fallback to simple concatenation if consolidation fails
        fallback_summary = chunk_summaries_text
        logger.debug(f"[Consolidation] Falling back to concatenated summary")
        return {"final_summary": fallback_summary}
