from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/register/', views.register_user,),
    path('users/login/', views.login_user,),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
