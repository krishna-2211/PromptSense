from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.upload_response import UploadResponse

router = APIRouter(tags=["Upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    try:
        file_id = f"{uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / file_id

        content = await file.read()
        file_path.write_bytes(content)

        return UploadResponse(
            file_id=file_id,
            filename=file.filename,
            message="File uploaded successfully",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc