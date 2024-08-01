from django.urls import path 
from . import views 

urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category'),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('menu-items/', views.MenuItemsView.as_view(), name= 'menu-items'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    
    #path("menu-items/", views.menuitem, name='menu-items'),
    #path("menu-items/<int:pk>", views.singlemenuitem, name='singlemenuitem'),
    #path('menu-items/', views.MenuItemView.as_view()),
    #path('menu-items/<int:pk>', views.EditMenuItemView.as_view()),
    #path('groups/manager/users/', views.groupManagers, name='groupManagers'),
    #path('groups/manager/users/<int:pk>', views.deletegroupManagers, name='deletegroupManagers'),
    #path('groups/delivery-crew/users/', views.groupDelivery, name='groupDelivery'),
    #path('groups/delivery-crew/users/<int:pk>', views.deletegroupDelivery, name='deletegroupDelivery'),
    
    path('groups/manager/users', views.GroupViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='groups/manager/users'),

    path('groups/delivery-crew/users', views.DeliveryCrewViewSet.as_view(
        {'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='groups/delivery-crew/users'),
    
    #path('cart/menu-items/', views.CartList.as_view()),
    path('cart/menu-items/', views.cartMangement, name='cartManagemnet'),
    path('orders/', views.order, name='orders'),
    path('orders/<int:pk>', views.singleorder, name='order'),
]