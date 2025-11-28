from fastapi import APIRouter, status
from typing import List
from app.schemas.app_schema import AppCreate, AppUpdate, AppResponse
from app.schemas.response_schema import ResponseModel
from app.services.app_service import AppService
from app.utils.response_utils import success_response, error_response

router = APIRouter(prefix="/api/v1/apps", tags=["应用管理"])

@router.post("", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_app(app_data: AppCreate):
    """创建应用"""
    try:
        app = await AppService.create_app(app_data)
        return success_response(AppResponse.model_validate(app).model_dump())
    except Exception as e:
        return error_response(f"Failed to create app: {str(e)}")

@router.get("", response_model=ResponseModel)
async def get_apps(page: int = 1, page_size: int = 20):
    """获取应用列表"""
    try:
        apps, total = await AppService.get_apps(page, page_size)
        return success_response({
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": [AppResponse.model_validate(app).model_dump() for app in apps]
        })
    except Exception as e:
        return error_response(f"Failed to get apps: {str(e)}")

@router.get("/{app_id}", response_model=ResponseModel)
async def get_app(app_id: int):
    """获取应用详情"""
    try:
        app = await AppService.get_app_by_id(app_id)
        if not app:
            return error_response("App not found")
        
        return success_response(AppResponse.model_validate(app).model_dump())
    except Exception as e:
        return error_response(f"Failed to get app: {str(e)}")

@router.put("/{app_id}", response_model=ResponseModel)
async def update_app(app_id: int, app_data: AppUpdate):
    """更新应用"""
    try:
        app = await AppService.update_app(app_id, app_data)
        if not app:
            return error_response("App not found")
        
        return success_response(AppResponse.model_validate(app).model_dump())
    except Exception as e:
        return error_response(f"Failed to update app: {str(e)}")

@router.delete("/{app_id}", response_model=ResponseModel)
async def delete_app(app_id: int):
    """删除应用"""
    try:
        success = await AppService.delete_app(app_id)
        if not success:
            return error_response("App 不存在")
        
        return success_response(None)
    except Exception as e:
        return error_response(f"Failed to delete app: {str(e)}")