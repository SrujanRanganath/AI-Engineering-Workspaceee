from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from auth.dependencies import get_current_user
from models.user import User
from utils.file_security import safe_path

from tools.document_generator.schemas import DocumentRequest, DocumentResponse
from tools.document_generator.service import generate_document

router = APIRouter(
    prefix="/document-generator",
    tags=["Document Generator"],
)


@router.post("/generate", response_model=DocumentResponse)
def generate(
    request: DocumentRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        result = generate_document(
            document_type=request.document_type,
            template=request.template,
            title=request.title,
            name=request.name,
            company=request.company,
            content=request.content,
        )
        return DocumentResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate document.")


@router.get("/download/{filename}")
def download_document(
    filename: str,
    current_user: User = Depends(get_current_user),
):
    filepath = safe_path("generated_docs", filename)

    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found.")

    return FileResponse(
        path=str(filepath),
        filename=filepath.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
