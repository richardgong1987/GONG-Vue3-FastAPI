from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel




class RecordModel(BaseModel):
    """
    交易研究记录表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    id: int | None = Field(default=None, description='主键ID')
    id: int | None = Field(default=None, description='主键ID')
    key_point: str | None = Field(default=None, description='关键位，例如 PDH / PDL / PWH')
    direction: str | None = Field(default=None, description='多空：B=Buy，S=Sell')
    signal: str | None = Field(default=None, description='信号：顶分型 / pinbar / 吞没')
    close_entry_result: str | None = Field(default=None, description='收盘入场')
    retrace_25_result: str | None = Field(default=None, description='回撤25入场')
    retrace_382_result: str | None = Field(default=None, description='回撤38.2入场')
    retrace_50_result: str | None = Field(default=None, description='回撤50入场')
    move_to_breakeven_at_r: Decimal | None = Field(default=None, description='R后推保本：1.5')
    remark: str | None = Field(default=None, description='备注')
    extra: dict | None = Field(default=None, description='扩展JSON字段')
    created_at: datetime | None = Field(default=None, description='创建时间')






class RecordQueryModel(RecordModel):
    """
    交易研究记录不分页查询模型
    """
    pass


class RecordPageQueryModel(RecordQueryModel):
    """
    交易研究记录分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteRecordModel(BaseModel):
    """
    删除交易研究记录模型
    """

    model_config = ConfigDict(alias_generator=to_camel)

    ids: str = Field(description='需要删除的主键ID')
