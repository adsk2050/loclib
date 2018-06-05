from django.urls import path, reverse
from . import views

app_name = 'catalog'
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    #path('search/', views.search, name='search')
]

urlpatterns += [
    path('books/]borrowed/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('books/all/borrowed', views.AllLoanedBooksListView.as_view(), name='all-borrowed'),
]

urlpatterns += [
    path('books/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('books/<uuid:pk>/return/', views.return_book_librarian, name='return-book-librarian'),
    path('books/<uuid:pk>/issue/', views.issue_book_librarian, name='issue-book-librarian')
]

urlpatterns += [
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
    path('bookinstance/create/', views.BookInstanceCreate.as_view(), name='bookinstance_create'),
    path('bookinstance/<int:pk>/update/', views.BookInstanceUpdate.as_view(), name='bookinstance_update'),
    path('bookinstance/<int:pk>/delete/', views.BookInstanceDelete.as_view(), name='bookinstance_delete'),
]

urlpatterns += [
    path('books/create/', views.BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]
