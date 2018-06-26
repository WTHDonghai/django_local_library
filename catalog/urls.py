from django.urls import path,re_path

from . import views

urlpatterns = [
        #re_path(r'^$',views.index,name = 'index'),
        path('',views.index,name = 'index'),
        path('books/',views.BookListView.as_view(),name = 'books'),
        path('book/<int:pk>',views.BookDetailView.as_view(),name='book-detail'),
        path('authors/',views.AuthorListView.as_view(),name = 'authors'),
        path('author/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'),
        path('mybooks/',views.LoanedBooksByUserListView.as_view(),name= 'my-borrowed'),
        path('borrowed/',views.CanMarkReturnedListView.as_view(),name='all-borrowed'),
]

#form 表单相关
urlpatterns +=[
        path('book/<uuid:pk>/renew/',views.renew_book_librarian,name='renew-book-librarian')
]

#通用视图的表单链接
urlpatterns += [
        path('author/create/',views.AuthorCreate.as_view(),name='author_create'),
        path('author/<int:pk>/update/',views.AuthorUpdate.as_view(),name='author_update'),
        path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author_delete'),
]
