from django.urls import path
from app.views import UserList,Auth,User1

urlpatterns = [
    path('user_list/', UserList),
    path('auth/',Auth),
    path('user1',User1)
]