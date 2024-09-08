from django.urls import path
from .views import SignupView,LoginView,CreateBookView,ListBook,update_collection,delete_records

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(), name='login'),
    path('addbook/',CreateBookView.as_view(),name='addbook'),
    path('record_list/',ListBook,name='record_list'),
    path('books/<int:id>/', update_collection, name='book-update'),
    path('delete/<int:id>/', delete_records, name='delete'),
    
    
]
