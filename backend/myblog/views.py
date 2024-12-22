import json, jwt, uuid, os
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.db.models import Q
from django.contrib.auth.models import User
from .models import BlogCategory, Blog, BlogComment, CmtComment, CollectBlog
from .models import LikeBlog, DislikeBlog, LikeBlogComment, DislikeBlogComment, LikeCmtComment, DislikeCmtComment


# Create your views here.
def blog2Json(blogs, user_id):
    user = User.objects.get(id=user_id)
    blogs_data = []
    for blog in blogs:
        blog_dict = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'pub_time': blog.pub_time,
            'categories': list(blog.category.values('id', 'name')),
            'author': User.objects.get(id=blog.author_id).username,
            'avatar': User.objects.get(id=blog.author_id).userdetail.avatar,
            'graphic': blog.graphic,
            'likes': blog.likes.count(),
            'dislikes': blog.dislikes.count(),
            'collects': blog.collects.count(),
            'comments': blog.comments.count(),
            'liked': LikeBlog.objects.filter(blog_id=blog.id, user_id=user_id).exists(),
            'disliked': DislikeBlog.objects.filter(blog_id=blog.id, user_id=user_id).exists(),
            'collected': CollectBlog.objects.filter(blog_id=blog.id, user_id=user_id).exists(),
            'privilege': blog.author_id == user_id or user.is_superuser,
        }
        blogs_data.append(blog_dict)
    return blogs_data[::-1]


def filter_blogs_by_interests(blogs, user_id):
    interests = set()
    collected_blogs = Blog.objects.filter(collects__user=user_id)
    for blog in collected_blogs:
        interests.update(blog.category.values_list('id', flat=True))
    liked_blogs = Blog.objects.filter(likes__user=user_id)
    for blog in liked_blogs:
        interests.update(blog.category.values_list('id', flat=True))
        
    filtered_blogs = []
    for blog in blogs:
        blog_tags = set(blog.category.values_list('id', flat=True))
        if interests & blog_tags:
            filtered_blogs.append(blog)

    if len(filtered_blogs) < 12:
        remaining_blogs = [blog for blog in blogs if blog not in filtered_blogs]
        additional_blogs = remaining_blogs[0:12 - len(filtered_blogs)]
        filtered_blogs.extend(additional_blogs)
    return filtered_blogs


@require_GET
def blog_interest(request):
    blogs = Blog.objects.all().order_by('pub_time')
    user_id = decode(request)
    blogs = filter_blogs_by_interests(blogs, user_id)
    return JsonResponse({'code': 200, 'blogs': blog2Json(blogs, user_id)})


@require_GET
def blog_all(request):
    blogs = Blog.objects.all().order_by('pub_time')
    user_id = decode(request)
    return JsonResponse({'code': 200, 'blogs': blog2Json(blogs, user_id)})


@require_GET
def category_all(request):
    categories = BlogCategory.objects.all()
    categories_data = []
    for category in categories:
        category_dict = {
            'id': category.id,
            'name': category.name,
        }
        categories_data.append(category_dict)
    return JsonResponse({'code': 200, 'categories': categories_data})


@require_POST
def search_by_keyword(request):
    user_id = decode(request)
    data = json.loads(request.body.decode('utf-8'))
    q = data.get('query')
    blogs = Blog.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)).all()
    return JsonResponse({'code': 200, 'blogs': blog2Json(blogs, user_id)})


@require_GET
def search_by_category(request, category_id):
    user_id = decode(request)
    blogs = Blog.objects.filter(category__id=category_id).all()
    return JsonResponse({'code': 200, 'blogs': blog2Json(blogs, user_id)})


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
def blog_detail(request, blog_id):
    user_id = decode(request)
    user = User.objects.get(id=user_id)
    blog = Blog.objects.get(id=blog_id)
    comments = BlogComment.objects.filter(blog_id=blog_id)
    comments_data = []
    for comment in comments:
        comment_author = User.objects.get(id=comment.author_id)
        cmtcomments = CmtComment.objects.filter(comment_id=comment.id)
        cmtcomments_data = []
        for cmtcomment in cmtcomments:
            cmtcomment_author = User.objects.get(id=cmtcomment.author_id)
            cmtcomment_dict = {
                'id': cmtcomment.id,
                'content': cmtcomment.content,
                'pub_time': cmtcomment.pub_time,
                'likes': cmtcomment.likes.count(),
                'dislikes': cmtcomment.dislikes.count(),
                'liked': LikeCmtComment.objects.filter(comment_id=cmtcomment.id, user_id=user_id).exists(),
                'disliked': DislikeCmtComment.objects.filter(comment_id=cmtcomment.id, user_id=user_id).exists(),
                'reply_to': { 'id': comment_author.id, 'username': comment_author.username },
                'author': { 'id': cmtcomment_author.id, 'username': cmtcomment_author.username, 'avatar': cmtcomment_author.userdetail.avatar },
                'privilege': cmtcomment.author_id == user_id or user.is_superuser,
            }
            cmtcomments_data.append(cmtcomment_dict)
        comment_dict = {
            'id': comment.id,
            'content': comment.content,
            'pub_time': comment.pub_time,
            'likes': comment.likes.count(),
            'dislikes': comment.dislikes.count(),
            'liked': LikeBlogComment.objects.filter(comment_id=comment.id, user_id=user_id).exists(),
            'disliked': DislikeBlogComment.objects.filter(comment_id=comment.id, user_id=user_id).exists(),
            'author': { 'id': comment_author.id, 'username': comment_author.username, 'avatar': comment_author.userdetail.avatar },
            'cmtcomments': cmtcomments_data,
            'privilege': comment.author_id == user_id or user.is_superuser,
        }
        comments_data.append(comment_dict)
    
    author = User.objects.get(id=blog.author_id)
    blog_data = {
        'id': blog.id,
        'title': blog.title,
        'content': blog.content,
        'pub_time': blog.pub_time,
        'categories': list(blog.category.values('id', 'name')),
        'author': { 'id': author.id, 'username': author.username, 'avatar': author.userdetail.avatar },
        'likes': blog.likes.count(),
        'dislikes': blog.dislikes.count(),
        'collects': blog.collects.count(),
        'liked': LikeBlog.objects.filter(blog_id=blog.id, user_id=user_id).exists(),
        'disliked': DislikeBlog.objects.filter(blog_id=blog.id, user_id=user_id).exists(),
        'collected': CollectBlog.objects.filter(blog_id=blog.id, user_id=user_id).exists(),
        'graphic': blog.graphic,
        'comments': comments_data,
        'privilege': blog.author_id == user_id or user.is_superuser,
    }
    return JsonResponse({'code': 200, 'blog': blog_data})


@require_POST
def blog_modify(request, blog_id):
    title = request.POST.get('title')
    content = request.POST.get('content')
    graphic = request.FILES.get('graphic')
    blog = Blog.objects.get(id=blog_id)
    
    blog.title = title
    blog.content = content
    graphic_name = ''
    if graphic:
        graphic_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, graphic_name)
        with open(file_path, 'wb') as destination:
            for chunk in graphic.chunks():
                destination.write(chunk)
        blog.graphic = graphic_name
    blog.save()
    return JsonResponse({'code': 200, 'message': '创建成功！', 'graphic': graphic_name})


@require_POST
def pub_blog(request):
    user_id = decode(request)
    title = request.POST.get('title')
    content = request.POST.get('content')
    graphic = request.FILES.get('graphic')
    if graphic:
        graphic_name = f'{uuid.uuid4()}.png'
        file_path = os.path.join(settings.MEDIA_ROOT, graphic_name)
        with open(file_path, 'wb') as destination:
            for chunk in graphic.chunks():
                destination.write(chunk)
        blog = Blog.objects.create(title=title, content=content, author_id=user_id, graphic=graphic_name)
    else:
        blog = Blog.objects.create(title=title, content=content, author_id=user_id)
    
    categories = json.loads(request.POST.get('categories'))
    for item in categories:
        category = BlogCategory.objects.get(id=item.get('id'))
        blog.category.add(category)
    return JsonResponse({'code': 200, 'message': '帖子发布成功！', 'blog_id': blog.id})


@require_POST
def pub_comment(request):
    user_id = decode(request)
    data = json.loads(request.body.decode('utf-8'))
    blog_id = data.get('blog_id')
    content = data.get('content')
    BlogComment.objects.create(content=content, blog_id=blog_id, author_id=user_id)
    return JsonResponse({'code': 200, 'message': '发布成功！'})


@require_POST
def pub_cmt_comment(request):
    user_id = decode(request)
    data = json.loads(request.body.decode('utf-8'))
    cmt_id = data.get('cmt_id')
    content = data.get('cmtcontent')
    CmtComment.objects.create(content=content, comment_id=cmt_id, author_id=user_id)
    return JsonResponse({'code': 200, 'message': '发布成功！'})


@require_GET
def collect_blog(request, blog_id):
    user_id = decode(request)
    collect, created = CollectBlog.objects.get_or_create(user_id=user_id, blog_id=blog_id)
    if not created:
        collect.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def like_blog(request, blog_id):
    user_id = decode(request)
    like, created = LikeBlog.objects.get_or_create(user_id=user_id, blog_id=blog_id)
    if not created:
        like.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def dislike_blog(request, blog_id):
    user_id = decode(request)
    dislike, created = DislikeBlog.objects.get_or_create(user_id=user_id, blog_id=blog_id)
    if not created:
        dislike.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def like_cmt(request, cmt_id):
    user_id = decode(request)
    like, created = LikeBlogComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        like.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def dislike_cmt(request, cmt_id):
    user_id = decode(request)
    dislike, created = DislikeBlogComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        dislike.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def like_cmt_cmt(request, cmt_id):
    user_id = decode(request)
    like, created = LikeCmtComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        like.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def dislike_cmt_cmt(request, cmt_id):
    user_id = decode(request)
    dislike, created = DislikeCmtComment.objects.get_or_create(user_id=user_id, comment_id=cmt_id)
    if not created:
        dislike.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！', 'created': created})


@require_GET
def delete_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    comments = BlogComment.objects.filter(blog_id=blog_id)
    for comment in comments:
        cmtcomments = CmtComment.objects.filter(comment_id=comment.id)
        for cmtcomment in cmtcomments:
            cmtcomment.delete()
        comment.delete()
    blog.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def delete_cmt(request, cmt_id):
    comment = BlogComment.objects.get(id=cmt_id)
    cmtcomments = CmtComment.objects.filter(comment_id=comment.id)
    for cmtcomment in cmtcomments:
        cmtcomment.delete()
    comment.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})


@require_GET
def delete_cmt_cmt(request, cmt_id):
    cmtcomment = CmtComment.objects.get(id=cmt_id)
    cmtcomment.delete()
    return JsonResponse({'code': 200, 'message': '操作成功！'})

