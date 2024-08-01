from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order, OrderItem
from django.contrib.auth.models import User, Group
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    Category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    #Category = CategorySerializer()
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','Category']
    
class CartSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Cart
        fields = ['id', 'user','menuitem', 'quantity', 'unit_price', 'price']
          
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        
class OderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'unit_price', 'price']
        
class UserSerilializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']