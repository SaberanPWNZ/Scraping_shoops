
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from checker import views


urlpatterns = [
    path('', views.index, name='index'),
    path('partner/<slug:slug>/', views.partner_detail, name='partner_detail'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('partners/', views.partners, name='partners'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('checkers/', include('checker.urls')),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

