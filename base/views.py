# from django.shortcuts import render
from datetime import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from djoser.views import TokenCreateView as BaseTokenCreateView
# Create your views here.
class TokenCreateView(BaseTokenCreateView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(f"Validated data: {serializer.validated_data}")
        user = serializer.user
        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response({"access": access_token, "refresh": refresh_token}, status=status.HTTP_200_OK)
        access_token = response.data['access']
        refresh_token = response.data['refresh']

        dt_now = datetime.utcnow()
        access_token_expiry = dt_now + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_expiry = dt_now + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        # Convert the datetime object to a string formatted for cookies (RFC 1123)
        access_expiry_str = access_token_expiry.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
        refresh_expiry_str = refresh_token_expiry.strftime('%a, %d-%b-%Y %H:%M:%S GMT')

        response.set_cookie(
            settings.SIMPLE_JWT['ACCESS_COOKIE_KEY'],
            value=access_token,
            expires = access_expiry_str,
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )

        response.set_cookie(
            settings.SIMPLE_JWT['REFRESH_COOKIE_KEY'],
            value=refresh_token,
            expires = refresh_expiry_str,
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        )

        return response