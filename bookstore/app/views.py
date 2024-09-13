from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import SignupSerializer, Loginserializer, BookSerializer
from .models import books

#signup_page

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes=[AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()     
        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        user_data = SignupSerializer(user).data
          return Response({
            'message': 'Signup successful',
            'user': user_data,
             'access': access_token,
            'refresh': refresh_token
        }, status=status.HTTP_201_CREATED)
        
#login_page

class LoginView(APIView):
    serializer_class = Loginserializer
    permission_classes=[AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
              
            if user is not None:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                
                return Response({
                    'message': 'Login successful',
                    'access': access_token,
                    'refresh': refresh_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# create_books_libary

class CreateBookView(generics.CreateAPIView):
    queryset = books.objects.all()
    serializer_class = BookSerializer
    permission_classes=[IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        book_data = serializer.data
        return Response({
            'message': 'Book created successfully',
            'book': book_data
        }, status=status.HTTP_201_CREATED)
        
#books_detalis_list

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def ListBook(request):
    search= request.query_params.get('search','')
    queryset=books.objects.all()   
     
    if search:
      queryset= queryset.filter(Q(id_icontains='id'))     
    serializer=BookSerializer(queryset,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

#   get_bookinfo_via_id
  
@api_view(['GET'])
@permission_classes([IsAuthenticated])

def book_id(request,id):  
    books_id= books.objects.get(id=id)
    Serializer=BookSerializer(books_id)   
    return Response(Serializer.data,status=status.HTTP_200_OK)


#update_book_record

@api_view(['PUT'])
@permission_classes([IsAuthenticated])

def update_collection(request,id):
        books_id=books.objects.get(id=id)
        serializer=BookSerializer(books_id,data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#delete.books

@api_view(['DELETE'])  
@permission_classes([IsAuthenticated])
 
def delete_records(self, request, id):
    books_id=books.objects.get(id=id)
    books_id.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    
