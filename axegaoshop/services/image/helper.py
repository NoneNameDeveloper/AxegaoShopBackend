import os

import aiofiles
from fastapi import UploadFile, HTTPException

from axegaoshop.settings import settings
from axegaoshop.services.utils import random_string


async def handle_image_upload(file: UploadFile) -> str:
    _, ext = os.path.splitext(file.filename)

    img_dir: str = settings.storage_folder_images

    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    content: bytes = await file.read()

    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")

    file_name = random_string(16) + ext

    async with aiofiles.open(os.path.join(img_dir, file_name), mode='wb') as f:
        await f.write(content)

    return file_name
