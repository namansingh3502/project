from django.urls import path, include

from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path("check_2fa", views.check_2fa, name="sign-in"),
    path(r'generate_sha_key/<str:key_type>', views.generate_ssh_key, name="Generate_SSH_Key"),
    path('validate_otp/', views.validate_totp, name="Validate_TOTP"),

    path('user_regisration/', views.register_user, name="User_Registration"),
    path('generate_email_verification/', views.generate_email_verification, name="Email_Verification"),
    path('verify_email/<uidb64>/<token>/', views.email_verification, name="Mobile_Verification"),
    path('generate_mobile_verification_otp/', views.generate_mobile_otp, name="Mobile_Verification"),
    path('user_mobile_verification/', views.mobile_verification, name="Mobile_Verification"),
]
