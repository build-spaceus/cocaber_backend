from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(
        "auth/",
        include(("api.v1.auth.urls", "api.v1.auth"), namespace="auth"),
    ),
]
