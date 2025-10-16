from fastapi import APIRouter, HTTPException
from app.services.azure_openai_client import send_to_azure_openai

router = APIRouter(prefix="/mcp", tags=["MCP"])

@router.get("/manifest")
def get_manifest():
    return {
        "name": "gitlab-ai-review-mcp",
        "version": "1.0.0",
        "description": "MCP-compatible AI code review server for GitLab",
        "tools": [
            {
                "name": "review_merge_request",
                "description": "Review GitLab merge request diff",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "diff": {"type": "string"},
                        "repo_name": {"type": "string"},
                        "author": {"type": "string"}
                    },
                    "required": ["diff"]
                }
            }
        ]
    }

@router.post("/tool-call")
def tool_call(req: dict):
    tool = req.get("tool")
    args = req.get("arguments", {})
    if tool != "review_merge_request":
        raise HTTPException(status_code=400, detail="Unknown tool")

    diff = args.get("diff")
    prompt = f"Review the following GitLab MR diff:\n\n{diff}"
    response = send_to_azure_openai([{"role": "user", "content": prompt}])
    return {"tool": tool, "output": {"review_summary": response["content"]}}
