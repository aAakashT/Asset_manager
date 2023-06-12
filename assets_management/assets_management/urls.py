"""
URL configuration for assets_management project.

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
from Asset_Tracker.views import *
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', login_required(AssetChartView.as_view()), name='dashboard'),
    path('asset_types/create/', create_asset_type, name='create_asset_type'),
    path('asset_types/data/', AssetTypeListJson.as_view(), name='asset_types_data'),
    path('asset_types/', login_required(AssetTypeListView.as_view()), name='asset_types'),
    path('asset_types/<int:pk>/update/', update_asset_type, name='update_asset_type'),
    path('asset_types/<int:pk>/delete/', AssetTypeDeleteView.as_view(), name='delete_asset_type'),
    path('assets/create/', create_asset, name='create_asset'),
    path('assets/data/', AssetListJson.as_view(), name='assets_data'),
    path('assets/', login_required(AssetListView.as_view()), name='assets'),
    path('assets/<int:id>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
    path('assets/<int:pk>/update/', update_asset, name='update_asset'),
    path('assets_image/create/', create_asset_image, name='create_asset_image'),
    path('assets/download/', download_assets_view, name='download_assets'),
    path('images/data/', ImagesJson.as_view(), name="image_data"),
    path('image/', login_required(ImageListView.as_view()), name="images") 
    ] 
from django.conf import settings
from django.conf.urls.static import static


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)