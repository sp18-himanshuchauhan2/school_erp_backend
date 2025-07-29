from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ..serializers import CustomTokenObtainPairSerializer
from utils.restful_response import send_response
from utils.data_constants import ResponseMessages
from rest_framework import status


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return send_response(
                data=serializer.validated_data,
                message=ResponseMessages.AUTH_SUCCESS,
                status_code=status.HTTP_200_OK
            )
        except Exception:
            return send_response(
                data={"detail": "Invalid email or password"},
                message=ResponseMessages.AUTH_FAILED,
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            return send_response(
                data=serializer.validated_data,
                message=ResponseMessages.TOKEN_REFRESH_SUCCESS,
                status_code=status.HTTP_200_OK
            )
        except Exception:
            return send_response(
                data={"detail": "Refresh token is invalid or expired"},
                message=ResponseMessages.INVALID_REFRESH_TOKEN,
                status_code=status.HTTP_401_UNAUTHORIZED
            )

