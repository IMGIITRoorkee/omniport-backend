from django.urls import path

from base_auth.views.reset_password import ResetPassword
from base_auth.views.verify_secret_answer import VerifySecretAnswer
from base_auth.views.recover_passowrd import RecoverPassword, VerifyRecoveryToken

app_name = 'base_auth'

urlpatterns = [
    path(
        'verify_secret_answer/',
        VerifySecretAnswer.as_view(),
        name='verify_secret_answer'
    ),
    path(
        'reset_password/',
        ResetPassword.as_view(),
        name='reset_password'
    ),
    path(
        'recover_password/',
        RecoverPassword.as_view(),
        name='password recovery'
    ),
    path(
        'verify/',
        VerifyRecoveryToken.as_view(),
        name='verify_recovery_token'
    ),
]
