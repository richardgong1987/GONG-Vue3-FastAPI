from typing import Any, Union

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import PageModel
from module_biz.it_assets.entity.do.laptops_do import BizLaptopManagement
from module_biz.it_assets.entity.vo.laptops_vo import LaptopsModel, LaptopsPageQueryModel
from utils.page_util import PageUtil


class LaptopsDao:
    """
    laptop管理模块数据库操作层
    """

    @classmethod
    async def get_laptops_detail_by_id(cls, db: AsyncSession, id: int) -> Union[BizLaptopManagement, None]:
        """
        根据id获取laptop管理详细信息

        :param db: orm对象
        :param id: id
        :return: laptop管理信息对象
        """
        laptops_info = (
            (
                await db.execute(
                    select(BizLaptopManagement)
                    .where(
                        BizLaptopManagement.id == id
                    )
                )
            )
            .scalars()
            .first()
        )

        return laptops_info

    @classmethod
    async def get_laptops_detail_by_info(cls, db: AsyncSession, laptops: LaptopsModel) -> Union[BizLaptopManagement, None]:
        """
        根据laptop管理参数获取laptop管理信息

        :param db: orm对象
        :param laptops: laptop管理参数对象
        :return: laptop管理信息对象
        """
        laptops_info = (
            (
                await db.execute(
                    select(BizLaptopManagement).where(
                    )
                )
            )
            .scalars()
            .first()
        )

        return laptops_info

    @classmethod
    async def get_laptops_list(
        cls, db: AsyncSession, query_object: LaptopsPageQueryModel, is_page: bool = False
    ) -> Union[PageModel, list[dict[str, Any]]]:
        """
        根据查询参数获取laptop管理列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: laptop管理列表信息对象
        """
        query = (
            select(BizLaptopManagement)
            .where(
                BizLaptopManagement.created_at == query_object.created_at if query_object.created_at else True,
                BizLaptopManagement.creator == query_object.creator if query_object.creator else True,
                BizLaptopManagement.updater == query_object.updater if query_object.updater else True,
                BizLaptopManagement.deleted_at == query_object.deleted_at if query_object.deleted_at else True,
                BizLaptopManagement.laptop_code == query_object.laptop_code if query_object.laptop_code else True,
                BizLaptopManagement.office_license == query_object.office_license if query_object.office_license else True,
                BizLaptopManagement.microsoft_account == query_object.microsoft_account if query_object.microsoft_account else True,
                BizLaptopManagement.product_id == query_object.product_id if query_object.product_id else True,
                BizLaptopManagement.sku_id == query_object.sku_id if query_object.sku_id else True,
                BizLaptopManagement.license_name.like(f'%{query_object.license_name}%') if query_object.license_name else True,
                BizLaptopManagement.license_description == query_object.license_description if query_object.license_description else True,
                BizLaptopManagement.beta_expiration == query_object.beta_expiration if query_object.beta_expiration else True,
                BizLaptopManagement.license_status == query_object.license_status if query_object.license_status else True,
                BizLaptopManagement.status == query_object.status if query_object.status else True,
            )
            .order_by(BizLaptopManagement.id)
            .distinct()
        )
        laptops_list: Union[PageModel, list[dict[str, Any]]] = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )

        return laptops_list

    @classmethod
    async def add_laptops_dao(cls, db: AsyncSession, laptops: LaptopsModel) -> BizLaptopManagement:
        """
        新增laptop管理数据库操作

        :param db: orm对象
        :param laptops: laptop管理对象
        :return:
        """
        db_laptops = BizLaptopManagement(**laptops.model_dump(exclude={}))
        db.add(db_laptops)
        await db.flush()

        return db_laptops

    @classmethod
    async def edit_laptops_dao(cls, db: AsyncSession, laptops: dict) -> None:
        """
        编辑laptop管理数据库操作

        :param db: orm对象
        :param laptops: 需要更新的laptop管理字典
        :return:
        """
        await db.execute(update(BizLaptopManagement), [laptops])

    @classmethod
    async def delete_laptops_dao(cls, db: AsyncSession, laptops: LaptopsModel) -> None:
        """
        删除laptop管理数据库操作

        :param db: orm对象
        :param laptops: laptop管理对象
        :return:
        """
        await db.execute(delete(BizLaptopManagement).where(BizLaptopManagement.id.in_([laptops.id])))

