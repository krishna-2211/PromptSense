from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.improve import router as improve_router
from app.api.routes.upload import router as upload_router

load_dotenv()

app = FastAPI(
    title="PromptSense API",
    description="Backend for PromptSense - context-aware prompt improver",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api")
app.include_router(improve_router, prefix="/api")
app.include_router(upload_router, prefix="/api")


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "PromptSense backend is running"}