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

const acquireCtgAllApi = () => {
    return request.get({
        url: '/blog/ctg_all',
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

const acquireCollectedBlogsApi = () => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/user/blog_collected',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const acquireFollowedZonesApi = () => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/user/zone_followed',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const acquireStaredObjectsApi = () => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/user/object_stared',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

export default {
    acquireBlogsApi,
    acquireCtgAllApi,
    acquireZonesApi,
    acquireObjectsApi,
    acquireCollectedBlogsApi,
    acquireFollowedZonesApi,
    acquireStaredObjectsApi,
}