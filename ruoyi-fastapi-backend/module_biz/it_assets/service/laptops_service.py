from typing import Any, Union

from sqlalchemy.ext.asyncio import AsyncSession

from common.constant import CommonConstant
from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_biz.it_assets.dao.laptops_dao import LaptopsDao
from module_biz.it_assets.entity.vo.laptops_vo import DeleteLaptopsModel, LaptopsModel, LaptopsPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class LaptopsService:
    """
    laptop管理模块服务层
    """

    @classmethod
    async def get_laptops_list_services(
        cls, query_db: AsyncSession, query_object: LaptopsPageQueryModel, is_page: bool = False
    ) -> Union[PageModel, list[dict[str, Any]]]:
        """
        获取laptop管理列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: laptop管理列表信息对象
        """
        laptops_list_result = await LaptopsDao.get_laptops_list(query_db, query_object, is_page)

        return laptops_list_result


    @classmethod
    async def add_laptops_services(cls, query_db: AsyncSession, page_object: LaptopsModel) -> CrudResponseModel:
        """
        新增laptop管理信息service

        :param query_db: orm对象
        :param page_object: 新增laptop管理对象
        :return: 新增laptop管理校验结果
        """
        try:
            await LaptopsDao.add_laptops_dao(query_db, page_object)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as e:
            await query_db.rollback()
            raise e

    @classmethod
    async def edit_laptops_services(cls, query_db: AsyncSession, page_object: LaptopsModel) -> CrudResponseModel:
        """
        编辑laptop管理信息service

        :param query_db: orm对象
        :param page_object: 编辑laptop管理对象
        :return: 编辑laptop管理校验结果
        """
        edit_laptops = page_object.model_dump(exclude_unset=True, exclude={})
        laptops_info = await cls.laptops_detail_services(query_db, page_object.id)
        if laptops_info.id:
            try:
                await LaptopsDao.edit_laptops_dao(query_db, edit_laptops)
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='laptop管理不存在')

    @classmethod
    async def delete_laptops_services(cls, query_db: AsyncSession, page_object: DeleteLaptopsModel) -> CrudResponseModel:
        """
        删除laptop管理信息service

        :param query_db: orm对象
        :param page_object: 删除laptop管理对象
        :return: 删除laptop管理校验结果
        """
        if page_object.ids:
            id_list = page_object.ids.split(',')
            try:
                for id in id_list:
                    await LaptopsDao.delete_laptops_dao(query_db, LaptopsModel(id=id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入id为空')

    @classmethod
    async def laptops_detail_services(cls, query_db: AsyncSession, id: int) -> LaptopsModel:
        """
        获取laptop管理详细信息service

        :param query_db: orm对象
        :param id: id
        :return: id对应的信息
        """
        laptops = await LaptopsDao.get_laptops_detail_by_id(query_db, id=id)
        result = LaptopsModel(**CamelCaseUtil.transform_result(laptops)) if laptops else LaptopsModel()

        return result

    @staticmethod
    async def export_laptops_list_services(laptops_list: list) -> bytes:
        """
        导出laptop管理信息service

        :param laptops_list: laptop管理信息列表
        :return: laptop管理信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'id': 'id',
            'id': 'id',
            'id': 'id',
            'createdAt': 'created_at',
            'createdBy': 'created_by',
            'creator': 'creator',
            'updatedAt': 'updated_at',
            'updatedBy': 'updated_by',
            'updater': 'updater',
            'deletedBy': 'deleted_by',
            'deletedAt': 'deleted_at',
            'laptopCode': '番号',
            'officeLicense': 'ライセンスキー',
            'microsoftAccount': 'Microsoft Account',
            'productId': 'PRODUCT_ID',
            'skuId': 'SKU_ID',
            'licenseName': 'LICENSE_NAME',
            'licenseDescription': 'LICENSE_DESCRIPTION',
            'betaExpiration': 'BETA_EXPIRATION',
            'licenseStatus': 'LICENSE_STATUS',
            'status': 'status',
            'remark': 'remark',
        }
        binary_data = ExcelUtil.export_list2excel(laptops_list, mapping_dict)

        return binary_data
