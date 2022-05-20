from django.urls import path
from postings.views import PostView, CommentSearchView

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/comment/<int:post_id>', CommentSearchView.as_view()),
]