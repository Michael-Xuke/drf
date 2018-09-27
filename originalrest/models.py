from django.db import models

# Create your models here.

# 商品吧


class Goods(models.Model):
    name = models.CharField(max_length=64, verbose_name='商品名称')
    price = models.IntegerField(verbose_name='商品价格')
    owner = models.ForeignKey('auth.User', related_name='goods')

    def to_dict(self):
        return {'name': self.name, 'price': self.price}
