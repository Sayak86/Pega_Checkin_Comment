from pathlib import Path
from config import load_config
from langchain_core.prompts import ChatPromptTemplate
from functools import partial

def load_prompt(ruleType:str)->ChatPromptTemplate:
    config = load_config()
    prompts_dir = Path(config["prompts"]['prompts_path'])
    generic_prompt_file = prompts_dir / config["prompts"]['generic']
    specific_prompt_file = prompts_dir / f"{ruleType}_prompt.md"
    # Read generic prompt (not used currently, but can be extended)
    if not generic_prompt_file.exists():
        raise FileNotFoundError(f"Generic prompt file {generic_prompt_file} does not exist.")
    with open(generic_prompt_file, "r", encoding="utf-8") as f:
        generic_prompt_content = f.read()

    # Load rule-specific context
    if not specific_prompt_file.exists():
        raise FileNotFoundError(f"Prompt file {specific_prompt_file} does not exist.")

    with open(specific_prompt_file, "r", encoding="utf-8") as f:
        specific_prompt_content = f.read()

    template =  ChatPromptTemplate.from_template(generic_prompt_content)
    return template.partial(ruleType = ruleType,rule_spcific_prompt = specific_prompt_content)

if __name__ == "__main__":
    print("Prompt loading module loaded.")
    prompt = load_prompt("activity")
    print("Loaded prompt:", prompt)