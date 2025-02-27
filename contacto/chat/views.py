from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import Quotation, User
from .models import ChatRoom, Mensaje



# Crear o recuperar sala de chat y redirigir a la sala
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom
from user.models import User  # Asegúrate de importar tu modelo de usuario personalizado

@login_required
def create_or_get_chat_room(request, professional_id):
    # Obtener al profesional desde el modelo de usuario
    professional = get_object_or_404(User, id=professional_id)

    # Crear un nombre único para la sala
    room_name = f"{min(request.user.id, professional.id)}-{max(request.user.id, professional.id)}"

    # Crear o recuperar la sala
    room, created = ChatRoom.objects.get_or_create(name=room_name)

    # Asegurarse de que ambos usuarios sean participantes
    room.participants.add(request.user, professional)

    # Redirigir a la sala de chat
    return redirect('chat:chat_room', room_name=room.name)


# Vista para la sala de chat
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import ChatRoom
from user.models import Review, Profile   # Asegúrate de importar Profile

@login_required
def chat_room(request, room_name):
    # Recuperar la sala
    room = get_object_or_404(ChatRoom, name=room_name)

    # Verificar que el usuario actual sea participante
    if request.user not in room.participants.all():
        return redirect('chat:chat_list')  # Redirigir si no tiene acceso

    # Recuperar los mensajes y el otro usuario
    messages = room.mensajes.order_by('timestamp')
    other_user = room.participants.exclude(id=request.user.id).first()

    # Obtener el perfil del otro usuario
    other_user_profile = get_object_or_404(Profile, user=other_user)

    # Obtener las reseñas existentes para este perfil
    reviews = Review.objects.filter(profile=other_user_profile)

    # Calcular el promedio de puntuaciones
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    average_rating = round(average_rating, 1) if average_rating else 0  # Manejar valores nulos

    # Verificar si hay cotizaciones pendientes
    pending_quotation = Quotation.objects.filter(sender=other_user, recipient=request.user, is_confirmed=False).first()

    # Determinar el grupo al que pertenece el otro usuario
    other_user_group = (
        other_user.groups.first().name if other_user.groups.exists() else "Sin grupo"
    )

    return render(request, "chat/chat_room.html", {
        "room": room,
        "messages": messages,
        "other_user": other_user,
        "roomName": room_name,
        "average_rating": average_rating,  # Promedio calculado
        "reviews": reviews,  # Lista de reseñas
        "other_user_group": other_user_group,
        "other_user_profile_picture": other_user_profile.profile_picture.url if other_user_profile.profile_picture else None,
        'pending_quotation': pending_quotation,  # Pasar la cotización pendiente al template
    })



# Enviar mensaje desde la sala de chat

# Enviar mensaje y redirigir a la sala de chat
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Mensaje

@login_required
def send_message(request, room_name):
    if request.method == "POST":
        room = get_object_or_404(ChatRoom, name=room_name)
        content = request.POST.get("message")
        if content:
            message = Mensaje.objects.create(room=room, sender=request.user, content=content)
            return JsonResponse({
                "sender": f"{message.sender.first_name} {message.sender.last_name}",
                "content": message.content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        return JsonResponse({"error": "Mensaje vacío"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)



# Obtener mensajes de una sala para mostrarlos automáticamente
@login_required
def get_messages(request, room_name):
    room = get_object_or_404(ChatRoom, name=room_name)
    messages = room.mensajes.order_by("timestamp").values(
        "sender__id", "sender__first_name", "sender__last_name", "content", "timestamp"
    )
    return JsonResponse(list(messages), safe=False)



# Lista de conversaciones
from django.utils.timezone import localtime

@login_required
def chat_list(request):
    chat_rooms = ChatRoom.objects.filter(participants=request.user).prefetch_related('participants', 'mensajes')

    chats = [
        {
            "room": room,
            "other_participant_name": f"{room.participants.exclude(id=request.user.id).first().first_name} "
                                      f"{room.participants.exclude(id=request.user.id).first().last_name}",
            "last_message": room.mensajes.last().content if room.mensajes.exists() else "Sin mensajes aún",
            "last_message_time": localtime(room.mensajes.last().timestamp).strftime('%d/%m/%Y %H:%M') if room.mensajes.exists() else None
        }
        for room in chat_rooms
        if room.participants.exclude(id=request.user.id).exists()
    ]

    return render(request, "chat/chat.html", {"chats": chats})


# Eliminar conversación
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom

@login_required
def delete_chat(request, room_name):
    if request.method == "POST":
        room = get_object_or_404(ChatRoom, name=room_name)
        if request.user in room.participants.all():
            room.delete()
            return JsonResponse({"success": True})
        return JsonResponse({"error": "No tienes permiso para eliminar esta sala."}, status=403)
    return JsonResponse({"error": "Método no permitido."}, status=405)
