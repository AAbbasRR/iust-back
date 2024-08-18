from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

v1_urlpatterns = [
    path("user/", include("app_user.api.urls", namespace="app_user")),
    path(
        "application/", include("app_application.api.urls", namespace="app_application")
    ),
    path("education/", include("app_education.api.urls", namespace="app_education")),
    path("occupation/", include("app_occupation.api.urls", namespace="app_occupation")),
    path(
        "frequently_question/",
        include(
            "app_frequently_question.api.urls", namespace="app_frequently_question"
        ),
    ),
    path(
        "notification/",
        include("app_notification.api.urls", namespace="app_notification"),
    ),
    path("chat/", include("app_chat.api.urls", namespace="app_chat")),
    path("admin/", include("app_admin.api.urls", namespace="app_admin")),
]

urlpatterns = [
    path("api/<str:version>/", include(v1_urlpatterns)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

handler404 = "utils.url_handlers.custom_404_response"
handler500 = "utils.url_handlers.custom_500_response"
