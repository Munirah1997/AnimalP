"""FYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.views import *
from user.views import SendMessageView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'messages', MessageViewSet)



urlpatterns = [
    path('msgs', get_messages),
    path('mmmss/', MessagesView.as_view(), name='messages'),
    path('users', get_users),
    path('initiate_chat', GetOrCreateChatView.as_view(), name='initiate_chat'),    
    path('report', get_reports),
    path('register', register_user),
    path('messages/', SendMessageView.as_view(), name='send_message'),
    path('login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('add_report/', add_report, name='add_report'),
    path('message/status/<uuid:sender_uuid>/<uuid:receiver_uuid>/', UpdateMessageStatusView.as_view(), name='message-status-update'),
    path('api/update_message_status/', update_message_status, name='update_message_status'),
    path('update_report/', update_report, name='update_report'),
    path('api/report/<uuid:report_id>/status/', update_report_status),
    path('api/report/<uuid:report_id>/verification/', update_verification_status),
    path('cancel_report/<str:report_id>', cancel_report, name='cancel_report'),
    path('delete_report/<str:report_id>', delete_report, name='delete_report'),
    path('resend_report/<str:report_id>', resend_report, name='resend_report'),
    path('update_user', update_user),
    path('delete_user', delete_user),
    path('update_user_status', update_user_status),
    path('update_message_is_read/', UpdateMessageIsReadView.as_view(), name='update_message_is_read'),


]
