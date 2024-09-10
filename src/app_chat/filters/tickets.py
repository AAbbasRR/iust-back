from django.db.models import Count, F

from django_filters import FilterSet, BooleanFilter, CharFilter

from app_chat.models import ChatRoomModel


class AdminTicketListFilter(FilterSet):
    my_tickets = BooleanFilter(method="get_my_tickets")
    status = CharFilter(method="filter_status")

    class Meta:
        model = ChatRoomModel
        fields = [
            "status",
            "my_tickets",
        ]

    def filter_status(self, queryset, name, value):
        if value:
            value_without_spaces = value.replace(" ", "")
            value_list = value_without_spaces.split(",")
            queryset = queryset.filter(status__in=value_list)
        return queryset

    def get_my_tickets(self, queryset, name, value):
        if value is True:
            return queryset.filter(admin=self.request.user)
        else:
            return queryset.filter(admin__isnull=True)
