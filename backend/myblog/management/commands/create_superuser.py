from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from user.models import UserDetail

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('username', type=str, nargs='?', help='用户名')
        parser.add_argument('email', type=str, nargs='?', help='邮箱')
        parser.add_argument('password', type=str, nargs='?', help='密码')

    def handle(self, *args, **kwargs):
        username = kwargs.get('username')
        if username is None:
            username = input("请输入用户名: ")
        # 正确使用用户名对应的字段名 'username' 进行查询验证
        if User.objects.filter(username=username).exists():
            raise ValueError(f"用户名 {username} 已存在，请重新输入")

        email = kwargs.get('email')
        if email is None:
            email = input("请输入邮箱: ")
        if User.objects.filter(email=email).exists():
            raise ValueError(f"邮箱 {email} 已存在，请重新输入")
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(f"邮箱 {email} 格式错误")

        password = kwargs.get('password')
        if password is None:
            password = input("请输入密码: ")
        if len(password) < 6:
            raise ValueError(f"密码 {password} 长度需大于等于6位")

        # 先创建用户
        self.create_user(username, email, password)
    
    def create_user(self, username, email, password):
        try:
            user = User.objects.create_superuser(username=username, email=email, password=password)
            UserDetail.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))