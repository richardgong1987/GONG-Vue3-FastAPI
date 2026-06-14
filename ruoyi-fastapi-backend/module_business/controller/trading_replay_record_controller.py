from fastapi import APIRouter
from starlette.responses import Response

from common.router import APIRouterPro
from utils.response_util import ResponseUtil

trading_replay_record_controller = APIRouterPro(prefix='/system/trading_replay_record')


@trading_replay_record_controller.get('/list')
async def create_trading_replay_record_route() -> Response:
    return ResponseUtil.success(msg='gong hanjin', data='my data')
