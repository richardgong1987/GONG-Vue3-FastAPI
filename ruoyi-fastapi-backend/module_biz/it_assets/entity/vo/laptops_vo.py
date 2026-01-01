from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class LaptopsModel(BaseModel):
    """
    laptop管理表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: Optional[int] = Field(default=None, description='id')
    created_at: Optional[datetime] = Field(default=None, description='created_at')
    created_by: Optional[int] = Field(default=None, description='created_by')
    creator: Optional[str] = Field(default=None, description='creator')
    updated_at: Optional[datetime] = Field(default=None, description='updated_at')
    updated_by: Optional[int] = Field(default=None, description='updated_by')
    updater: Optional[str] = Field(default=None, description='updater')
    deleted_by: Optional[int] = Field(default=None, description='deleted_by')
    deleted_at: Optional[datetime] = Field(default=None, description='deleted_at')
    laptop_code: Optional[str] = Field(default=None, description='番号')
    office_license: Optional[str] = Field(default=None, description='ライセンスキー')
    microsoft_account: Optional[str] = Field(default=None, description='Microsoft Account')
    product_id: Optional[str] = Field(default=None, description='PRODUCT_ID')
    sku_id: Optional[str] = Field(default=None, description='SKU_ID')
    license_name: Optional[str] = Field(default=None, description='LICENSE_NAME')
    license_description: Optional[str] = Field(default=None, description='LICENSE_DESCRIPTION')
    beta_expiration: Optional[str] = Field(default=None, description='BETA_EXPIRATION')
    license_status: Optional[str] = Field(default=None, description='LICENSE_STATUS')
    status: Optional[str] = Field(default=None, description='status')
    remark: Optional[str] = Field(default=None, description='remark')






class LaptopsQueryModel(LaptopsModel):
    """
    laptop管理不分页查询模型
    """
    pass


class LaptopsPageQueryModel(LaptopsQueryModel):
    """
    laptop管理分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteLaptopsModel(BaseModel):
    """
    删除laptop管理模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的id')
