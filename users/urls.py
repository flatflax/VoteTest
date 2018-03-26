from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'users'
urlpatterns = [
    # ex: /user/
    path('', views.index, name='index'),
    # ex: /user/signup
    path('signup', views.signup, name='signup'),
] + static(settings.STATIC_URL,
document_root=settings.STATIC_URL)