from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Organization, User
from .serializers import UserRegistrationSerializer, OrganizationRegistrationSerializer


class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OrganizationRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Hash the organization password
            password = serializer.validated_data.pop('password')
            organization = Organization(**serializer.validated_data)
            organization.password = make_password(password)
            organization.save()
            return Response({'message': 'Organization registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user_type': 'user',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'User login successful'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password for user'}, status=status.HTTP_401_UNAUTHORIZED)


class OrganizationLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            organization = Organization.objects.get(email=email)
            if check_password(password, organization.password):  # Compare hashed password
                return Response({
                    'user_type': 'organization',
                    'message': 'Organization login successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid email or password for organization'}, status=status.HTTP_401_UNAUTHORIZED)
        except Organization.DoesNotExist:
            return Response({'error': 'Invalid email or password for organization'}, status=status.HTTP_401_UNAUTHORIZED)
