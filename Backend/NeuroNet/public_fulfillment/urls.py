from django.urls import path
from public_fulfillment import views
from public_fulfillment import api

urlpatterns = [
    path('', views.about, name="about"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('update_profile/', views.update_profile, name="update_profile"),
    path('stop_email/', views.stop_email, name="stop_email"),
    path('stop_email_confirmed/', views.stop_email_confirmed, name="stop_email_confirmed"),    
    path('example/', views.example, name="example"),
    #path('privacy_policy/', views.privacy_policy, name="privacy_policy"),
    path('get_server_time/', api.get_server_time, name="get_server_time"),
]

    