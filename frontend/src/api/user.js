import request from './request'

const loginApi = data => {
    return request.post({
        url: '/user/login',
        data
    })
}

const captchaApi = data => {
    return request.post({
        url: '/user/captcha',
        data
    })
}

const registerApi = data => {
    return request.post({
        url: '/user/register',
        data
    })
}

const recoverPasswordApi = data => {
    return request.post({
        url: '/user/forget',
        data
    })
}

const recoverCaptchaApi = data => {
    return request.post({
        url: '/user/recover_captcha',
        data
    })
}

const modifyInfoApi = data => {
    return request.post({
        url: '/user/modify_information',
        data
    })
}

const modifyPaswApi = data => {
    return request.post({
        url: '/user/modify_password',
        data
    })
}

const uploadAvatarApi = data => {
    const token = localStorage.getItem('jwt_token');
    return request.post({
        url: '/user/upload_avatar',
        headers: {
            'Content-Type':'multipart/form-data',
            'Authorization': `Bearer ${token}`,
        },
        data
    })
}

const fetchUserData = () => {
    const token = localStorage.getItem('jwt_token');
    return fetch('http://localhost:9090/user/center', {
        method: 'GET',
        headers: {
        'Authorization': `Bearer ${token}`,
        }
    })
    .then(response => response.json())
    .then(data => data.user)
    .catch(error => {
        console.error('Error:', error)
    });
}

const fetchUserDataById = id => {
    return fetch('http://localhost:9090/user/center/' + id, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => data.user)
    .catch(error => {
        console.error('Error:', error)
    });
}
  

export default {
    loginApi,
    captchaApi,
    registerApi,
    recoverPasswordApi,
    recoverCaptchaApi,
    modifyInfoApi,
    modifyPaswApi,
    fetchUserData,
    uploadAvatarApi,
    fetchUserDataById,
}