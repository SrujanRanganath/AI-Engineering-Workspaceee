from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from auth.dependencies import get_current_user
from models.user import User
from utils.file_security import safe_path

from tools.data_cleaner.schemas import DataCleanerResponse
from tools.data_cleaner.service import clean_data

router = APIRouter(
    prefix="/data-cleaner",
    tags=["Data Cleaner"],
)


@router.post("/clean", response_model=DataCleanerResponse)
def clean_uploaded_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file selected.")

    try:
        result = clean_data(file)
        return DataCleanerResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing the file.",
        )


@router.get("/download/{filename}")
def download_cleaned_file(
    filename: str,
    current_user: User = Depends(get_current_user),
):
    filepath = safe_path("cleaned_files", filename)

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Cleaned file not found.")

    return FileResponse(
        path=str(filepath),
        filename=filepath.name,
    )
