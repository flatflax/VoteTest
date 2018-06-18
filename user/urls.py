from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'user'
urlpatterns = [
    # /user/login/
    path('login', views.login, name='login'),
    # /user/logout/
    path('logout',views.logout, name='logout'),
    # /user/register/
    path('register', views.register, name='register'),
] + static(settings.STATIC_URL,
document_root=settings.STATIC_URL)
