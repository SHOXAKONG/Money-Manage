from django.contrib.auth import authenticate, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from config import settings
from users.models import User
from users.serializers import LoginSerializer, RegisterSerializer, ForgotPasswordSerializer, RestorePasswordSerializer


class LoginViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'email': user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class ForgotPasswordViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "No user found with this email address"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct reset link
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

        # Send email
        try:
            send_mail(
                subject="Password Reset Request",
                message=f"Please use the following link to reset your password: {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"detail": f"Failed to send email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"detail": "Password reset email sent successfully"},
            status=status.HTTP_200_OK
        )


class RestorePasswordViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = RestorePasswordSerializer

    @action(detail=False, methods=['post'])
    def restore_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password reset successfully"},
            status=status.HTTP_200_OK
        )


class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        logout(request)
        return Response({
            "message": "User Logged Out Successfully"
        }, status=status.HTTP_200_OK)
