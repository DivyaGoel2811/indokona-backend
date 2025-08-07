from django.urls import path
from myapp.views import (
    RegisterView,
    MyTokenObtainPairView,
    DashboardView,
    UserLoginView,
    GetUserRole
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # ✅ Add these for frontend login system
    path('login2/', UserLoginView.as_view(), name='custom_login'),
    path('get-role/', GetUserRole.as_view(), name='get_user_role'),
]
