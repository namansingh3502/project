import base64
import secrets
import string

import pyotp
from coreapi.compat import force_text
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from djoser.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from twilio.rest import Client

from .forms import RegistrationForm
from .models import *
from .tokens import *

alphabet = string.ascii_letters + string.digits

account_sid = ""
auth_token = ""
verify_sid = ""

KEY_SIZE = {
    "SHA1": 20,
    "SHA256": 32,
    "SHA512": 64
}


@csrf_exempt
def sign_in(request):
    username = request.POST["username"]
    password = request.POST["password"]
    platform = request.POST["platform"]

    user = authenticate(request, username=username, password=password)
    token, _ = settings.TOKEN_MODEL.objects.get_or_create(user=user)
    if user is None:
        return JsonResponse({"msg": "Username or password incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        platform = Platform.objects.get(name=platform)
        user_platform = UserTOTPDetails.objects.get(user=user, platform=platform, is_active=True)
    except Platform.DoesNotExist:
        return JsonResponse({"msg": "Platform does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    except UserTOTPDetails.DoesNotExist:
        return JsonResponse({"msg": "2FA not active", "is_active": False, "auth_token": str(token)},
                            status=status.HTTP_200_OK)

    return JsonResponse({"msg": "authenticated", "is_active": True, "auth_token": str(token)},
                        status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_2fa(request):
    try:
        user = UserProfile.objects.get(id=request.user.pk)
    except UserProfile.DoesNotExist:
        return JsonResponse({"msg": "Some error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({"is_2fa_activated": user.is2faActivated}, status=status.HTTP_200_OK)


@api_view(['POST'])
def register_user(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse(
            {'Message': "You are already authenticated."},
            status=status.HTTP_400_BAD_REQUEST
        )

    form = RegistrationForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()

    else:
        return JsonResponse(
            {'msg': form.errors.values()},
            status=status.HTTP_400_BAD_REQUEST
        )

    return JsonResponse(
        {'msg': "User Registration Successful."},
        status=status.HTTP_201_CREATED
    )


@api_view(["get"])
def generate_email_verification(request):
    user = UserProfile.objects.get(pk=request.user.pk)
    try:
        mail_subject = 'Forum Account activation link.'
        message = render_to_string('account_activate_email.html', {
            'user': user,
            'domain': "http://127.0.0.1:1234",
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = request.POST["email"]
        email = EmailMessage(
            mail_subject,
            message,
            to=[to_email]
        )
        email.send()
    except Exception:
        return JsonResponse(
            {"response": "Verification email generation failed"},
            status=status.HTTP_400_BAD_REQUEST
        )

    return JsonResponse(
        {"response": "Verification email sent"},
        status=status.HTTP_200_OK
    )


@api_view(["get"])
def email_verification(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response(
            {'msg': "Email verified."},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {'msg': "Email verification failed."},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["post"])
def generate_mobile_otp(request):
    client = Client(account_sid, auth_token)
    phone_number = request.POST["phone"]

    try:
        verification = client.verify.v2.services(verify_sid).verifications.create(to=phone_number, channel="sms")
    except Exception as e:
        return JsonResponse(
            {"response": "failed to send otp"},
            status=status.HTTP_408_REQUEST_TIMEOUT
        )

    return JsonResponse(
        {"response": "otp sent successfully"},
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def mobile_verification(request):
    client = Client(account_sid, auth_token)
    otp_code = request.POST["otp"]
    phone_number = request.POST["phone"]

    try:
        verification_check = client.verify.v2.services(verify_sid).verification_checks.create(
            to=phone_number,
            code=otp_code
        )
        print("verification_check ", verification_check.status)
    except Exception as e:
        return JsonResponse(
            {"response": "mobile verification failed"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return JsonResponse(
        {"response": "mobile verified"},
        status=status.HTTP_200_OK
    )


@api_view(["post"])
@permission_classes([IsAuthenticated])
def validate_totp(request):
    data = request.data
    is_valid = False
    try:
        platform = Platform.objects.get(name=data["platform"])
        credentials = UserTOTPDetails.objects.get(user_id=request.user.pk, platform=platform)
        key = base64.b32encode(bytearray(credentials.key, 'ascii'))
        totp = pyotp.TOTP(key)
        is_valid = totp.verify(data["totp"])
        if is_valid:
            credentials.is_active = True
            credentials.save()

    except Exception as e:
        return JsonResponse(
            {"msg": "Some error occured"},
            status=status.HTTP_400_BAD_REQUEST
        )
    return JsonResponse(
        {"is_valid": is_valid},
        status=status.HTTP_200_OK
    )


@api_view(["get"])
@permission_classes([IsAuthenticated])
def generate_ssh_key(request, key_type, platform_name):
    """
    :param key_type: type of sha key to be used i.e. SHA1, SHA256, SHA526
    :param request:
    generates a 20 char key alphanumeric secret key
    :return:
    """

    try:
        key_size = KEY_SIZE[key_type]
        sha_key = ''.join(secrets.choice(alphabet) for i in range(key_size))
    except Exception as e:
        return JsonResponse(
            {"Error": "Key type not supported"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = UserProfile.objects.get(pk=request.user.id)
    platform = Platform.objects.get(name=platform_name)

    try:
        UserTOTP = UserTOTPDetails.objects.get(
            user=user,
            platform=platform,
        )
        UserTOTP.key = sha_key
        UserTOTP.save()
    except Exception as e:
        UserTOTP = UserTOTPDetails.objects.create(
            user=user,
            platform=platform,
            delay=0,
            key=sha_key,
            is_active=False
        )
    key = base64.b32encode(bytearray(sha_key, 'ascii'))
    uri = pyotp.totp.TOTP(key).provisioning_uri(name="TOTP Platform", issuer_name=platform_name)

    return JsonResponse(
        {"sha_key": str(key)[2:-1], "uri": str(uri)},
        status=status.HTTP_200_OK
    )
