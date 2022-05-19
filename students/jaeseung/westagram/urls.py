
from django.urls import path, include

urlpatterns = [
    # users
    path("users", include("users.urls")),
    path("postings", include("postings.urls"))
]
