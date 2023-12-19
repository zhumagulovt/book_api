from django.urls import path

from . import views


urlpatterns = [
    path('books/', views.BookListAPIView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailAPIView.as_view(), name='book-detail'),
]
