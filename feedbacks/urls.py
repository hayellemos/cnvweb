from django.urls import path
from . import views

urlpatterns = [
    path("novo/", views.novo_feedback, name="novo_feedback"),
]
