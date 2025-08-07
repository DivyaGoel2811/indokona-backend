from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from myapp.serializers import UserRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# 👤 Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🔐 Custom JWT Token View
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 📊 Authenticated Dashboard View
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.user.role
        dashboards = {
            'customer': {'welcome': 'Customer Dashboard'},
            'connector_partner': {'welcome': 'Connector Partner Dashboard'},
            'retailer': {'welcome': 'Retailer Dashboard'},
            'distributor': {'welcome': 'Distributor Dashboard'},
            'master_distributor': {'welcome': 'Master Distributor Dashboard'},
            'super_distributor': {'welcome': 'Super Distributor Dashboard'},
            'franchise': {'welcome': 'Franchise Dashboard'},
            'b2b_panel': {'welcome': 'B2B Panel Dashboard'},
        }
        return Response(dashboards.get(role, {'welcome': 'Default Dashboard'}))

# ✅ NEW: User Login View for /api/login2/
class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ NEW: Get Role View for /api/get-role/
class GetUserRole(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"role": request.user.role})
