from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from apps.user.views import UserView
from apps.credit_card.views import CreditCardView

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, basename='users')
router.register(r'credit-cards', CreditCardView, basename='credit_cards')

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
]

urlpatterns += router.urls