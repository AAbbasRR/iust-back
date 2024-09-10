from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.utils import IntegrityError

from app_chat.models import ChatRoomModel, MessageModel
from app_user.models import UserModel

from utils.classes import ManageMailService

import uuid


@receiver(post_save, sender=ChatRoomModel)
def create_ticket_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        while True:
            try:
                instance.room_id = str(uuid.uuid4()).split("-")[-1]
                instance.save()
                break
            except IntegrityError:
                pass
        superusers = UserModel.objects.filter(is_superuser=True)
        for user in superusers:
            superuser_mail = ManageMailService(user.email)
            user = instance.user
            superuser_mail.send_email_to_user(
                subject="تیکت جدید",
                content={
                    "title": "message",
                    "data": {
                        "title": f"یک تیکت جدید ایجاد شده است.",
                        "description": f"یک تیکت جدید از {user.user_profile.get_full_name()} با ایمیل {user.email} با موضوع {instance.title} ایجاد شده است. ",
                    },
                },
            )


@receiver(post_save, sender=MessageModel)
def create_ticket_message_handler(sender, instance, **kwargs):
    if kwargs["created"]:
        superuser = instance.chat_room.admin
        if superuser is not None:
            superuser_mail = ManageMailService(superuser.email)
            user = instance.user
            superuser_mail.send_email_to_user(
                subject="پیام جدید",
                content={
                    "title": "message",
                    "data": {
                        "title": f"یک پیام جدید ایجاد شده است.",
                        "description": f"یک پیام جدید از تیکت {user.user_profile.get_full_name()} با ایمیل {user.email} با موضوع {instance.title} ایجاد شده است. ",
                    },
                },
            )
