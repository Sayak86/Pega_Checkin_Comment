# We create a Fast API endpoint that receives a JSON payload with rule comparison results and the rule type.
# It will return a LLM processed comment based on the rule comparison.
from fastapi import FastAPI, HTTPException,APIRouter
from pydantic import BaseModel
from typing import Dict, Any, Optional
from graph.workflow import wokflow_process
import logging

logger = logging.getLogger("uvicorn")

logger.debug("GetCheckInComment module loaded.")

router = APIRouter()
class CheckInCommentRequest(BaseModel):
    RuleDiff: Dict[str, Any]
    RuleType: str

class CheckInCommentResponse(BaseModel):
    comment: Optional[str] = None
    error: Optional[str] = None

@router.post("/get_checkin_comment", response_model=CheckInCommentResponse)
def generate_checkin_comment(request: CheckInCommentRequest):
    logger.debug("Received request for generating check-in comment.")
    """
    Generate a check-in comment based on the compared results JSON and rule type.
    """
    try:
        # Here we would integrate with the LLM to generate the comment.
        # For demonstration, we will return a placeholder comment.
        comment = f"Generated check-in comment for rule type {request.RuleType}."
        logger.debug(comment)

        # validate request data
        comparedResultsJson = request.RuleDiff
        ruleType = request.RuleType

        if not comparedResultsJson:
            raise ValueError("comparedResultsJson cannot be empty")
        if not ruleType:
            raise ValueError("ruleType cannot be empty")
        
        # If ruleType is in the enum of known types, proceed
        set_of_rule_types = {"Activity", "Model"}
        if ruleType not in set_of_rule_types:
            raise ValueError(f"ruleType {ruleType} is not recognized.")
        
        # Call the workflow process
        result = wokflow_process(comparedResultsJson, ruleType)

        return CheckInCommentResponse(comment=result, error=None)
    except Exception as e:
        return CheckInCommentResponse(comment=None, error=str(e))