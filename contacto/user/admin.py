from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Speciality, Credential, Review, Quotation
from django.contrib.auth.models import Group

# Admin para el modelo User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'telefono', 'location', 'rut', 'region', 'comuna', 'password')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'telefono', 'region', 'comuna', 'password1', 'password2'),
        }),
    )
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'rut', 'region', 'comuna', 'is_staff', 'is_active')  # Agregamos 'region' y 'comuna'
    search_fields = ('id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'rut', 'region', 'comuna')  # Agregamos 'region' y 'comuna'
    ordering = ('id',)  # Ordenar por ID

# Admin para el modelo Speciality
@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin para el modelo Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'instagram', 'facebook', 'twitter', 'website')
    search_fields = ('user__username', 'bio', 'instagram', 'facebook', 'twitter', 'website')
    list_filter = ('specialties',)
    filter_horizontal = ('specialties',)

# Admin para el modelo Credential
@admin.register(Credential)
class CredentialAdmin(admin.ModelAdmin):
    list_display = ('profile', 'title', 'uploaded_at')
    search_fields = ('profile__user__username', 'title')
    list_filter = ('uploaded_at',)

# Admin para el modelo Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('profile', 'reviewer', 'rating', 'created_at')
    search_fields = ('profile__user__username', 'reviewer__username', 'comment')
    list_filter = ('rating', 'created_at')

# Personalización del modelo Group en el admin
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users')
    search_fields = ('name',)

    def get_users(self, obj):
        """Muestra una lista de usuarios asociados al grupo."""
        return ", ".join([user.username for user in obj.user_set.all()])
    get_users.short_description = 'Usuarios'

# Registrar el modelo Group con la personalización
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Admin para el modelo Quotation
@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'is_confirmed', 'created_at')
    list_filter = ('is_confirmed', 'created_at',)
    search_fields = ('sender__username', 'recipient__username')
