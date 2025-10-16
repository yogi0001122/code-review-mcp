from fastapi import FastAPI
from app.routes import health, mcp, review
from app.utils.logger import get_logger

logger = get_logger()

app = FastAPI(title="MCP AI Review Server")

app.include_router(health.router)
app.include_router(review.router)
app.include_router(mcp.router)

@app.get("/")
def root():
    return {"message": "MCP AI Review Server is running"}
