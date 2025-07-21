from django.utils.translation import gettext_lazy as _

from rest_framework import generics, exceptions, response, status

from app_chat.api.serializers.tickets_admin import (
    AdminMessageSerializers,
    AdminEditMessageSerializers,
    AdminTicketChatRoomSerializers,
    AdminChatRoomRetrieveSerializer,
    AdminCloseTicketSerializers,
)
from app_chat.models import ChatRoomModel, MessageModel
from app_chat.filters.tickets import AdminTicketListFilter

from utils.permissions import (
    IsAuthenticatedPermission,
    IsAdminUserPermission,
    IsSuperUserPermission,
)
from utils.base_errors import BaseErrors
from utils.versioning import BaseVersioning
from utils.paginations import BasePagination


class AdminListTicketView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminTicketChatRoomSerializers
    search_fields = ["title", "room_id"]
    filterset_class = AdminTicketListFilter
    queryset = ChatRoomModel.objects.all()


class AdminRetrieveTicketMessagesView(generics.RetrieveAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminChatRoomRetrieveSerializer
    filterset_class = AdminTicketListFilter
    queryset = ChatRoomModel.objects.all()
    lookup_field = "pk"

    def get_object(self):
        pk_param_value = self.request.GET.get(self.lookup_field, None)
        if pk_param_value is None or pk_param_value == "":
            raise exceptions.ParseError(
                BaseErrors._change_error_variable(
                    "parameter_is_required", param_name="pk"
                )
            )
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.filter(pk=pk_param_value).first()
        if obj is None:
            raise exceptions.NotFound(
                BaseErrors._change_error_variable(
                    "object_not_found", object=_("Ticket")
                )
            )
        return obj


class AdminCreateMessageOnChatRoomView(generics.CreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminMessageSerializers

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return response.Response(
                AdminMessageSerializers(
                    instance=message, many=False, context={"request": request}
                ).data,
                status=status.HTTP_201_CREATED,
            )


class AdminEditMessageOnChatRoomView(generics.UpdateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminEditMessageSerializers
    lookup_field = "pk"

    def get_queryset(self):
        return MessageModel.objects.filter(user=self.request.user)


class AdminCloseTicketView(generics.CreateAPIView):
    permission_classes = [
        IsAuthenticatedPermission,
        IsAdminUserPermission,
        IsSuperUserPermission,
    ]
    versioning_class = BaseVersioning
    serializer_class = AdminCloseTicketSerializers

    def perform_create(self, serializer):
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return response.Response({"message": "ticket room closed"})
