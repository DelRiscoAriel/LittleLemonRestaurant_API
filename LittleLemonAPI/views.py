from django.shortcuts import render, get_object_or_404
from rest_framework import status
from django.db import IntegrityError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from .models import *
from .serializers import *
from .permissions import IsManager, IsDelivey
from django.forms.models import model_to_dict
from django.contrib.auth.models import User, Group
from django.core import serializers
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets

def home(request):
    return render(request, 'home.html')
    
# Create your views here.   
@permission_classes([IsManager])  
@throttle_classes([UserRateThrottle])  
class CategoryView(generics.ListCreateAPIView):  
    queryset = Category.objects.all()  
    serializer_class = CategorySerializer  

@throttle_classes([UserRateThrottle])
class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()  
    serializer_class = CategorySerializer
    
'''@api_view(['GET', 'POST'])
@throttle_classes([AnonRateThrottle])
def menuitem(request):
    if(request.method=='GET'):
        items = MenuItem.objects.select_related('Category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage',default=10)
        page = request.query_params.get('page',default=1)
        if(category_name):
            items = items.filter(Category__title=category_name)
        if(to_price):
            items = items.filter(price__lte = to_price)
        if(search):
            items = items.filter(title__icontains = search)
        if(ordering):
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)
        
        paginator = Paginator(items,per_page=perpage)
        try:
            items= paginator.page(number=page)
        except EmptyPage:
            items = []
        serialize_item = MenuItemSerializer(items, many=True)
        return Response(serialize_item.data, status=200)
    
    elif(request.method=='POST' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):  
        title = request.POST.get('title')
        price = request.POST.get('price')
        featured = request.POST.get('featured')
        category = request.POST.get('category')
        c = Category.objects.get(pk=category)
        z = Category.objects.get(pk=1)
        
        if request.POST.get('id') :
            id = request.POST.get('id')
            item = MenuItem(
                id = id,
                title = title,
                price = price,
                featured = featured,
                Category = c 
            )
        else: 
            item = MenuItem(
                title = title,
                price = price,
                featured = featured,
                Category = c,    
            )
        try: 
            item.save()
        except IntegrityError:
            return Response({'message':'required field missing'}, status=400)
        
        return Response(model_to_dict(item), status=201)
    
    else:
        return Response({'message':'unauthorize user'}, status=403)
    
@api_view(['GET', 'PATCH', 'DELETE'])
@throttle_classes([AnonRateThrottle])
def singlemenuitem(request, pk=None):
    if(request.method=='GET'):
        if pk: 
            item = get_object_or_404(MenuItem, pk=pk)
            s = MenuItemSerializer(item)  
        return Response(s.data, status=200)  
    
    elif(request.method=='PATCH' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):  
        title = request.POST.get('title')
        price = request.POST.get('price')
        featured = request.POST.get('featured')
        category = request.POST.get('category')
        
        c = Category.objects.get(pk=category)
        item = MenuItem(
            id = pk,
            title = title,
            price = price,
            featured = featured,
            Category = c    
        )
        try: 
            MenuItem.objects.filter(id=pk).delete()
            item.save()
        except IntegrityError:
            return Response({'message':'required field missing'}, status=400)
        
        return Response(model_to_dict(item), status=200) 
    
    elif(request.method=='DELETE' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        try:
            MenuItem.objects.filter(pk=pk).delete()
            return Response({'message':'object deleted'}, status=200)
        except:
            return Response({'message':'error'}, status=400)
    
    else:
        return Response({'message':'unauthorize user'}, status=403)
'''

@throttle_classes([UserRateThrottle])
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    search_fields = ['Category__title']
    ordering_fields = ['price', 'inventory']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

@throttle_classes([UserRateThrottle])
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
     
'''@api_view(['GET', 'POST'])
@permission_classes([IsManager])
@throttle_classes([AnonRateThrottle])
def groupManagers(request):
    managers = Group.objects.get(name='Managers')
    if(request.method == 'GET' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        users = managers.user_set.all()
        result = ''
        for user in users:
            result += '[id: '
            result += str(user.id)
            result += ', '
            result += user.username
            result += ', '
            result += user.email    
            result += '], '
        return Response({'message' : result}, status=200) 
    
    elif (request.method=='POST' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        managers.user_set.add(user)
        return Response({'message' : 'ok'}, status=201)
    
    return Response({'message':'not authorize'} ,status=403)

@api_view(['DELETE'])
@permission_classes([IsManager])
@throttle_classes([AnonRateThrottle])
def deletegroupManagers(request, pk=None):
    if(request.method=='DELETE' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        managers = Group.objects.get(name='Managers')
        user = get_object_or_404(User, pk=pk)
        managers.user_set.remove(user)
        return Response({'message' : 'ok'}, status=200)
    
    return Response({'message':'not authorize'} ,status=403)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle])
def groupDelivery(request):
    deliveries = Group.objects.get(name='Delivery_Crew')
    if(request.method == 'GET' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        users = deliveries.user_set.all()
        result = ''
        for user in users:
            result += '[id: '
            result += str(user.id)
            result += ', '
            result += user.username
            result += ', '
            result += user.email  
            result += '], '
        return Response({'message' : result}, status=200) 
    
    elif (request.method=='POST' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        deliveries.user_set.add(user)
        return Response({'message' : 'ok'}, status=201)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([AnonRateThrottle])
def deletegroupDelivery(request, pk=None):
    if (request.method=='DELETE' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        deliveries = Group.objects.get(name='Delivery_Crew')
        user = get_object_or_404(User, pk=pk)
        deliveries.user_set.remove(user)
        return Response({'message' : 'ok'}, status=200)'''
    
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def cartMangement(request):
    if(request.method=='GET'):
        items = Cart.objects.filter(user=request.user.id).all()
        serialize_item = CartSerializer(items, many=True)
        return Response(serialize_item.data, status=200)
    
    elif(request.method=='POST'):
        user = User.objects.get(pk=request.user.id)
        menuitem_id = request.POST.get('menuitem_id')       
        menuitem = MenuItem.objects.get(pk=menuitem_id)
        quantity = request.POST.get('quantity')
        unit_price = menuitem.price
        price = float(quantity) * float(unit_price)
        
        cart = Cart(
            user = user,
            menuitem = menuitem,
            quantity = quantity,
            unit_price = unit_price,
            price = price
        )
        try: 
            cart.save()
        except IntegrityError:
            return Response({'message':'required field missing'}, status=400)
        return Response(model_to_dict(cart), status=200)

    elif(request.method=='DELETE'):
        try:
            Cart.objects.filter(user=request.user.id).delete()
            return Response({'message':'object deleted'}, status=200)
        except:
            return Response({'message':'error'}, status=400)
    return None

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def order(request):
    if(request.method == 'GET'):
        perpage = request.query_params.get('perpage',default=10)
        page = request.query_params.get('page',default=1)
        
        if(User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
            items = Order.objects.all()
            
            paginator = Paginator(items,per_page=perpage)
            try:
                items= paginator.page(number=page)
            except EmptyPage:
                items = []
        
        elif(User.objects.filter(pk=request.user.id, groups__name='Delivery_Crew').exists()):
            items = Order.objects.filter(delivery_crew=request.user.id).all()
            
            paginator = Paginator(items,per_page=perpage)
            try:
                items= paginator.page(number=page)
            except EmptyPage:
                items = []
        
        else:
            items = Order.objects.filter(user=request.user.id).all()
        
            paginator = Paginator(items,per_page=perpage)
            try:
                items= paginator.page(number=page)
            except EmptyPage:
                items = []
            
        serialize_item = OrderSerializer(items, many=True)
        orderItems = []
        for x in serialize_item.data:
            orderItems += OrderItem.objects.filter(order=x['id']).all()
        serialize_Orderitems = OderItemSerializer(orderItems, many=True)    
        return Response({'orders' : serialize_item.data, 'order items' : serialize_Orderitems.data}, status=200)
    
    elif(request.method=='POST'):
        #Get all items in the cart
        itemsInCart = Cart.objects.filter(user=request.user.id).all()
        serialize_item = CartSerializer(itemsInCart, many=True)
        #Sum the prices fro total
        total = 0
        for item in serialize_item.data:
            total += float(item['price'])
        #Get cuurent time
        now = timezone.now()
        order = Order(
            user = User.objects.get(pk=request.user.id),
            delivery_crew = None,
            status = False,
            total = total,
            date = now,
        )
        try: 
            order.save()
        except IntegrityError:
            return Response({'message':'required field missing'}, status=400)
        for ids in serialize_item.data:
            orderItems = OrderItem(
                order = Order.objects.get(pk=order.id),
                menuitem = MenuItem.objects.get(pk=ids['menuitem']),
                quantity = ids['quantity'],
                unit_price = ids['unit_price'],
                price = ids['price'],
            )
            try: 
                orderItems.save()
            except Exception as e:
                return Response({'message':e.args}, status=400)
        itemsInCart = Cart.objects.filter(user=request.user.id).all().delete()
        
        return Response({'message':'order created'},status=201)

@api_view(['GET', 'PATCH','DELETE'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def singleorder(request, pk=None):
    if(request.method=='GET'):
        itemsID = get_object_or_404(Order, id=pk)
        items = Order.objects.filter(id=pk)
        ob_id = itemsID.user.id
        serialize_item = OrderSerializer(items, many=True)
        if(request.user.id == ob_id or User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
            orderItems = []
            for x in serialize_item.data:
                orderItems += OrderItem.objects.filter(order=x['id']).all()
            serialize_Orderitems = OderItemSerializer(orderItems, many=True)
            return Response({'orders' : serialize_item.data, 'order items' : serialize_Orderitems.data}, status=200)
        else:
            return Response({'message':'not authorize'}, status=403)
    
    elif(request.method=='PATCH' and User.objects.filter(pk=request.user.id, groups__name='Delivery_Crew').exists()):
        itemsID = get_object_or_404(Order, id=pk)
        ob_id = itemsID.delivery_crew.id
        if(request.user.id == ob_id):
            status = request.POST.get('status')
            order = Order.objects.get(id=pk)
            order.status = status
            order.save()
            return Response({'message':'order updated'})
        else:
            return Response({'message':'Not in current order'})
    
    elif(request.method=='PATCH' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        deliveryID = request.POST.get('delivery_id')
        deliveries = Group.objects.get(name='Delivery_Crew')
        item = get_object_or_404(Order, id=pk)
        try:
            item.delivery_crew = deliveries.user_set.get(pk=deliveryID)
        except Exception as e:
            return Response({'message':e.args}, status=400)     
        item.save()
        return Response({'message':'order updated'})
    
    elif(request.method=='DELETE' and User.objects.filter(pk=request.user.id, groups__name='Managers').exists()):
        try:
            x = Order.objects.filter(id=pk)
            if(not x.exists()):
                return Response({'message':["No Order matches the given query."]},status=400)
            s = OrderSerializer(x, many=True)
            for z in s.data:
                OrderItem.objects.filter(order=z['id']).delete()
            x.delete()
            return Response({'message':'object deleted'}, status=200)
        except Exception as e:
            return Response({'message':e.args}, status=400)
    
    else:
        return Response({'message':'not authorize'}, status=403)
    
@throttle_classes([UserRateThrottle])
class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Managers')
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Managers")
        managers.user_set.add(user)
        return Response({"message": "user added to the manager group"}, 200)

    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Managers")
        managers.user_set.remove(user)
        return Response({"message": "user removed from the manager group"}, 200)

@throttle_classes([UserRateThrottle])
class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Delivery_Crew')
        items = UserSerilializer(users, many=True)
        return Response(items.data)

    def create(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Managers').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery_Crew")
        dc.user_set.add(user)
        return Response({"message": "user added to the delivery crew group"}, 200)

    def destroy(self, request):
        #only for super admin and managers
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name='Managers').exists() == False:
                return Response({"message":"forbidden"}, status.HTTP_403_FORBIDDEN)
        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name="Delivery_Crew")
        dc.user_set.remove(user)
        return Response({"message": "user removed from the delivery crew group"}, 200)
