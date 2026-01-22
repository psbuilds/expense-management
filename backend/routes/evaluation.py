from fastapi import APIRouter
from evaluation.evaluation_runner import run_evaluation

router = APIRouter(
    prefix="/evaluation",
    tags=["Evaluation"]
)

@router.post("/run")
def run_full_evaluation(payload: dict):
    """
    Runs full 3-layer evaluation:
    - Automated metrics
    - LLM as judge
    - (Optional) Human review
    """

    ground_truth = payload.get("ground_truth")
    prediction = payload.get("prediction")
    human_review = payload.get("human_review")

    result = run_evaluation(
        ground_truth=ground_truth,
        prediction=prediction,
        human_review=human_review
    )

    return result
