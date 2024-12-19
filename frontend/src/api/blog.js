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


const searchByCategoryApi = category_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/category/' + category_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const acquireBlogDetailApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/detail/' + blog_id,
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


const pubBlogApi = data => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/blog/pub',
        headers: {
            'Content-Type':'multipart/form-data',
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const updateBlogApi = (data, blog_id) => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/blog/modify/' + blog_id,
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
        url: '/blog/comment/pub',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const pubCmtCmtApi = data => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/blog/cmtcomment/pub',
        headers: {
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}


const collectBlogApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/collect/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const likeBlogApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/like/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const dislikeBlogApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/dislike/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}


const likeCmtApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/like_cmt/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const likeCmtCmtApi = cmt_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/like_cmt_cmt/' + cmt_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const dislikeCmtApi = blog_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/dislike_cmt/' + blog_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const dislikeCmtCmtApi = cmt_id => {
    const token = localStorage.getItem('jwt_token');
    return request.get({
        url: '/blog/dislike_cmt_cmt/' + cmt_id,
        headers: {
            'Authorization': `Bearer ${token}`,
        },
    })
}

const deleteBlogApi = blog_id => {
    return request.get({
        url: '/blog/delete/' + blog_id,
    })
}

const deleteCmtApi = cmt_id => {
    return request.get({
        url: '/blog/delete_cmt/' + cmt_id,
    })
}

const deleteCmtCmtApi = cmt_cmt_id => {
    return request.get({
        url: '/blog/delete_cmt_cmt/' + cmt_cmt_id,
    })
}

export default {
    acquireBlogsApi,
    searchByCategoryApi,
    acquireBlogDetailApi,
    acquireCtgAllApi,
    pubBlogApi,
    updateBlogApi,
    pubCmtApi,
    pubCmtCmtApi,
    collectBlogApi,
    likeBlogApi,
    dislikeBlogApi,
    likeCmtApi,
    likeCmtCmtApi,
    dislikeCmtApi,
    dislikeCmtCmtApi,
    deleteBlogApi,
    deleteCmtApi,
    deleteCmtCmtApi,
}