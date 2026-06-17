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
from module_business.entity.vo.record_vo import DeleteRecordModel, RecordModel, RecordPageQueryModel
from module_business.service.record_service import RecordService
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.response_util import ResponseUtil

record_controller = APIRouterPro(prefix='/trd_trade_record/record', order_num=50, tags=['交易研究记录'])


@record_controller.get(
    '/list',
    summary='获取交易研究记录分页列表接口',
    description='用于获取交易研究记录分页列表',
    response_model=PageResponseModel[RecordModel],
    dependencies=[UserInterfaceAuthDependency('trd_trade_record:record:list')],
)
async def get_trd_trade_record_record_list(
    request: Request,
    record_page_query: Annotated[RecordPageQueryModel, Query()],
    query_db: Annotated[AsyncSession, DBSessionDependency(), PreAuthDependency()],
) -> Response:
    # 获取分页数据
    record_page_query_result = await RecordService.get_record_list_services(query_db, record_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=record_page_query_result)


@record_controller.post(
    '',
    summary='新增交易研究记录接口',
    description='用于新增交易研究记录',
    response_model=ResponseBaseModel,
)
@ValidateFields(validate_model='add_record')
async def add_trd_trade_record_record(
    request: Request,
    add_record: RecordModel,
    query_db: Annotated[AsyncSession, DBSessionDependency()],
) -> Response:
    add_record_result = await RecordService.add_record_services(query_db, add_record)
    logger.info(add_record_result.message)

    return ResponseUtil.success(msg=add_record_result.message)


@record_controller.put(
    '',
    summary='编辑交易研究记录接口',
    description='用于编辑交易研究记录',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('trd_trade_record:record:edit')],
)
@ValidateFields(validate_model='edit_record')
@Log(title='交易研究记录', business_type=BusinessType.UPDATE)
async def edit_trd_trade_record_record(
    request: Request,
    edit_record: RecordModel,
    query_db: Annotated[AsyncSession, DBSessionDependency(), PreAuthDependency()],
    current_user: Annotated[CurrentUserModel, CurrentUserDependency()],
) -> Response:
    edit_record_result = await RecordService.edit_record_services(query_db, edit_record)
    logger.info(edit_record_result.message)

    return ResponseUtil.success(msg=edit_record_result.message)


@record_controller.delete(
    '/{ids}',
    summary='删除交易研究记录接口',
    description='用于删除交易研究记录',
    response_model=ResponseBaseModel,
    dependencies=[UserInterfaceAuthDependency('trd_trade_record:record:remove')],
)
@Log(title='交易研究记录', business_type=BusinessType.DELETE)
async def delete_trd_trade_record_record(
    request: Request,
    ids: Annotated[str, Path(description='需要删除的主键ID')],
    query_db: Annotated[AsyncSession, DBSessionDependency(), PreAuthDependency()],
) -> Response:
    delete_record = DeleteRecordModel(ids=ids)
    delete_record_result = await RecordService.delete_record_services(query_db, delete_record)
    logger.info(delete_record_result.message)

    return ResponseUtil.success(msg=delete_record_result.message)


@record_controller.get(
    '/{id}',
    summary='获取交易研究记录详情接口',
    description='用于获取指定交易研究记录的详细信息',
    response_model=DataResponseModel[RecordModel],
    dependencies=[UserInterfaceAuthDependency('trd_trade_record:record:query')],
)
async def query_detail_trd_trade_record_record(
    request: Request,
    id: Annotated[int, Path(description='主键ID')],  # noqa: A002
    query_db: Annotated[AsyncSession, DBSessionDependency(), PreAuthDependency()],
) -> Response:
    record_detail_result = await RecordService.record_detail_services(query_db, id)
    logger.info(f'获取id为{id}的信息成功')

    return ResponseUtil.success(data=record_detail_result)


@record_controller.post(
    '/export',
    summary='导出交易研究记录列表接口',
    description='用于导出当前符合查询条件的交易研究记录列表数据',
    response_class=StreamingResponse,
    responses={
        200: {
            'description': '流式返回交易研究记录列表excel文件',
            'content': {
                'application/octet-stream': {},
            },
        }
    },
    dependencies=[UserInterfaceAuthDependency('trd_trade_record:record:export')],
)
@Log(title='交易研究记录', business_type=BusinessType.EXPORT)
async def export_trd_trade_record_record_list(
    request: Request,
    record_page_query: Annotated[RecordPageQueryModel, Form()],
    query_db: Annotated[AsyncSession, DBSessionDependency(), PreAuthDependency()],
) -> Response:
    # 获取全量数据
    record_query_result = await RecordService.get_record_list_services(query_db, record_page_query, is_page=False)
    record_export_result = await RecordService.export_record_list_services(record_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(record_export_result))
