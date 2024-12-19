import string, random, json, jwt, uuid
from django.views.decorators.http import require_POST, require_GET
from datetime import datetime, timedelta
from django.contrib.auth import login
from django.conf import settings
from django.http.response import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import CaptchaModel, UserDetail
import os


@require_POST
def mylogin(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password):
        login(request, user)
        # 生成token
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=24),  # 设置过期时间为24小时
            'iat': datetime.utcnow()                         # 签发时间
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({'code': 200, 'token': token.decode('utf-8'), 'avatar': user.userdetail.avatar, 'username': user.username})
    elif not user:
        return JsonResponse({'code': 400, 'message': '不存在此邮箱！'})
    elif not user.check_password(password):
        return JsonResponse({'code': 400, 'message': '密码错误！'})


@require_POST
def admin_login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    user = User.objects.filter(email=email).first()
    if user and user.check_password(password) and user.is_superuser:
        login(request, user)
        # 生成token
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(hours=24),  # 设置过期时间为24小时
            'iat': datetime.utcnow()                         # 签发时间
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return JsonResponse({'code': 200, 'token': token.decode('utf-8')})
    elif not user:
        return JsonResponse({'code': 400, 'message': '不存在此邮箱！'})
    elif not user.check_password(password):
        return JsonResponse({'code': 400, 'message': '密码错误！'})


@require_POST
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    if User.objects.filter(email=email).first():
        return JsonResponse({'code': 400, 'message': '此邮箱已被注册！'})
    
    username = data.get('username')
    if User.objects.filter(username=username).first():
        return JsonResponse({'code': 400, 'message': '用户名已被使用！'})
    
    password = data.get('password')
    if len(password) < 6:
        return JsonResponse({'code': 400, 'message': '密码长度需大于六位！'})
    
    user = User.objects.create_user(email=email, username=username, password=password)
    UserDetail.objects.create(user=user)
    return JsonResponse({'code': 200, 'message': '用户注册成功！'})


@require_POST
def send_email_captcha(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'code': 400, 'message': '邮箱格式错误！'})
    
    captcha = ''.join(random.sample(string.digits, 4))
    user = User.objects.filter(email=email).first()
    if not user:
        CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
        send_mail('注册验证', message=f'您的注册验证码是：{captcha}', recipient_list=[email], from_email=None)
        return JsonResponse({'code': 200, 'message': '验证码发送成功！'})
    else:
        return JsonResponse({'code': 400, 'message': '此邮箱已被注册！'})


@require_POST
def forget(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    if not email:
        return JsonResponse({'code': 400, 'message': '此邮箱未被注册！'})
    
    captcha = data.get('captcha')
    captchaModel = CaptchaModel.objects.filter(captcha=captcha, email=email).first()
    if captchaModel:
        user = User.objects.filter(email=email).first()
        password = data.get('password')
        user.set_password(password)
        user.save()
        return JsonResponse({'code': 200, 'message': '重置密码成功！'})
    else:
        return JsonResponse({'code': 400, 'message': '验证码错误！'})


@require_POST
def send_recover_email_captcha(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'code': 400, 'message': '邮箱格式错误！'})
    
    captcha = ''.join(random.sample(string.digits, 4))
    user = User.objects.filter(email=email).first()
    if user:
        CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
        send_mail('注册验证', message=f'您的注册验证码是：{captcha}', recipient_list=[email], from_email=None)
        return JsonResponse({'code': 200, 'message': '验证码发送成功！'})
    else:
        return JsonResponse({'code': 400, 'message': '此邮箱未被注册！'})


def decode(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({'code': 401, 'message': 'Authorization header missing'}, status=401)

    # Token一般形式为 'Bearer <token>'
    token = auth_header.split(' ')[1] if len(auth_header.split(' ')) == 2 else None
    if not token:
        return JsonResponse({'code': 401, 'message': 'Token missing or malformed'}, status=401)

    # 解码并验证Token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return user_id


@require_GET
def center(request):
    user_id = decode(request)
    user = User.objects.get(id=user_id)
    userdetail = UserDetail.objects.get(user_id=user_id)
    user_data = {
        'id': user_id,
        'name': user.username,
        'mail': user.email,
        'age': userdetail.age,
        'gender': userdetail.gender,
        'major': userdetail.major,
        'grade': userdetail.grade,
        'avatar': userdetail.avatar,
        'logintime': user.last_login,
    }
    return JsonResponse({'code': 200, 'user': user_data})


@require_GET
def center_id(request, user_id):
    user = User.objects.get(id=user_id)
    userdetail = UserDetail.objects.get(user_id=user_id)
    user_data = {
        'id': user_id,
        'name': user.username,
        'mail': user.email,
        'age': userdetail.age,
        'gender': userdetail.gender,
        'major': userdetail.major,
        'grade': userdetail.grade,
        'avatar': userdetail.avatar,
        'logintime': user.last_login,
    }
    return JsonResponse({'code': 200, 'user': user_data})


@require_POST
def modify_information(request):
    data = json.loads(request.body.decode('utf-8'))
    user_id = data.get('user_id')
    user = User.objects.get(id=user_id)
    username = data.get('昵称')
    if username != user.username and User.objects.filter(username=username).first():
        return JsonResponse({'code': 400, 'message': '用户名已被使用！'})
    else:
        user.username = username
        user.save()
    
    userdetail = UserDetail.objects.get(user=user)
    age = data.get('年龄')
    if age:
        userdetail.age = age
    gender = data.get('性别')
    if gender:
        userdetail.gender = gender
    major = data.get('专业')
    if major:
        userdetail.major = major
    grade = data.get('年级')
    if grade:
        userdetail.grade = grade
    userdetail.save()
    return JsonResponse({'code': 200, 'message': '修改信息成功！', 'username': user.username})


@require_POST
def modify_password(request):
    data = json.loads(request.body.decode('utf-8'))
    user_id = data.get('user_id')
    user = User.objects.get(id=user_id)
    old_password = data.get('oldPassword')
    if check_password(old_password, user.password):
        new_password = data.get('newPassword')
        if len(new_password) < 6:
            return JsonResponse({'code': 400, 'message': '密码长度需大于6位！'})
        else:
            user.set_password(new_password)
            user.save()
            return JsonResponse({'code': 200, 'message': '重置密码成功！'})
    else:
        return JsonResponse({'code': 400, 'message': '原密码错误！'})


@require_POST
def upload_avatar(request):
    avatar = request.FILES.get('avatar')
    if avatar:
        avatar_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, avatar_name)
        with open(file_path, 'wb') as destination:
            for chunk in avatar.chunks():
                destination.write(chunk)
        user_id = decode(request)
        user_detail = UserDetail.objects.get(user_id=user_id)
        user_detail.avatar = avatar_name
        user_detail.save()
        return JsonResponse({'code': 200, 'message': '操作成功！', 'avatar': avatar_name})
    return JsonResponse({'code': 500, 'message': '无头像上传！'})



from zone.models import Zone, Object
from zone.views import zone2Json, object2Json
from myblog.models import Blog
from myblog.views import blog2Json
@require_GET
def zone_followed(request):
    user_id = decode(request)
    zones = Zone.objects.filter(follows__user=user_id)
    return JsonResponse({'code': 200, 'zones': zone2Json(zones)})


@require_GET
def blog_collected(request):
    user_id = decode(request)
    blogs = Blog.objects.filter(collects__user=user_id)
    print(blogs.count())
    return JsonResponse({'code': 200, 'blogs': blog2Json(blogs, user_id)})


@require_GET
def object_stared(request):
    user_id = decode(request)
    objects = Object.objects.filter(stars__user=user_id)
    return JsonResponse({'code': 200, 'objects': object2Json(objects)})


@require_GET
def blog_pubed(request):
    user_id = decode(request)
    blogs = Blog.objects.filter(author_id=user_id)
    return JsonResponse({'code': 200, 'blogs': blog2Json(blogs)})


@require_GET
def object_pubed(request):
    user_id = decode(request)
    objects = Object.objects.filter(creator_id=user_id)
    return JsonResponse({'code': 200, 'objects': blog2Json(objects)})

        