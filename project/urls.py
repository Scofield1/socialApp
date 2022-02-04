from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('create-room', views.create_room, name="create_room"),
    path('edit-room/<str:pk>', views.update_room, name="edit_room"),
    path('delete-room/<str:pk>', views.delete_room, name="delete_room"),
    # path('delete-message<str:pk>', views.delete_message, name="delete_msg"),
    path('room-details<str:pk>', views.room_details, name="room_details"),


    path('register', views.register, name="register"),
    path('user-profile/<str:pk>', views.user_profile, name="user-profile"),
    # path('edit-profile', views.edit_profile, name="edit_profile"),
    path('login', views.login_page, name="login"),
    path('logout', views.logout_page, name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
