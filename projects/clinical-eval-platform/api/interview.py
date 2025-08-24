from fastapi import APIRouter
from core.interview_eval import evaluate_interview

router = APIRouter()

@router.post("/interview")
def interview_endpoint(payload):
    return evaluate_interview(payload)
