from django.urls import path
from . import views

urlpatterns = [
    path("", views.scrapproducts, name="home"),
    path("scrap", views.scrapproducts, name="scrap"),
    path("scrap/index", views.scrapproducts,name="scrap/index"),
    path("scrap/products", views.scrapproducts, name="scrap/products"),
    path("scrap/products/<slug:slug>", views.scrapproduct_details, name="scrap/product-details"),
    path('scrap/search', views.scrapsearch_products, name='scrap/search-products'),
]