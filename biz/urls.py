from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dash/', views.dash, name='dash'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('trials/', views.trials, name='trials'),
    path('test/', views.test, name='test'),
    path('api/analyze/', views.analyze, name='analyze'),
]
