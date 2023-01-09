from django.urls import path
from . import views

urlpatterns = [
    path("shop", views.shopproducts, name="shop"),
    path("shop/index", views.shopproducts,name="shop/index"),
    path("shop/products", views.shopproducts, name="shop/products"),
    path("shop/products/<slug:slug>", views.shopproduct_details, name="shop/product-details"),
    path('shop/search', views.shopsearch_products, name='shop/search-products'),
    path("shop/login", views.login_request, name="login"),
    path("shop/register", views.register_request, name="register"),
    path("shop/logout", views.logout_request, name="logout"),
    path("admin/", views.admin, name="admin"),
    path("admin/products/<int:id>", views.admin_products, name="admin_products"),
    path("admin/rams/<int:id>", views.admin_rams, name="admin_rams"),
    path("admin/storages/<int:id>", views.admin_storages, name="admin_storages"),
    path("admin/processors/<int:id>", views.admin_processors, name="admin_processors"),
    path("admin/systems/<int:id>", views.admin_systems, name="admin_systems"),
    path("admin/screens/<int:id>", views.admin_screens, name="admin_screens"),
    path("admin/brands/<int:id>", views.admin_brands, name="admin_brands"),
    path("admin/product/add/", views.admin_product_add, name="admin_product_add"),
    path("admin/brand/add/", views.admin_brand_add, name="admin_brand_add"),
    path("admin/ram/add/", views.admin_ram_add, name="admin_ram_add"),
    path("admin/storage/add/", views.admin_storage_add, name="admin_storage_add"),
    path("admin/processor/add/", views.admin_processor_add, name="admin_processor_add"),
    path("admin/system/add/", views.admin_system_add, name="admin_system_add"),
    path("admin/screen/add/", views.admin_screen_add, name="admin_screen_add"), 
    
]