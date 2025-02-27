from django.contrib import admin
from .models import ChatRoom, Mensaje


class MensajeInline(admin.TabularInline):
    model = Mensaje
    extra = 0  # No añadir filas vacías por defecto


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_participants')  # Mostrar nombre y participantes
    search_fields = ('name',)  # Permitir búsqueda por nombre
    inlines = [MensajeInline]  # Mostrar mensajes relacionados en la misma página

    def get_participants(self, obj):
        return ", ".join([user.get_full_name() or user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'  # Nombre en la tabla


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'content', 'timestamp')  # Campos visibles en la lista
    list_filter = ('room', 'timestamp')  # Filtros por sala y fecha
    search_fields = ('content', 'sender__username', 'sender__first_name', 'sender__last_name')  # Búsqueda
    ordering = ('-timestamp',)  # Ordenar por fecha descendente
