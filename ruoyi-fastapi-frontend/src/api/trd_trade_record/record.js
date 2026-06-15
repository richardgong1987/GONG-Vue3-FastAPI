import request from '@/utils/request'

// 查询交易研究记录列表
export function listRecord(query) {
    return request({
        url: '/trd_trade_record/record/list',
        method: 'get',
        params: query
    })
}

// 查询交易研究记录详细
export function getRecord(id) {
    return request({
        url: '/trd_trade_record/record/' + id,
        method: 'get'
    })
}

// 新增交易研究记录
export function addRecord(data) {
    return request({
        url: '/trd_trade_record/record',
        method: 'post',
        data: data
    })
}

// 修改交易研究记录
export function updateRecord(data) {
    return request({
        url: '/trd_trade_record/record',
        method: 'put',
        data: data
    })
}

// 删除交易研究记录
export function delRecord(id) {
    return request({
        url: '/trd_trade_record/record/' + id,
        method: 'delete'
    })
}
