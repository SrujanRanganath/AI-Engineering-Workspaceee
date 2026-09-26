from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from auth.dependencies import get_current_user
from models.user import User
from utils.file_security import safe_filename

from tools.website_builder.schemas import (
    GenerateWebsiteRequest,
    GenerateWebsiteResponse,
    SaveWebsiteRequest,
    SaveWebsiteResponse,
)
from tools.website_builder.service import (
    generate_website,
    save_generated_website,
    download_generated_website,
)

router = APIRouter(
    prefix="/website",
    tags=["Website Builder"],
)


@router.post("/generate", response_model=GenerateWebsiteResponse)
def generate(
    request: GenerateWebsiteRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        result = generate_website(
            request.prompt,
            request.framework,
            request.template,
        )
        return GenerateWebsiteResponse(
            app=result["app"],
            css=result["css"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Website generation failed: {str(e)}",
        )


@router.post("/save", response_model=SaveWebsiteResponse)
def save(
    request: SaveWebsiteRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        project_name = safe_filename(request.project_name)
        result = save_generated_website(
            project_name,
            request.framework,
            request.app,
            request.css,
        )
        return SaveWebsiteResponse(
            message=result["message"],
            folder=result["folder"],
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Saving website failed: {str(e)}",
        )


@router.get("/download/{project_name}")
def download(
    project_name: str,
    current_user: User = Depends(get_current_user),
):
    try:
        safe_project_name = safe_filename(project_name)
        zip_file = download_generated_website(safe_project_name)

        return FileResponse(
            path=zip_file,
            filename=f"{safe_project_name}.zip",
            media_type="application/zip",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Download failed: {str(e)}",
        )
