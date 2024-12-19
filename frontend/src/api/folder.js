import request from './request'

const acquireBlogsApi = () => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/all',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const acquireZonesApi = () => {
    return request.get({
        url: '/zone/all',
    })
}

const acquireObjectsApi = () => {
    return request.get({
        url: '/zone/object/all',
    })
}

export default {
    acquireBlogsApi,
    acquireCtgAllApi,
    acquireZonesApi,
    acquireObjectsApi,
}