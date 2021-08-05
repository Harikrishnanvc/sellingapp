from django.db import models

# Create your models here.
class Post(models.Model):
    Product_name = models.CharField(max_length=150)
    Product_description = models.TextField()
    Product_category = models.CharField(max_length=50)
    Product_price = models.IntegerField()
    Product_image = models.ImageField(upload_to='image')
    Product_status = models.PositiveIntegerField()
    Username = models.CharField(max_length=150)
    # id = models.IntegerField(primary_key=True,auto_created=True)


    def __str__(self):
        return self.Product_name

class Buyer(models.Model):
    Username_buyer = models.CharField(max_length=150)
    Product_id = models.PositiveIntegerField()
    Buyer_price = models.PositiveIntegerField()
    Product_name = models.CharField(max_length=150, null=True)


class Seller(models.Model):
    Buyer_name = models.CharField(max_length=150, default=Buyer)
    Product_id = models.PositiveIntegerField(default=0)
