from fastapi import APIRouter
from core.patient_eval import evaluate_patient

router = APIRouter()

@router.post("/patient")
def patient_endpoint(payload):
    return evaluate_patient(payload)
