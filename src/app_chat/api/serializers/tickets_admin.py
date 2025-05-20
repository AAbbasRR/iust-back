from django.utils.translation import gettext_lazy as _

from rest_framework import serializers, exceptions

from app_chat.models import (
    ChatRoomModel,
    MessageModel,
)

from utils.base_errors import BaseErrors


class AdminMessageSerializers(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField("get_file_url")
    user_owner = serializers.SerializerMethodField("get_user_owner")

    chatroom_id = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = MessageModel
        fields = [
            "id",
            "message",
            "created_at",
            "file_url",
            "user_owner",
            "file",
            "chatroom_id",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "message": {"required": False, "allow_blank": True},
            "file": {"required": False, "allow_null": True, "write_only": True},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def validate_chatroom_id(self, value):
        chatroom_obj = ChatRoomModel.objects.filter(pk=value).first()
        if chatroom_obj:
            return chatroom_obj
        else:
            raise exceptions.NotFound(
                BaseErrors._change_error_variable(
                    "object_not_found", object=_("Chat Room")
                )
            )

    def get_file_url(self, obj):
        return obj.get_file_url(self.request)

    def get_user_owner(self, obj):
        return True if self.user == obj.user else False

    def create(self, validated_data):
        chat_room_obj = validated_data.pop("chatroom_id")
        message_obj = MessageModel.objects.create(
            chat_room=chat_room_obj, user=self.user, **validated_data
        )
        chat_room_obj.status = ChatRoomModel.ChatRoomStatusOptions.Has_Been_Answered
        chat_room_obj.admin = self.user
        chat_room_obj.save()
        return message_obj


class AdminTicketChatRoomSerializers(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField("get_latest_message")

    class Meta:
        model = ChatRoomModel
        fields = [
            "id",
            "title",
            "room_id",
            "status",
            "priority",
            "created_at",
            "updated_at",
            "latest_message",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "title": {"required": True},
            "priority": {"required": True},
            "status": {"read_only": True},
            "room_id": {"read_only": True},
            "create_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(AdminTicketChatRoomSerializers, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def get_latest_message(self, obj):
        return AdminMessageSerializers(
            obj.chatroom_messages.last(),
            many=False,
            read_only=True,
            context=self.context,
        ).data


class AdminChatRoomRetrieveSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField("get_messages")
    can_close = serializers.SerializerMethodField("get_can_close")

    class Meta:
        model = ChatRoomModel
        fields = [
            "id",
            "title",
            "room_id",
            "status",
            "priority",
            "created_at",
            "messages",
            "can_close",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "title": {"read_only": True},
            "room_id": {"read_only": True},
            "status": {"read_only": True},
            "priority": {"read_only": True},
            "create_at": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(AdminChatRoomRetrieveSerializer, self).__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def get_messages(self, obj):
        return AdminMessageSerializers(
            obj.chatroom_messages.all().order_by("create_at"),
            many=True,
            context=self.context,
        ).data

    def get_can_close(self, obj):
        return obj.admin == self.user


class AdminCloseTicketSerializers(serializers.Serializer):
    chatroom_id = serializers.CharField(required=True, write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request")
        if self.request:
            self.user = self.request.user

    def validate_chatroom_id(self, value):
        chatroom_obj = self.user.user_chat_rooms.filter(pk=value).first()
        if chatroom_obj:
            return chatroom_obj
        else:
            raise exceptions.NotFound(
                BaseErrors._change_error_variable(
                    "object_not_found", object=_("Chat Room")
                )
            )

    def validate(self, attrs):
        attrs["chatroom_id"].status = ChatRoomModel.ChatRoomStatusOptions.Closed
        attrs["chatroom_id"].save()
        return attrs
