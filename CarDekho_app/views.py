from django.shortcuts import render
from . models import Carlist,Showroomlist
# from django.http import JsonResponse,HttpResponse
# import json
from .app_file.serializer import CarSerializers,ShowroomSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# def car_list_view(request):
#     cars = Carlist.objects.all()
#     data = {
#         'cars':list(cars.values()),
#     }
#     # return JsonResponse(data)
#     data_json = json.dumps(data)
#     return HttpResponse (data_json,content_type="application/json")

# def car_detail_view(request,pk):
#     car = Carlist.objects.get(pk=pk)
#     data ={
#         'car': car.name,
#         'description': car.description,
#         'active': car.active
#     }
#     return JsonResponse(data)

class showroom_view(APIView):
       
       authentication_classes = [BasicAuthentication]
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
                  return Response(serializer.data, status=201)
              
              else:
                     return Response(serializer.errors, status=400)
       return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'PUT','DELETE'])

def car_detail_view(request,pk):
       
       if request.method == 'GET':
              try :
                     car = Carlist.objects.get(pk=pk)
              except:
                     return Response({'Error':'Car not Found'},status=status.HTTP_404_NOT_FOUND)
              serializer = CarSerializers(car)
              return Response(serializer.data)
       if request.method == 'PUT':
              car = Carlist.objects.get(pk=pk)
              serializer = CarSerializers(car, data=request.data)
              if serializer.is_valid():
                     serializer.save()
                     return Response(serializer.data)
              else:
                      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
       
       if request.method == 'DELETE':
              car = Carlist.objects.get(pk=pk)
              car.delete()
              return Response(status=status.HTTP_204_NO_CONTENT)
       return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)