import request from './request'

const createZoneApi = data => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/create',
        headers: {
            'Content-Type':'multipart/form-data',
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const acquireZonesApi = () => {
    return request.get({
        url: '/zone/all',
    })
}


const acquireZoneDetailApi = zone_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/detail/' + zone_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const followZoneApi = zone_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/follow/' + zone_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const updateZoneApi = (data, zone_id) => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/modify/' + zone_id,
        headers: {
            'Content-Type':'multipart/form-data',
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const createObjectApi = (data, zone_id) => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/object/create/' + zone_id,
        headers: {
            'Content-Type':'multipart/form-data',
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const acquireObjectDetailApi = object_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/object/detail/' + object_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const starObjectApi = (data, object_id) => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/object/star/' + object_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const updateObjectApi = (data, object_id) => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/object/modify/' + object_id,
        headers: {
            'Content-Type':'multipart/form-data',
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const pubCmtApi = data => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/comment/pub',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const pubCmtCmtApi = data => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/zone/cmtcomment/pub',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}

const likeCmtApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/like_cmt/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const likeCmtCmtApi = cmt_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/like_cmt_cmt/' + cmt_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const dislikeCmtApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/dislike_cmt/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const dislikeCmtCmtApi = cmt_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/zone/dislike_cmt_cmt/' + cmt_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const deleteZoneApi = zone_id => {
    return request.get({
        url: '/zone/delete_zone/' + zone_id,
    })
}

const deleteObjApi = obj_id => {
    return request.get({
        url: '/zone/delete_obj/' + obj_id,
    })
}

const deleteCmtApi = cmt_id => {
    return request.get({
        url: '/zone/delete_cmt/' + cmt_id,
    })
}

const deleteCmtCmtApi = cmt_cmt_id => {
    return request.get({
        url: '/zone/delete_cmt_cmt/' + cmt_cmt_id,
    })
}


export default {
    createZoneApi,
    acquireZonesApi,
    acquireZoneDetailApi,
    followZoneApi,
    updateZoneApi,
    createObjectApi,
    acquireObjectDetailApi,
    starObjectApi,
    updateObjectApi,
    pubCmtApi,
    pubCmtCmtApi,
    likeCmtApi,
    likeCmtCmtApi,
    dislikeCmtApi,
    dislikeCmtCmtApi,
    deleteZoneApi,
    deleteObjApi,
    deleteCmtApi,
    deleteCmtCmtApi
}