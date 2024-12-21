from django.urls import path, include
from webapp.views import HomePage

urlpatterns = [
    path("", HomePage.as_view())
]