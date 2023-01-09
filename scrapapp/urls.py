from django.urls import path,include
urlpatterns = [
    path('', include('scrap.urls')),
    path('', include('shop.urls')),
]
