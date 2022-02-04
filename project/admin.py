from django.contrib import admin
from .models import *

admin.site.register(ProfileModel)
admin.site.register(TopicModel)
admin.site.register(RoomModel)
admin.site.register(MessageModel)