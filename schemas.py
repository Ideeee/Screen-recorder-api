from fastapi import UploadFile
from pydantic import BaseModel

class VideoData(BaseModel):
    id : str
    blob : str
    # blob_num : int
    is_final : bool = False