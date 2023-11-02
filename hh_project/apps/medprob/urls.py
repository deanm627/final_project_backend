from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'bps', views.BPViewSet, basename="bp")

# urlpatterns = [
#     path('', include(router.urls))
# ]

urlpatterns = [
    path('bp/', views.BPSummaryView.as_view(), name='bp-home'),
    path('bps/', views.BPListView.as_view(), name='bp-list'),
    path('bps/<int:pk>/', views.BPDetailView.as_view(), name='bp-detail'),
]