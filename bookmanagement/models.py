from datetime import datetime
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import AbstractUser


class BookTypes(models.Model):
    typeid = models.CharField(max_length=2, primary_key=True, verbose_name='类型编号')
    typename = models.CharField(max_length=8, default='', verbose_name='类型名称')

    class Meta:
        db_table = 'booktypes'


class Publishers(models.Model):
    pubid = models.CharField(max_length=4, primary_key=True, verbose_name='出版社编号')
    pubname = models.CharField(max_length=20, null=False, default='', verbose_name='出版社名称')
    pubaddr = models.CharField(max_length=50, null=True, verbose_name='出版社地址')

    class Meta:
        db_table = 'publishers'


class Books(models.Model):
    bookid = models.CharField(max_length=10, primary_key=True, verbose_name='图书编号')
    bookname = models.CharField(max_length=50, null=False, verbose_name='图书名称')
    author = models.CharField(max_length=50, null=False, verbose_name='作者')
    publishdate = models.DateField(null=True, verbose_name='出版日期')
    ISBN = models.CharField(max_length=20, verbose_name='ISBN')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='价格')
    desc = models.CharField(max_length=200, verbose_name='简介', null=True, default='')
    booktype = models.ForeignKey(BookTypes, on_delete=models.CASCADE, verbose_name='图书类别')
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE, verbose_name='出版社')

    class Meta:
        db_table = 'books'


class UserTypes(models.Model):
    typeid = models.CharField(max_length=2, primary_key=True, verbose_name='类型编号')
    typename = models.CharField(max_length=8, default='', verbose_name='类型名称')

    class Meta:
        db_table = 'usertypes'


def current_year():
    return datetime.now().year


class Users(AbstractUser):
    gender_choices = (('男', '男'), ('女', '女'))
    gender = models.CharField(max_length=2, choices=gender_choices, verbose_name='性别')
    usertype = models.ForeignKey(UserTypes, on_delete=models.CASCADE, verbose_name='用户类型')
    enrolldate = models.IntegerField(verbose_name='入学时间', default=current_year)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='book_users',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='book_users',
        blank=True,
        verbose_name='user permissions',
    )

    class Meta:
        db_table = 'users'


class Borrows(models.Model):
    borrowid = models.AutoField(primary_key=True, verbose_name='借阅编号')
    username = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name='用户名')
    book = models.ForeignKey(Books, on_delete=models.CASCADE, verbose_name='图书')
    borrowdate = models.DateField(verbose_name="出借日期", auto_now_add=True)
    returndate = models.DateField(verbose_name="归还日期", null=True, blank=True)
    pay = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='费用', default=Decimal('0.00'))
    return_status_choices = ((0, '未归还'), (1, '已归还'), (2, '逾期归还'), (3, '丢失赔偿'))
    returntype = models.IntegerField(choices=return_status_choices, verbose_name='归还类型', default=0)

    class Meta:
        db_table = 'borrows'