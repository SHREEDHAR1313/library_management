from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.book_list, name='book_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:book_id>/delete/', views.book_delete, name='book_delete'),
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.member_add, name='member_add'),
    path('members/<int:member_id>/delete/', views.member_delete, name='member_delete'),
    path('issue/', views.issue_view, name='issue_view'),
    path('return/<int:transaction_id>/', views.return_book, name='return_book'),
    path('transactions/', views.transaction_list, name='transaction_list'),
]
