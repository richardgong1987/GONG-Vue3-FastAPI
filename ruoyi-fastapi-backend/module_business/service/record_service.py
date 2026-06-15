from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_business.dao.record_dao import RecordDao
from module_business.entity.vo.record_vo import DeleteRecordModel, RecordModel, RecordPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class RecordService:
    """
    交易研究记录模块服务层
    """

    @classmethod
    async def get_record_list_services(
        cls, query_db: AsyncSession, query_object: RecordPageQueryModel, is_page: bool = False
    ) -> PageModel | list[dict[str, Any]]:
        """
        获取交易研究记录列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 交易研究记录列表信息对象
        """
        record_list_result = await RecordDao.get_record_list(query_db, query_object, is_page)

        return record_list_result


    @classmethod
    async def add_record_services(cls, query_db: AsyncSession, page_object: RecordModel) -> CrudResponseModel:
        """
        新增交易研究记录信息service

        :param query_db: orm对象
        :param page_object: 新增交易研究记录对象
        :return: 新增交易研究记录校验结果
        """
        try:
            await RecordDao.add_record_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_record_services(cls, query_db: AsyncSession, page_object: RecordModel) -> CrudResponseModel:
        """
        编辑交易研究记录信息service

        :param query_db: orm对象
        :param page_object: 编辑交易研究记录对象
        :return: 编辑交易研究记录校验结果
        """
        edit_record = page_object.model_dump(exclude_unset=True, exclude={})
        record_info = await cls.record_detail_services(query_db, page_object.id)
        if record_info.id:
            try:
                await RecordDao.edit_record_dao(query_db, edit_record)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='交易研究记录不存在')

    @classmethod
    async def delete_record_services(cls, query_db: AsyncSession, page_object: DeleteRecordModel) -> CrudResponseModel:
        """
        删除交易研究记录信息service

        :param query_db: orm对象
        :param page_object: 删除交易研究记录对象
        :return: 删除交易研究记录校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await RecordDao.delete_record_dao(query_db, RecordModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入主键ID为空')

    @classmethod
    async def record_detail_services(cls, query_db: AsyncSession, id: int) -> RecordModel:
        """
        获取交易研究记录详细信息service

        :param query_db: orm对象
        :param id: 主键ID
        :return: 主键ID对应的信息
        """
        record = await RecordDao.get_record_detail_by_id(query_db, id=id)
        result = RecordModel(**CamelCaseUtil.transform_result(record)) if record else RecordModel()

        return result

    @staticmethod
    async def export_record_list_services(record_list: list) -> bytes:
        """
        导出交易研究记录信息service

        :param record_list: 交易研究记录信息列表
        :return: 交易研究记录信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': '主键ID',
            'id': '主键ID',
            'keyPoint': '关键位，例如 PDH / PDL / PWH',
            'direction': '多空：B=Buy，S=Sell',
            'signal': '信号：顶分型 / pinbar / 吞没',
            'closeEntryResult': '收盘入场',
            'retrace25Result': '回撤25入场',
            'retrace382Result': '回撤38.2入场',
            'retrace50Result': '回撤50入场',
            'moveToBreakevenAtR': 'R后推保本：1.5',
            'remark': '备注',
            'extra': '扩展JSON字段',
            'createdAt': '创建时间',
        }
        binary_data = ExcelUtil.export_list2excel(record_list, mapping_dict)

        return binary_data
