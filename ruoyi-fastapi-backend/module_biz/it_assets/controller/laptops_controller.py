from typing import Annotated

from fastapi import Form, Path, Query, Request, Response
from fastapi.responses import StreamingResponse
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from common.annotation.log_annotation import Log
from common.aspect.db_seesion import DBSessionDependency
from common.aspect.interface_auth import UserInterfaceAuthDependency
from common.aspect.pre_auth import CurrentUserDependency, PreAuthDependency
from common.enums import BusinessType
from common.router import APIRouterPro
from common.vo import DataResponseModel, PageResponseModel, ResponseBaseModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_biz.it_assets.service.laptops_service import LaptopsService
from module_biz.it_assets.entity.vo.laptops_vo import DeleteLaptopsModel, LaptopsModel, LaptopsPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil

laptops_controller = APIRouterPro(
    prefix='/laptops/laptops', order_num=50, tags=['laptop管理'], dependencies=[PreAuthDependency()]
)


@laptops_controller.get(
    '/list',
    summary='获取laptop管理分页列表接口',
    description='用于获取laptop管理分页列表',
    response_model=PageResponseModel[LaptopsModel],
    dependencies=[UserInterfaceAuthDependency('laptops:laptops:list')],
)
async def get_laptops_laptops_list(
        request: Request,
        laptops_page_query: Annotated[LaptopsPageQueryModel, Query()],
        query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取分页数据
    laptops_page_query_result = await LaptopsService.get_laptops_list_services(query_db, laptops_page_query,
                                                                               is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=laptops_page_query_result)


@laptops_controller.post(
    '',
    summary='新增laptop管理接口',
    description='用于新增laptop管理',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('laptops:laptops:add')],
)
@ValidateFields(validate_model='add_laptops')
@Log(title='laptop管理', business_type=BusinessType.INSERT)
async def add_laptops_laptops(
        request: Request,
        add_laptops: LaptopsModel,
        query_db: Annotated[AsyncSession, DBSessionDependency()],
        current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    add_laptops_result = await LaptopsService.add_laptops_services(query_db, add_laptops)
    logger.info(add_laptops_result.message)

    return ResponseUtil.success(msg=add_laptops_result.message)


@laptops_controller.put(
    '',
    summary='编辑laptop管理接口',
    description='用于编辑laptop管理',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('laptops:laptops:edit')],
)
@ValidateFields(validate_model='edit_laptops')
@Log(title='laptop管理', business_type=BusinessType.UPDATE)
async def edit_laptops_laptops(
        request: Request,
        edit_laptops: LaptopsModel,
        query_db: Annotated[AsyncSession, DBSessionDependency()],
        current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_laptops_result = await LaptopsService.edit_laptops_services(query_db, edit_laptops)
    logger.info(edit_laptops_result.message)

    return ResponseUtil.success(msg=edit_laptops_result.message)


@laptops_controller.delete(
    '/{ids}',
    summary='删除laptop管理接口',
    description='用于删除laptop管理',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('laptops:laptops:remove')],
)
@Log(title='laptop管理', business_type=BusinessType.DELETE)
async def delete_laptops_laptops(
        request: Request,
        ids: Annotated[str, Path(description='需要删除的id')],
        query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    delete_laptops = DeleteLaptopsModel(ids=ids)
    delete_laptops_result = await LaptopsService.delete_laptops_services(query_db, delete_laptops)
    logger.info(delete_laptops_result.message)

    return ResponseUtil.success(msg=delete_laptops_result.message)


@laptops_controller.get(
    '/{id}',
    summary='获取laptop管理详情接口',
    description='用于获取指定laptop管理的详细信息',
    response_model=DataResponseModel[LaptopsModel],
    dependencies=[UserInterfaceAuthDependency('laptops:laptops:query')]
)
async def query_detail_laptops_laptops(
        request: Request,
        id: Annotated[int, Path(description='id')],
        query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    laptops_detail_result = await LaptopsService.laptops_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=laptops_detail_result)


@laptops_controller.post(
    '/export',
    summary='导出laptop管理列表接口',
    description='用于导出当前符合查询条件的laptop管理列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回laptop管理列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('laptops:laptops:export')],
)
@Log(title='laptop管理', business_type=BusinessType.EXPORT)
async def export_laptops_laptops_list(
        request: Request,
        laptops_page_query: Annotated[LaptopsPageQueryModel, Form()],
        query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    # 获取全量数据
    laptops_query_result = await LaptopsService.get_laptops_list_services(query_db, laptops_page_query, is_page=False)
    laptops_export_result = await LaptopsService.export_laptops_list_services(laptops_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(laptops_export_result))
