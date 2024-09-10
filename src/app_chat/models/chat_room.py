from django.db import models
from django.utils.translation import gettext_lazy as _

from Abrat.settings import DEBUG
from app_user.models import UserModel

from utils.general_models import GeneralDateModel


class ChatRoomManager(models.Manager):
    pass


class ChatRoom(GeneralDateModel):
    class Meta:
        ordering = ["-create_at"]

    class ChatRoomPriorityOptions(models.TextChoices):
        LOW = "LOW", _("LOW")
        Medium = "Medium", _("Medium")
        High = "High", _("High")

    class ChatRoomStatusOptions(models.TextChoices):
        Waiting_For_An_Answer = "Waiting_For_An_Answer", _("Waiting For An Answer")
        Has_Been_Answered = "Has_Been_Answered", _("Has Been Answered")
        Closed = "Closed", _("Closed")

    title = models.CharField(max_length=75, verbose_name=_("Title"))
    user = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="user_chat_rooms",
        verbose_name=_("User"),
    )
    admin = models.ForeignKey(
        UserModel,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="admin_chat_rooms",
        verbose_name=_("Admin"),
    )
    room_id = models.CharField(
        max_length=250, blank=True, null=True, verbose_name=_("Room Id")
    )
    status = models.CharField(
        max_length=21,
        choices=ChatRoomStatusOptions.choices,
        default=ChatRoomStatusOptions.Waiting_For_An_Answer,
        verbose_name=_("Status"),
    )
    priority = models.CharField(
        max_length=6,
        choices=ChatRoomPriorityOptions.choices,
        default=ChatRoomPriorityOptions.LOW,
        verbose_name=_("Priority"),
    )

    objects = ChatRoomManager()


def ticket_image_directory_path(instance, filename):
    return "chat_images/{0}/{1}".format(instance.chat_room.room_id, filename)


class Message(GeneralDateModel):
    class Meta:
        ordering = ["-create_at"]

    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="chatroom_messages",
        verbose_name=_("Chat Room"),
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_messages",
        verbose_name=_("User"),
    )
    message = models.TextField(null=True, blank=True, verbose_name=_("Message"))
    file = models.FileField(
        upload_to=ticket_image_directory_path, verbose_name=_("Image")
    )

    def get_file_url(self, request):
        if self.file is None or self.file == "":
            return None
        else:
            host = request.get_host()
            protocol = request.build_absolute_uri().split(host)[0]
            protocol = (
                protocol
                if DEBUG
                else protocol.replace("http", "https")
                if protocol.split(":")[0] == "http"
                else protocol
            )
            website_url = protocol + host
            return website_url + self.file.url
