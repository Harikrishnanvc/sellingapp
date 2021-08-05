from django.urls import path
from . import views
from products.views import CreatePostView
from products.views import BuyProductView
from products.views import GetBuyerDetailsView
from products.views import MyProductsView
from products.views import SellProductView
from products.views import Edit_product
from products.views import EditProductView
from products.views import BuyerListView
from products.views import SellProduct
from products.views import IntoAppliedProducts
urlpatterns = [
    path('create_post/',CreatePostView.as_view(), name='create_post'),
    path('loginn/',views.Product_list, name='post_list'),
    path('buy/id=<int:id>',BuyProductView.as_view(),name='buy_product'),
    path('buynow/',GetBuyerDetailsView.as_view(), name='buy_now'),
    path('my_products/',MyProductsView.as_view(), name='my_products'),
    path('sell/id=<int:id>', SellProductView.as_view(), name='sell_product'),
    path('edit_product_view',EditProductView.as_view(),name='edit_product_view'),
    path('edit_product',Edit_product,name='edit_product'),
    path('buyer_list/id=<int:id>',BuyerListView.as_view(), name='buyer_list'),
    path('sell_product/id=<int:id>',SellProduct.as_view(), name='sell_product_confirmation'),
    path('delete_product', views.Delete_Product, name='delete_product'),
    path('into_applied_products',IntoAppliedProducts.as_view(), name='into_applied_products')

]