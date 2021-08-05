from django.contrib import admin
from .models import Post
from .models import Buyer
from .models import Seller
# Register your models here.
admin.site.register(Post)
admin.site.register(Buyer)
admin.site.register(Seller)