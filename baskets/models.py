from django.db import models

# Create your models here.
from django.utils.functional import cached_property

from authapp.models import User
from mainapp.models import Product


# class BasketQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()
        # self.user.basket.select_related()

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        # baskets = Basket.objects.filter(user=self.user)
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    # def delete(self,*args, **kwargs):
    #
    #     self.product.quantity += self.quantity
    #     self.save()
    #     super(Basket, self).delete(*args, **kwargs)
    #
    # def save(self,*args, **kwargs):
    #     if self.pk:
    #         get_item = self.get_item(int(self.pk))
    #         self.product.quantity -= self.quantity - get_item
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(Basket, self).save(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity
