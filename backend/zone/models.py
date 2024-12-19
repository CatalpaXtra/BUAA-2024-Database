from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Zone(models.Model):
    name = models.CharField(max_length=32)
    introduction = models.TextField()
    view_num = models.IntegerField(default=0)
    graphic = models.CharField(max_length=256, default='kobe.png')
    created_at = models.DateTimeField(auto_now_add=True)


class FollowZone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='follows')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'zone')
        ordering = ['-created_at']


class ZoneAdmin(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='admins')
    created_or_update_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_or_update_at']


class Object(models.Model):
    name = models.CharField(max_length=32)
    introduction = models.TextField()
    view_num = models.IntegerField(default=0)
    star_ave = models.FloatField(default=-1)
    graphic = models.CharField(max_length=256, default='kobe.png')
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class StarObject(models.Model):
    star = models.IntegerField(default=-1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='stars')
    created_or_update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_or_update_at']


class CollectObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='collects')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'object')  # 确保每个用户只能对每篇帖子点赞一次
        ordering = ['-created_at']


class ObjectComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-pub_time']


class LikeObjectComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(ObjectComment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # 确保每个用户只能对一级评论点赞一次
        ordering = ['-created_at']


class DislikeObjectComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(ObjectComment, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # 确保每个用户只能对一级评论点踩一次
        ordering = ['-created_at']
        

class ObjectCmtComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(ObjectComment, on_delete=models.CASCADE, related_name='cmtcomments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-pub_time']


class LikeObjectCmtComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(ObjectCmtComment, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # 确保每个用户只能对二级评论点赞一次
        ordering = ['-created_at']


class DislikeObjectCmtComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(ObjectCmtComment, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')  # 确保每个用户只能对二级评论点踩一次
        ordering = ['-created_at']
