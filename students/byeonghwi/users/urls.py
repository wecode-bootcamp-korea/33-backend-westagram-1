from django.urls import path
from users.views import UsersView, LoginView

urlpatterns = [
  path('', UsersView.as_view()),
  path('/login', LoginView.as_view())
]
