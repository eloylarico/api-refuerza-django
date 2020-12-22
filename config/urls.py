from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

# Views
from refuerzamas.clases.api.views import UserDetailView
from refuerzamas.utils.auth.views import (
    obtain_estudiante_tutor_token,
    obtain_docente_token,
)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    path("api/auth/user/", UserDetailView.as_view(), name="user"),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/auth-token/docente", obtain_docente_token),
    path("api/auth-token/estudiante_tutor", obtain_estudiante_tutor_token),
    # Admin chat
    path("adminchat/",include(("administrar_chat.urls", "administrar_chat"), namespace="administrar_chat"),),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

admin.site.site_header = "Administrador de REFUERZA+"
admin.site.site_title = "REFUERZA+"
admin.site.index_title = "Bienvenido al administrador de REFUERZA+"
