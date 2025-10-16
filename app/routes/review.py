from fastapi import APIRouter, HTTPException
from app.services.azure_openai_client import send_to_azure_openai

router = APIRouter(prefix="/v1", tags=["Review"])

@router.post("/review")
def review_code(diff: str):
    try:
        prompt = f"Review the following code diff for quality, security, and compliance issues:\n\n{diff}"
        response = send_to_azure_openai([{"role": "user", "content": prompt}])
        return {"review_summary": response["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
