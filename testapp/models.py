from django.db import models

# 配置缓存装饰器
import json
from functools import wraps
from django_redis import get_redis_connection
from django.db import models

# 编写缓存装饰器
_cache = get_redis_connection('default')


def cache(func):
    @wraps(func)
    def wrapper(obj, *args):
        key = args[0]
        value = _cache.get(key)
        if value:
            return json.loads(value)
        rs = func(obj, *args)
        _cache.set(key, json.dumps(rs))
        return rs
    return wrapper


# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    @classmethod
    @cache
    def get(cls, name):
        rs = cls.objects.get(name=name)
        return {
            'name': rs.name,
            'age': rs.age
        }


# 权限
class Apage(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    def Meta(self):
        permissions = [
            ('look_a_page', 'can get A page')
        ]


class Bpage(models.Model):
    name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    def Meta(self):
        permissions = [
            ('look_b_page', 'can get B page')
        ]
