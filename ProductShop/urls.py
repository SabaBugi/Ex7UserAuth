from django.urls import path
from .views import home, product_page

app_name = 'product_shop'

urlpatterns = [
    path('', home, name='home'),
    path('product/', product_page, name='product_page'),  
]