from django.urls import path

from .views import PostingView, PostingDetailView

urlpatterns = [
    path('/post', PostingView.as_view()),
    path('/post/<int:id>', PostingDetailView.as_view()),
    
]