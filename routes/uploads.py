import os.path

from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import FileResponse

from data.config import Storage
from schemas.uploads import UploadOut
from utils.helpers import random_string, handle_image_upload

router = APIRouter(tags=["Uploads"])


@router.post("/upload", response_model=UploadOut)
async def create_upload(file: UploadFile = File()):
    data = await handle_image_upload(file)

    return UploadOut(upload=data)


@router.get("/uploads/{uid}")
async def get_upload(uid: str) -> FileResponse:
    file_: str = Storage.uploads + "/" + uid

    if os.path.exists(Storage.uploads + "/" + uid):
        return FileResponse(
            file_, status_code=200
        )
    else:
        raise HTTPException(status_code=404, detail="Not found")
