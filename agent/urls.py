from django.urls import path
from . import views

urlpatterns = [
    # other urls
    path('emails/', views.email_list, name='get_emails')
]
