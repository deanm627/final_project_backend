from django.urls import path
from . import views

urlpatterns = [
    path('meds/', views.MedListView.as_view(), name='med-list'),
    path('meds/<int:pk>/', views.MedDetailView.as_view(), name='med-detail'),
]