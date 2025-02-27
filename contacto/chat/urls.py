from django.urls import path
from . import views

app_name = 'chat'  # Namespace de la app

urlpatterns = [
    path('', views.chat_list, name='chat_list'),  # Ruta para la lista de chats
    
    path("<str:room_name>/send_message/", views.send_message, name="send_message"),
    path("<str:room_name>/get_messages/", views.get_messages, name="get_messages"),
    path("delete-chat/<str:room_name>/", views.delete_chat, name="delete_chat"),
    
    
    path('create-chat/<int:professional_id>/', views.create_or_get_chat_room, name='create_chat'),
    path('<str:room_name>/', views.chat_room, name='chat_room'),
]
