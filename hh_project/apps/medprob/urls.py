from django.urls import path
from . import views

urlpatterns = [
    path('bp/', views.BPSummaryView.as_view(), name='bp-home'),
    path('bps/', views.BPListView.as_view(), name='bp-list'),
    path('bps/<int:pk>/', views.BPDetailView.as_view(), name='bp-detail'),
]