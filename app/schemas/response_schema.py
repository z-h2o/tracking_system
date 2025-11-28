from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

# 定义一个泛型类型变量，用于表示data字段的类型
T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    """
    统一的API响应模型
    
    成功响应格式：
    {
        "code": 0,
        "message": "success",
        "data": xxx
    }
    
    失败响应格式：
    {
        "code": -1,
        "message": "错误原因",
        "data": null
    }
    """
    # 状态码：0表示成功，-1表示失败
    code: int = Field(..., description="状态码，0表示成功，非0表示失败")
    # 响应消息：成功时为"success"，失败时为错误原因
    message: str = Field(..., description="响应消息")
    # 响应数据：成功时为具体数据，失败时为null
    data: Optional[T] = Field(None, description="响应数据")

    class Config:
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {}
            }
        }
