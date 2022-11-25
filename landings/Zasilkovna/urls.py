from django.urls import path
from . import views


urlpatterns = [
    path(r'receive/<int:post_id>', views.index)
]
