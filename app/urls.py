# urls.py
from django.urls import path
from .views import UserRegistrationView, OrganizationRegistrationView , UserLoginView , OrganizationLoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', UserRegistrationView.as_view(), name='user-register'),
    path('organization/register/', OrganizationRegistrationView.as_view(), name='organization-register'),
    path('user/login/' , UserLoginView.as_view() , name = 'user-login'),
    path('organization/login/' , OrganizationLoginView.as_view() , name = 'org-login'),

]

