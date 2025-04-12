from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        

        
        user = authenticate(request, email=email, password=password)  

        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "status": "success",
                "message": "Usuario autenticado correctamente",
                "data": {
                    "token": access_token,
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id_card,
                        "name": user.name,
                        "email": user.email
                    }
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Credenciales inválidas"
        }, status=status.HTTP_401_UNAUTHORIZED)
