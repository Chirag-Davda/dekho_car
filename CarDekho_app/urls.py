from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import car_detail_view, car_list_view

# Register viewsets with the router
router = DefaultRouter()
router.register('showroom', views.Showroom_Viewset)

urlpatterns = [
    # Non-router paths for car list and detail views
    path('cars/', car_list_view, name='car_list'),  # Ensure this matches the endpoint you're trying to access
    path('cars/<int:pk>/', car_detail_view, name='car_detail'),
    # Include the router URLs
    path('', include(router.urls)),

    # Showroom specific paths
    path('showroom/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('showroom/<int:pk>/review/', views.Reviewlist.as_view(), name='review-list'),
    path('showroom/review/<int:pk>/', views.ReviewDetails.as_view(), name='review-detail'),
]
