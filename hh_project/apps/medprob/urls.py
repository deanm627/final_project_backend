from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'bps', views.BPViewSet, basename="bp")

# urlpatterns = [
#     path('', include(router.urls))
# ]

urlpatterns = [
    path('bps/', views.BPView.as_view(), name = 'bp-list')
]