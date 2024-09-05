from django.shortcuts import render
from . models import Carlist,Showroomlist
from .app_file.serializer import CarSerializers,ShowroomSerializer,ReviewSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .app_file.permission import  AdminOrReadOnlyPermission,RevieUserOrReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from rest_framework import mixins
from rest_framework import generics
from .models import Review
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
from.app_file.throttling import ReviewDetailThrottle,ReviewListThrottle
from.app_file.pagination import Reviewlistpagiation,ReviewListlimitoffpag


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')  # Safer to use .get() to avoid KeyError
        car = Carlist.objects.get(pk=pk) 
        user = self.request.user 
        review_queryset = Review.objects.filter(car=car, user=user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this car")
        
        serializer.save(car=car, user=user)
        
class Reviewlist(generics.ListAPIView):
       serializer_class = ReviewSerializer
       authentication_classes = [TokenAuthentication]
       # authentication_classes = [JWTAuthentication]
#      permission_classes = [IsAuthenticated,]
       # throttle_classes = [ReviewListThrottle,AnonRateThrottle]
       pagination_class = ReviewListlimitoffpag
    
       def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Review.objects.filter(car=pk)

       
class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
       queryset = Review.objects.all()
       serializer_class = ReviewSerializer
       permission_classes = [RevieUserOrReadOnly]
       authentication_classes = [TokenAuthentication]
       # throttle_classes = [ReviewDetailThrottle,AnonRateThrottle]


# ------------------------------------------------------------------------MIXINS----------------------------------------------------------------

# class ReviewDetails(mixins.RetrieveModelMixin,generics.GenericAPIView):
#        queryset = Review.objects.all()
#        serializer_class = ReviewSerializer
       
#        authentication_classes = [SessionAuthentication]
#        permission_classes = [DjangoModelPermissions]
       
       
       
#        def get(self, request, *args, **kwargs):
#               return self.retrieve(request, *args, **kwargs)
       

# class Reviewlist(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#        queryset = Review.objects.all()
#        serializer_class = ReviewSerializer

#        def get(self, request, *args, **kwargs):
#               return self.list(request, *args, **kwargs)

#        def post(self, request, *args, **kwargs):
#               return self.create(request, *args, **kwargs)
       
             
#  ===========================================================CLASSBASE========================================================================      



class Showroom_Viewset(viewsets.ModelViewSet):
       
       queryset = Showroomlist.objects.all()
       serializer_class = ShowroomSerializer

class showroom_view(APIView):
       
       authentication_classes = [SessionAuthentication]
       permission_classes = [IsAuthenticated]
       
       
       
       
       def get(self, request):
              cars = Showroomlist.objects.all()
              serializer = ShowroomSerializer(cars, many=True)
              return Response(serializer.data)
       
       
       def post(self, request):
              serializer = ShowroomSerializer(data=request.data)
              if serializer.is_valid():
                  serializer.save()
                  return Response(serializer.data, status=201)

              else:
                     return Response(serializer.errors, status=400)
       
class Showroom_Details(APIView):
       def get(self, request, pk):
              try :
                     showroom = Showroomlist.objects.get(pk=pk)
              except:
                     return Response({'Error':'Car not Found'}, status=status.HTTP_404_NOT_FOUND)
              serializer = ShowroomSerializer(showroom)
              return Response(serializer.data)
       
       def put(self, request, pk):
              showroom = Showroomlist.objects.get(pk=pk)
              serializer = ShowroomSerializer(showroom, data=request.data)
              if serializer.is_valid():
                     serializer.save()
                     return Response(serializer.data)
              else:
                      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       def delete(self, request, pk):
              showroom = Showroomlist.objects.get(pk=pk)
              showroom.delete()
              return Response(status=status.HTTP_204_NO_CONTENT)
       
       
       
# ------------------------------------------------------------------------FUNCTIONBASE----------------------------------------------------------------------------------
       
@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method == 'GET':
        cars = Carlist.objects.all()
        serializer = CarSerializers(cars, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CarSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT', 'DELETE'])
def car_detail_view(request, pk):
    try:
        car = Carlist.objects.get(pk=pk)
    except Carlist.DoesNotExist:
        return Response({'Error': 'Car not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CarSerializers(car)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CarSerializers(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)