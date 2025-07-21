from django.urls import path

from .views import *

app_name = "app_chat"
urlpatterns = [
    # user tickets
    path(
        "list_create/",
        ListCreateTicketView.as_view(),
        name="user_list_create_ticket_chatroom",
    ),
    path(
        "retrieve/",
        RetrieveTicketMessagesView.as_view(),
        name="user_retrieve_ticket_chatroom",
    ),
    path(
        "message/create/",
        CreateMessageOnChatRoomView.as_view(),
        name="user_create_message_chatroom",
    ),
    path(
        "admin/list/",
        AdminListTicketView.as_view(),
        name="admin_list_ticket_chatroom",
    ),
    path(
        "admin/retrieve/",
        AdminRetrieveTicketMessagesView.as_view(),
        name="admin_retrieve_ticket_chatroom",
    ),
    path(
        "admin/message/create/",
        AdminCreateMessageOnChatRoomView.as_view(),
        name="admin_create_message_chatroom",
    ),
path(
        "admin/message/edit/<int:pk>/",
        AdminEditMessageOnChatRoomView.as_view(),
        name="admin_edit_message_chatroom",
    ),
    path(
        "admin/close/",
        AdminCloseTicketView.as_view(),
        name="admin_close_chatroom",
    ),
]
