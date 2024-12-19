import json, jwt, uuid, os
from django.conf import settings
from django.core.cache import cache
from django.db.models import Count
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from .models import Zone, FollowZone, ZoneAdmin, Object, StarObject, CollectObject
from .models import ObjectComment, LikeObjectComment, DislikeObjectComment, ObjectCmtComment, LikeObjectCmtComment, DislikeObjectCmtComment
from django.views.decorators.http import require_POST, require_GET


# Create your views here.
def object2Json(objects):
    objects_data = []
    for object in objects:
        comments = ObjectComment.objects.filter(object_id=object.id)
        most_liked_comment = comments.annotate(
            like_count = Count('likes')
        ).order_by('-like_count').first()
        if most_liked_comment:
            most_liked_comment = most_liked_comment.content
        else:
            most_liked_comment = '尚未有人进行过评论'
        
        object_dict = {
            'id': object.id,
            'name': object.name,
            'introduction': object.introduction,
            'graphic': object.graphic,
            'reviews_count': object.view_num,
            'star_count': StarObject.objects.filter(object_id=object.id).count(),
            'star_ave': round(object.star_ave, 1),
            'hot_comment': most_liked_comment,
        }
        objects_data.append(object_dict)
    return objects_data[::-1]


def zone2Json(zones):
    zones_data = []
    for zone in zones:
        objects = Object.objects.filter(zone_id=zone.id).annotate(
            star_count=Count('stars')
        ).order_by('star_count', 'star_ave')
        zone_dict = {
            'id': zone.id,
            'name': zone.name,
            'introduction': zone.introduction,
            'graphic': zone.graphic,
            'view_num': zone.view_num,
            'objects': object2Json(objects),
        }
        zones_data.append(zone_dict)
    return zones_data[::-1]


@require_GET
def zone_all(request):
    zones = Zone.objects.all().order_by('view_num')
    return JsonResponse({'code': 200, 'zones': zone2Json(zones)})


def decode(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({'code': 401, 'message': 'Authorization header missing'})

    # Token一般形式为 'Bearer <token>'
    token = auth_header.split(' ')[1] if len(auth_header.split(' ')) == 2 else None
    if not token:
        return JsonResponse({'code': 401, 'message': 'Token missing or malformed'})

    # 解码并验证Token
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return user_id


@require_GET
def zone_detail(request, zone_id):
    user_id = decode(request)
    user = User.objects.get(id=user_id)
    cache_key = f'zone_{zone_id}_user_{user.id}_viewed'
    zone = Zone.objects.filter(id=zone_id).first()
    if not cache.get(cache_key):
        zone.view_num += 1
        cache.set(cache_key, True, timeout=15 * 60)
        zone.save()
    
    objects = Object.objects.filter(zone_id=zone_id).annotate(
        star_count=Count('stars')
    ).order_by('star_count', 'star_ave')
    zone_data = {
        'id': zone.id,
        'name': zone.name,
        'introduction': zone.introduction,
        'graphic': zone.graphic,
        'created_at': zone.created_at,
        'view_num': zone.view_num,
        'objects': object2Json(objects),
        'follows': zone.follows.count(),
        'privilege': ZoneAdmin.objects.filter(zone=zone, admin=user).exists() or user.is_superuser,
    }
    data = {
        'zone': zone_data,
        'isFollowed': FollowZone.objects.filter(zone=zone, user=user).exists(),
    }
    return JsonResponse({'code': 200, 'data': data})


@require_POST
def create_zone(request):
    user_id = decode(request)
    name = request.POST.get('titie')
    if Zone.objects.filter(name=name):
        return JsonResponse({'code': 400, 'message': '专区名重复！'})
    introduction = request.POST.get('introduction')
    
    graphic = request.FILES.get('graphic')
    if graphic:
        graphic_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, graphic_name)
        with open(file_path, 'wb') as destination:
            for chunk in graphic.chunks():
                destination.write(chunk)
        zone = Zone.objects.create(name=name, introduction=introduction, graphic=graphic_name)
    else:
        zone = Zone.objects.create(name=name, introduction=introduction)
    
    objects = json.loads(request.POST.get('objects'))
    for object in objects:
        name = object.get('name')
        introduction = object.get('description')
        
        file = request.FILES.get(f'files[{name}]')
        file_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        Object.objects.create(name=name, introduction=introduction, zone_id=zone.id, graphic=file_name, creator_id=user_id)
    ZoneAdmin.objects.create(admin_id=user_id, zone_id=zone.id)
    return JsonResponse({'code': 200, 'message': '创建成功！'})

from django.db.models import Q
@require_POST
def zone_modify(request, zone_id):
    name = request.POST.get('name')
    introduction = request.POST.get('introduction')
    graphic = request.FILES.get('graphic')
    zone = Zone.objects.get(id=zone_id)
    if name != zone.name and Zone.objects.filter(Q(name__exact=name)):
        return JsonResponse({'code': 400, 'message': '对象名重复！'})
    
    zone.name = name
    zone.introduction = introduction
    graphic_name = ''
    if graphic:
        graphic_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, graphic_name)
        with open(file_path, 'wb') as destination:
            for chunk in graphic.chunks():
                destination.write(chunk)
        zone.graphic = graphic_name
    zone.save()
    return JsonResponse({'code': 200, 'message': '创建成功！', 'graphic': graphic_name})


@require_GET
def follow_zone(request, zone_id):
    user_id = decode(request)
    zone = Zone.objects.get(id=zone_id)
    follow, created = FollowZone.objects.get_or_create(user_id=user_id, zone=zone)
    if not created:
        follow.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})



@require_GET
def object_all(request):
    objects = Object.objects.filter(star_ave__gt=0).annotate(
        star_count=Count('stars')
    ).order_by('-star_count', '-star_ave')
    return JsonResponse({'code': 200, 'objects': object2Json(objects[0:8])[::-1]})


@require_GET
def object_detail(request, object_id):
    user_id = decode(request)
    user = User.objects.get(id=user_id)
    cache_key = f'object_{object_id}_user_{user_id}_viewed'
    object = Object.objects.filter(id=object_id).first()
    if not cache.get(cache_key):
        object.view_num += 1
        cache.set(cache_key, True, timeout=15 * 60)
        object.save()
    
    comments = ObjectComment.objects.filter(object_id=object_id)
    comments_data = []
    for comment in comments:
        comment_author = User.objects.get(id=comment.author_id)
        cmtcomments = ObjectCmtComment.objects.filter(comment_id=comment.id)
        cmtcomments_data = []
        for cmtcomment in cmtcomments:
            cmtcomment_author = User.objects.get(id=cmtcomment.author_id)
            cmtcomment_dict = {
                'id': cmtcomment.id,
                'content': cmtcomment.content,
                'pub_time': cmtcomment.pub_time,
                'likes': cmtcomment.likes.count(),
                'dislikes': cmtcomment.dislikes.count(),
                'liked': LikeObjectCmtComment.objects.filter(comment_id=cmtcomment.id, user_id=user_id).exists(),
                'disliked': DislikeObjectCmtComment.objects.filter(comment_id=cmtcomment.id, user_id=user_id).exists(),
                'reply_to': { 'id': comment_author.id, 'username': comment_author.username },
                'author': { 'id': cmtcomment_author.id, 'username': cmtcomment_author.username, 'avatar': cmtcomment_author.userdetail.avatar },
                'privilege': cmtcomment.author_id == user_id or user.is_superuser,
                'star': starObject.star if (starObject := StarObject.objects.filter(object=object, user_id=cmtcomment.author_id).first()) else -1,
            }
            cmtcomments_data.append(cmtcomment_dict)
        comment_dict = {
            'id': comment.id,
            'content': comment.content,
            'pub_time': comment.pub_time,
            'likes': comment.likes.count(),
            'dislikes': comment.dislikes.count(),
            'liked': LikeObjectComment.objects.filter(comment_id=comment.id, user_id=user_id).exists(),
            'disliked': DislikeObjectComment.objects.filter(comment_id=comment.id, user_id=user_id).exists(),
            'author': { 'id': comment_author.id, 'username': comment_author.username, 'avatar': comment_author.userdetail.avatar },
            'cmtcomments': cmtcomments_data,
            'privilege': comment.author_id == user_id or user.is_superuser,
            'star': starObject.star if (starObject := StarObject.objects.filter(object=object, user_id=comment.author_id).first()) else -1,
        }
        comments_data.append(comment_dict)
    
    stars = StarObject.objects.filter(object_id=object_id)
    star_count = {i: 0 for i in range(1, 6)}
    for star in stars:
        star_count[star.star] += 1
    
    object_data = {
        'id': object.id,
        'name': object.name,
        'introduction': object.introduction,
        'view_num': object.view_num,
        'star_ave': round(object.star_ave, 1),
        'graphic': object.graphic,
        'created_at': object.created_at,
        'star_count': StarObject.objects.filter(object_id=object.id).count(),
        'star_num': star_count,
        'comments': comments_data,
        'privilege': Object.objects.filter(zone_id=object.zone_id).count() > 3 and (object.creator_id == user_id or user.is_superuser),
        'privilege_modi': object.creator_id == user_id or user.is_superuser,
        'zone_id': object.zone_id,
    }
    data = {
        'object': object_data,
        'user_star': starObject.star if (starObject := StarObject.objects.filter(object=object, user=user).first()) else -1,
    }
    return JsonResponse({'code': 200, 'data': data})


@require_POST
def star_object(request, object_id):
    user_id = decode(request)
    data = json.loads(request.body.decode('utf-8'))
    starObject, _ = StarObject.objects.get_or_create(user_id=user_id, object_id=object_id)
    starObject.star = data.get('value')
    starObject.save()
    
    object = Object.objects.filter(id=object_id).first()
    stars = StarObject.objects.filter(object=object).all()
    if stars.count() == 0:
        object.star_ave = -1
    else:
        star_sum = 0
        for star in stars:
            star_sum += star.star
        object.star_ave = star_sum / stars.count()
    object.save()
    
    stars = StarObject.objects.filter(object_id=object_id)
    star_count = {i: 0 for i in range(1, 6)}
    for star in stars:
        star_count[star.star] += 1
    
    return JsonResponse({'code': 200, 'message': '评分成功！', 'star_num': star_count, 'star_ave': round(object.star_ave, 1)})


@require_GET
def collect_object(request, object_id):
    user_id = decode(request)
    collect, created = CollectObject.objects.get_or_create(user_id=user_id, object_id=object_id)
    if not created:
        collect.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_POST
def create_object(request, zone_id):
    user_id = decode(request)
    name = request.POST.get('name')
    if Object.objects.filter(zone_id=zone_id, name=name):
        return JsonResponse({'code': 400, 'message': '对象名重复！'})
    introduction = request.POST.get('introduction')
    
    graphic = request.FILES.get('graphic')
    if graphic:
        graphic_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, graphic_name)
        with open(file_path, 'wb') as destination:
            for chunk in graphic.chunks():
                destination.write(chunk)
        Object.objects.create(name=name, introduction=introduction, zone_id=zone_id, graphic=graphic_name, creator_id=user_id)
    else:
        Object.objects.create(name=name, introduction=introduction, zone_id=zone_id, creator_id=user_id)
    return JsonResponse({'code': 200, 'message': '创建成功！'})


@require_POST
def object_modify(request, object_id):
    name = request.POST.get('name')
    introduction = request.POST.get('introduction')
    graphic = request.FILES.get('graphic')
    object = Object.objects.get(id=object_id)
    if name != object.name and Object.objects.filter(zone_id=object.zone_id, name=name):
        return JsonResponse({'code': 400, 'message': '对象名重复！'})
    
    object.name = name
    object.introduction = introduction
    graphic_name = ''
    if graphic:
        graphic_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, graphic_name)
        with open(file_path, 'wb') as destination:
            for chunk in graphic.chunks():
                destination.write(chunk)
        object.graphic = graphic_name
    object.save()
    return JsonResponse({'code': 200, 'message': '创建成功！', 'graphic': graphic_name})


@require_POST
def pub_comment(request):
    user_id = decode(request)
    data = json.loads(request.body.decode('utf-8'))
    object_id = data.get('object_id')
    content = data.get('content')
    ObjectComment.objects.create(content=content, object_id=object_id, author_id=user_id)
    return JsonResponse({'code': 200, 'message': '发布成功！'})


@require_POST
def pub_cmt_comment(request):
    user_id = decode(request)
    data = json.loads(request.body.decode('utf-8'))
    cmt_id = data.get('cmt_id')
    content = data.get('cmtcontent')
    ObjectCmtComment.objects.create(content=content, comment_id=cmt_id, author_id=user_id)
    return JsonResponse({'code': 200, 'message': '发布成功！'})


@require_GET
def like_cmt(request, cmt_id):
    user_id = decode(request)
    like, created = LikeObjectComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        like.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def dislike_cmt(request, cmt_id):
    user_id = decode(request)
    dislike, created = DislikeObjectComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        dislike.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def like_cmt_cmt(request, cmt_id):
    user_id = decode(request)
    like, created = LikeObjectCmtComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        like.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def dislike_cmt_cmt(request, cmt_id):
    user_id = decode(request)
    dislike, created = DislikeObjectCmtComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        dislike.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


# TODO 对象删除、评论删除
@require_GET
def select_admin_set(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    admins = zone.admins.all()
    users = User.objects.all().exclude(id__in=admins.values_list('admin_id', flat=True))
    users_data = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'major': user.userdetail.major,
            'grade': user.userdetail.grade,
        }
        users_data.append(user_data)
    return JsonResponse({'code': 200, 'users': users_data})


@require_GET
def select_admin_del(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    users = ZoneAdmin.objects.filter(zone=zone).all()
    users_data = []
    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'major': user.userdetail.major,
            'grade': user.userdetail.grade,
        }
        users_data.append(user_data)
    return JsonResponse({'code': 200, 'users': users_data})


@require_GET
def set_admin(request, zone_id, admin_id):
    admin = User.objects.get(id=admin_id)
    zone = Zone.objects.get(id=zone_id)
    ZoneAdmin.objects.create(admin=admin, zone=zone)
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def del_admin(request, zone_id, admin_id):
    admin = User.objects.get(id=admin_id)
    zone = Zone.objects.get(id=zone_id)
    ZoneAdmin.objects.filter(admin=admin, zone=zone).delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def delete_zone(request, zone_id):
    zone = Zone.objects.get(id=zone_id)
    zone.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def delete_object(request, object_id):
    object = Object.objects.get(id=object_id)
    comments = ObjectComment.objects.filter(object_id=object_id)
    for comment in comments:
        cmtcomments = ObjectCmtComment.objects.filter(comment_id=comment.id)
        for cmtcomment in cmtcomments:
            cmtcomment.delete()
        comment.delete()
    object.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def delete_cmt(request, cmt_id):
    comment = ObjectComment.objects.get(id=cmt_id)
    cmtcomments = ObjectCmtComment.objects.filter(comment_id=comment.id)
    for cmtcomment in cmtcomments:
        cmtcomment.delete()
    comment.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def delete_cmt_cmt(request, cmt_id):
    cmtcomment = ObjectCmtComment.objects.get(id=cmt_id)
    cmtcomment.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})
