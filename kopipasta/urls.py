from django.urls import path

from .controllers import common

urlpatterns = [
    path('', common.common)
]
