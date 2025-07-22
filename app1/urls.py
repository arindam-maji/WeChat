from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from  . views import register , loginView, index, search , user_logout , chatroom ,  add_user_to_chatroom
urlpatterns = [

    path('register/' , register , name = 'register' ) ,
    path('login/' ,  loginView, name= 'login') ,
    path('' , index ,  name  = 'index') ,
    path('search/' , search , name = 'search_users' ) ,
    path('logout/' , user_logout , name  = 'logout'),
    path('createroom/<int:user_id>/' ,add_user_to_chatroom , name  = 'create_chat_room'),
    path('chatroom/<int:id>/' , chatroom , name  = 'chatroom')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
