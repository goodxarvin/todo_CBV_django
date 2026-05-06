from celery import shared_task
from django.contrib.auth import get_user_model
from mail_templated import send_mail, EmailMessage

user = get_user_model()


@shared_task
def send_email_verification_worker(username, access_token):

        email_object = EmailMessage(
            subject="send verification email",
            template_name="mail/verification.tpl",
            context={"name": username, "access_token": access_token},
            from_email="from@a.aa",
            to=[
                f"{username}@send.com",
            ],
        )
        email_object.send()
        print("email sent successfully")
    
@shared_task
def resend_email_verification_worker(username, access_token):

        email_object = EmailMessage(
            subject="resend verification email",
            template_name="mail/verification.tpl",
            context={"name": username, "access_token": access_token},
            from_email="from@a.aa",
            to=[
                f"{username}@resend.com",
            ],
        )
        email_object.send()
        print("email resent successfully")

@shared_task
def forgot_password_email_worker(username, access_token):

    email_object = EmailMessage(
        subject="forgot password email",
        template_name="mail/forgot_password.tpl",
        context={"name": username, "access_token": access_token},
        from_email="from@a.aa",
        to=[
            f"{username}@forgot.com",
        ],
    )
    email_object.send()
    print("forgot email sent successfully")