from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from auth.dependencies import get_current_user
from models.user import User
from utils.file_security import safe_filename, safe_path

from tools.code_tool.schemas import (
    GenerateCodeRequest,
    GenerateCodeResponse,
    SaveCodeRequest,
    SaveCodeResponse,
    RunCodeRequest,
    RunCodeResponse,
    ExplainCodeRequest,
    ExplainCodeResponse,
)
from tools.code_tool.service import (
    generate_code,
    save_generated_code,
    run_generated_code,
    explain_code,
)

router = APIRouter(
    prefix="/code",
    tags=["Code Tool"],
)


@router.post("/generate", response_model=GenerateCodeResponse)
def generate(
    request: GenerateCodeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        code = generate_code(
            request.prompt,
            request.language,
            request.template,
        )
        return GenerateCodeResponse(code=code)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code generation failed: {str(e)}",
        )


@router.post("/save", response_model=SaveCodeResponse)
def save(
    request: SaveCodeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        filename = safe_filename(request.filename)
        result = save_generated_code(filename, request.code)
        return SaveCodeResponse(
            message=result["message"],
            filename=result["filename"],
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/run", response_model=RunCodeResponse)
def run(
    request: RunCodeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        filename = safe_filename(request.filename)
        result = run_generated_code(filename)
        return RunCodeResponse(output=result["output"])
    except HTTPException:
        raise
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except TimeoutError:
        raise HTTPException(status_code=408, detail="Code execution timed out.")


@router.get("/download/{filename}")
def download_generated_code(
    filename: str,
    current_user: User = Depends(get_current_user),
):
    filepath = safe_path("generated", filename)

    if not filepath.exists():
        raise HTTPException(
            status_code=404,
            detail="Generated code file not found.",
        )

    return FileResponse(
        path=str(filepath),
        filename=filepath.name,
        media_type="text/plain",
    )


@router.post("/explain", response_model=ExplainCodeResponse)
def explain(
    request: ExplainCodeRequest,
    current_user: User = Depends(get_current_user),
):
    try:
        explanation = explain_code(request.code, request.language)
        return ExplainCodeResponse(explanation=explanation)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Code explanation failed: {str(e)}",
        )
