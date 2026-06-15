from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_business.entity.do.record_do import TrdTradeRecord
from module_business.entity.vo.record_vo import RecordModel, RecordPageQueryModel
from utils.page_util import PageUtil


class RecordDao:
    """
    交易研究记录模块数据库操作层
    """

    @classmethod
    async def get_record_detail_by_id(cls, db: AsyncSession, id: int) -> TrdTradeRecord | None:
        """
        根据主键ID获取交易研究记录详细信息

        :param db: orm对象
        :param id: 主键ID
        :return: 交易研究记录信息对象
        """
        record_info = (await db.execute(select(TrdTradeRecord).where(TrdTradeRecord.id == id))).scalars().first()

        return record_info

    @classmethod
    async def get_record_detail_by_info(cls, db: AsyncSession, record: RecordModel) -> TrdTradeRecord | None:
        """
        根据交易研究记录参数获取交易研究记录信息

        :param db: orm对象
        :param record: 交易研究记录参数对象
        :return: 交易研究记录信息对象
        """
        record_info = (await db.execute(select(TrdTradeRecord).where())).scalars().first()

        return record_info

    @classmethod
    async def get_record_list(
        cls, db: AsyncSession, query_object: RecordPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        根据查询参数获取交易研究记录列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 交易研究记录列表信息对象
        """
        query = (
            select(TrdTradeRecord)
            .where(
                TrdTradeRecord.id == query_object.id if query_object.id else True,
                TrdTradeRecord.key_point == query_object.key_point if query_object.key_point else True,
                TrdTradeRecord.direction == query_object.direction if query_object.direction else True,
                TrdTradeRecord.signal == query_object.signal if query_object.signal else True,
                TrdTradeRecord.close_entry_result == query_object.close_entry_result
                if query_object.close_entry_result
                else True,
                TrdTradeRecord.retrace_25_result == query_object.retrace_25_result
                if query_object.retrace_25_result
                else True,
                TrdTradeRecord.retrace_382_result == query_object.retrace_382_result
                if query_object.retrace_382_result
                else True,
                TrdTradeRecord.retrace_50_result == query_object.retrace_50_result
                if query_object.retrace_50_result
                else True,
                TrdTradeRecord.move_to_breakeven_at_r == query_object.move_to_breakeven_at_r
                if query_object.move_to_breakeven_at_r
                else True,
                TrdTradeRecord.remark.like(f'%{query_object.remark}%') if query_object.remark else True,
                TrdTradeRecord.extra.like(f'%{query_object.extra}%') if query_object.extra else True,
            )
            .order_by(TrdTradeRecord.id)
            .distinct()
        )
        record_list: PageModel | list[dict[str, Any]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return record_list

    @classmethod
    async def add_record_dao(cls, db: AsyncSession, record: RecordModel) -> TrdTradeRecord:
        """
        新增交易研究记录数据库操作

        :param db: orm对象
        :param record: 交易研究记录对象
        :return:
        """
        db_record = TrdTradeRecord(**record.model_dump(exclude={}))
        db.add(db_record)
        await db.flush()

        return db_record

    @classmethod
    async def edit_record_dao(cls, db: AsyncSession, record: dict) -> None:
        """
        编辑交易研究记录数据库操作

        :param db: orm对象
        :param record: 需要更新的交易研究记录字典
        :return:
        """
        await db.execute(update(TrdTradeRecord), [record])

    @classmethod
    async def delete_record_dao(cls, db: AsyncSession, record: RecordModel) -> None:
        """
        删除交易研究记录数据库操作

        :param db: orm对象
        :param record: 交易研究记录对象
        :return:
        """
        await db.execute(delete(TrdTradeRecord).where(TrdTradeRecord.id.in_([record.id])))
