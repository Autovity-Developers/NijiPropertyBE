from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from pyotp import otp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserOTP
import base64
from django.conf import settings
from django.core.mail import send_mail

# This class returns the string needed to generate the key


def generateKey(email,user):
    return str(email) + str(datetime.date(datetime.now())) + settings.SECRET_KEY


def send_otp(user, email):
    try:
        otp_obj = UserOTP.objects.get(user=user)
    except ObjectDoesNotExist:
        otp_obj = UserOTP.objects.create(
            user=user,
        )
    otp_obj.counter = otp_obj.counter + 1
    otp_obj.save()

    key = base64.b32encode(generateKey(
        email, user).encode())

    hotp = pyotp.HOTP(key)
    otp = hotp.at(otp_obj.counter)
    otp_obj.otp_code = otp
    otp_obj.save()
    try:
        message = "Your OTP Code for validation is " + str(otp)
        send_mail(
            'OTP code',
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print('unable to send mail')
        return False


def verify_otp(user, email, otp_code):
    try:
        otp_obj = UserOTP.objects.get(user=user)
    except ObjectDoesNotExist:
        return False
    print(otp_obj.otp_code, otp_code)
    if otp_code == otp_obj.otp_code:
        return True

    return False
