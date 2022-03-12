from django.urls import path
from .views import BookList, BookRetrieve, BoxCreate, Delivery, Basket

urlpatterns = [
    path('list/', BookList.as_view(), name='book_list'),
    path('retrieve/<int:pk>/', BookRetrieve.as_view(), name='book_retrieve'),
    path('box/', BoxCreate.as_view(), name='box_create'),
    path('basket/', Basket.as_view(), name='basket'),
    path('delivery/', Delivery.as_view(), name='delivery'),
]
