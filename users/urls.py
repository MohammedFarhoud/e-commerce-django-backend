from django.urls import path
from users.views import ContactUsView
from users.views import Registeration, UserDetail
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
    path('git/', Registeration.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserDetail.as_view(), name='user_detail'),
    path('contactus/', ContactUsView.as_view(), name='contact_us'),
]
