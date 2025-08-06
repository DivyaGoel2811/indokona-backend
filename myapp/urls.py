
from django.urls import path
from myapp.views import RegisterView, MyTokenObtainPairView, DashboardView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]
