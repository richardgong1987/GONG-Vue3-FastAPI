import request from '@/utils/request'

// 查询laptop管理列表
export function listLaptops(query) {
  return request({
    url: '/laptops/laptops/list',
    method: 'get',
    params: query
  })
}

// 查询laptop管理详细
export function getLaptops(id) {
  return request({
    url: '/laptops/laptops/' + id,
    method: 'get'
  })
}

// 新增laptop管理
export function addLaptops(data) {
  return request({
    url: '/laptops/laptops',
    method: 'post',
    data: data
  })
}

// 修改laptop管理
export function updateLaptops(data) {
  return request({
    url: '/laptops/laptops',
    method: 'put',
    data: data
  })
}

// 删除laptop管理
export function delLaptops(id) {
  return request({
    url: '/laptops/laptops/' + id,
    method: 'delete'
  })
}
