"""
URL configuration for coolboards project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import coolboards.views as views

admin.site.site_header = "Coolboards Admin"

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        # home page
        path("", views.home, name="home"),
        # products page
        path("products/", views.products, name="products"),
        # products page
        path("products/<str:category>", views.products, name="category"),
        # brand page
        path("brand/<str:brand>/", views.brand, name="brand"),
        # product page
        path("i/<int:item_id>/", views.product, name="product"),
        # cart page
        path("cart/", views.cart, name="cart"),
        # brands page
        path("brands/", views.brands, name="brands"),
        # categories page
        path("categories/", views.categories, name="categories"),
        path("order/", views.order, name="order"),
        path("ordercomplete/", views.ordercomplete, name="ordercomplete"),
        # post review
        path("review/<int:item_id>", views.post_review, name="review"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
