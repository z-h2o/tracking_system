from typing import Any, Optional
from app.schemas.response_schema import ResponseModel

def success_response(data: Any) -> ResponseModel:
    """
    生成成功响应
    
    Args:
        data: 成功时返回的数据
        
    Returns:
        ResponseModel: 格式化的成功响应对象
    """
    return ResponseModel(
        code=0,
        message="success",
        data=data
    )

def error_response(message: str) -> ResponseModel:
    """
    生成失败响应
    
    Args:
        message: 错误原因说明
        
    Returns:
        ResponseModel: 格式化的失败响应对象
    """
    return ResponseModel(
        code=-1,
        message=message,
        data=None
    )
