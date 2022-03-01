from django.db.models import Q
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .models import *
import jwt, datetime

# Create your views here.
class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class login(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt": token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithm='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializers = UserSerializer(user)
        return Response(serializers.data)

class Logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})

@api_view(['POST', 'GET'])
def checkout(request):
    token = request.headers.get('Authorization')
    payload = jwt.decode(token, 'secret', algorithms='HS256')
    request.data['user'] = payload['id']
    request.data['first_name'] = User.objects.values_list('first_name', flat=True).get(pk=payload['id'])
    request.data['last_name'] = User.objects.values_list('last_name', flat=True).get(pk=payload['id'])
    request.data['username'] = User.objects.values_list('username', flat=True).get(pk=payload['id'])
    request.data['email'] = User.objects.values_list('email', flat=True).get(pk=payload['id'])
    request.data['phone_number'] = User.objects.values_list('phone_number', flat=True).get(pk=payload['id'])
    serializer = OrderSerializer(data=request.data)
    if not token:
        return Response({'message':'unauthenticated','explanation':'Your are not logged in or the token expired'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        try:
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError:
        return Response('Unauthenticated', status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

#             try:
                # charge = stripe.Charge.create(
                #     amount=int(paid_amount * 100),
                #     currency='USD',
                #     description='Charge from Djackets',
                #     source=serializer.validated_data['stripe_token']
                # )

            #     serializer.save(user=request.user, paid_amount=paid_amount)

class OrdersList(APIView):
    def get(self, request, format=None):
        token = request.headers.get('Authorization')
        payload = jwt.decode(token, 'secret', algorithms='HS256')
        if not token:
            return Response('unauthenticated', status=status.HTTP_400_BAD_REQUEST)
        else:
            orders = Order.objects.filter(user=payload['id'])
            serializer = MyOrderSerializer(orders, many=True)
            return Response(serializer.data)
