from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'core/home.html')



#Lista de profesionales
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import Speciality
from core.forms import SpecialtyFilterForm
from user.models import regiones_comunas

from django.db.models import Avg
from user.models import Review

@login_required
def lista(request):
    # Obtener el grupo "profesional"
    group = Group.objects.get(name='profesional')

    # Obtener los usuarios del grupo y calcular el promedio de calificaciones
    professionals = group.user_set.prefetch_related('profile__specialties').annotate(
        average_rating=Avg('profile__reviews__rating')
    )

    # Manejar el formulario de filtro
    form = SpecialtyFilterForm(request.GET or None)
    if form.is_valid():
        specialty = form.cleaned_data.get('specialty')
        region = form.cleaned_data.get('region')
        comuna = form.cleaned_data.get('comuna')

        if specialty:
            professionals = professionals.filter(profile__specialties=specialty)
        if region:
            professionals = professionals.filter(region=region)
        if comuna:
            professionals = professionals.filter(comuna=comuna)

    # Crear un diccionario con los nombres de las salas
    chat_rooms = {
        professional.id: f"{min(request.user.id, professional.id)}-{max(request.user.id, professional.id)}"
        for professional in professionals if professional.id
    }

    return render(request, 'core/lista.html', {
        'professionals': professionals,
        'form': form,
        'chat_rooms': chat_rooms,
        'regiones_comunas': regiones_comunas,
    })





# Vista de mi perfil
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Max, Q
from user.models import Review, Profile
from user.models import Quotation
from django.db.models import Avg


@login_required
def verperfil(request):
    # Obtener el perfil del usuario logeado
    profile = getattr(request.user, 'profile', None)

    # Calcular el promedio de reseñas y obtener reseñas si el perfil existe
    reviews = []
    average_rating = None
    if profile:
        reviews = Review.objects.filter(profile=profile).order_by('-created_at')
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        average_rating = round(average_rating, 1) if average_rating else 0

    # Determinar si el usuario es profesional o cliente
    is_professional = request.user.groups.filter(name="profesional").exists()
    is_client = request.user.groups.filter(name="cliente").exists()

    # Obtener especialidades y redes sociales del usuario logeado si es profesional
    user_specialties = profile.specialties.all() if is_professional else []
    has_credentials = profile.credentials.exists() if is_professional else False
    has_social_links = any([profile.linkedin, profile.facebook, profile.twitter]) if profile else False

    # Mostrar alerta si es profesional y falta información
    show_alert = is_professional and (not user_specialties or not has_credentials or not has_social_links)

    # Subquery para obtener la última cotización enviada o recibida por usuario
    latest_quotations_subquery = Quotation.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user),
        Q(sender=OuterRef('sender')) | Q(recipient=OuterRef('recipient'))
    ).order_by('-created_at').values('id')[:1]

    # Filtrar cotizaciones usando la subquery
    latest_quotations = Quotation.objects.filter(
        id__in=Subquery(latest_quotations_subquery)
    ).select_related('sender__profile', 'recipient__profile')

    # Crear datos procesados sobre el otro usuario
    quotations_data = []
    for quotation in latest_quotations:
        other_user = quotation.recipient if quotation.sender == request.user else quotation.sender
        other_user_is_professional = other_user.groups.filter(name="profesional").exists()
        other_user_specialties = (
            other_user.profile.specialties.all() if other_user_is_professional else []
        )
        quotations_data.append({
            'quotation': quotation,
            'other_user': other_user,
            'is_professional': other_user_is_professional,
            'specialties': other_user_specialties,
        })

    return render(request, 'core/verperfil.html', {
        'profile': profile,
        'reviews': reviews,
        'average_rating': average_rating,
        'is_professional': is_professional,
        'is_client': is_client,
        'user_specialties': user_specialties,
        'latest_quotations_data': quotations_data,
        'show_alert': show_alert,  # Agregar esta variable al contexto
    })






def exit(request):
    logout(request)
    return redirect('home')


# Registro de usuarios
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from user.models import regiones_comunas

def register(request):
    if request.method == 'POST':
        # Define el formulario con los datos enviados por el usuario
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            # Asigna el grupo seleccionado
            group = form.cleaned_data['group']
            group.user_set.add(user)

            # Autenticar y loguear al usuario automáticamente
            login(request, user)

            # Mensaje de éxito y redirección
            messages.success(request, "Registro completado exitosamente. ¡Bienvenido!")
            return redirect('verperfil')
        else:
            # Agrega un mensaje general si el formulario tiene errores
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        # Define el formulario vacío para solicitudes GET
        form = CustomUserCreationForm()

    # Renderiza el formulario (vacío o con errores) y pasa las regiones/comunas al contexto
    return render(request, 'registration/register.html', {
        'form': form,
        'regiones_comunas': regiones_comunas
    })




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from user.models import Profile, User
from user.models import Review  # Importa el modelo Review
from user.models import Quotation  # Importa el modelo Quotation
from .forms import ReviewForm  # Importa el formulario ReviewForm

@login_required
def professional_detail(request, user_id):
    # Obtén el usuario y su perfil
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)

    # Determinar si el usuario es profesional o cliente
    is_professional = request.user.groups.filter(name="profesional").exists()
    is_client = request.user.groups.filter(name="cliente").exists()

    # Verifica si hay una cotización entre el usuario autenticado y el profesional
    has_quotation = Quotation.objects.filter(
        Q(sender=request.user, recipient=user) |
        Q(sender=user, recipient=request.user)
    ).exists()

    # Obtén las reseñas existentes para este perfil
    reviews = Review.objects.filter(profile=profile)

    # Calcula el promedio de puntuaciones
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']  # Obtiene el promedio de 'rating'

    # Maneja el formulario de reseñas
    if request.method == 'POST' and has_quotation:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user  # Asigna el usuario autenticado como autor de la reseña
            review.profile = profile  # Asigna el perfil reseñado
            review.save()
            return redirect('professional_detail', user_id=user.id)
    else:
        form = ReviewForm() if has_quotation else None

    # Incrementa el contador de visitas solo si el usuario no ha visitado este perfil en la sesión actual
    session_key = f'visited_profile_{user_id}'
    if not request.session.get(session_key, False):
        profile.visit_count += 1
        profile.save(update_fields=['visit_count'])  # Solo actualiza el campo 'visit_count'
        request.session[session_key] = True  # Marca el perfil como visitado en esta sesión

    # Pasa los datos al template
    return render(request, 'core/professional_detail.html', {
        'user': user,
        'profile': profile,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,  # Pasa el promedio al template
        'has_quotation': has_quotation,  # Pasa si hay cotización al template
        'is_professional': is_professional,  # Pasa si el usuario actual es profesional
        'is_client': is_client,  # Pasa si el usuario actual es cliente
    })







# VISTA PARA EDITAR PERFIL

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from user.models import Profile, Credential, regiones_comunas
from .forms import UserUpdateForm, ProfileUpdateForm, CredentialForm

@login_required
def perfil(request):
    user = request.user
    profile = user.profile

    # Obtener la región y comuna seleccionadas del usuario
    region_selected = user.region  # Asegúrate de que `User` tenga este campo
    comuna_selected = user.comuna  # Asegúrate de que `User` tenga este campo

    # Inicializar formularios con datos existentes
    user_form = UserUpdateForm(
        instance=user, 
        region_selected=region_selected
    )
    profile_form = ProfileUpdateForm(instance=profile)
    credential_form = CredentialForm()

    if request.method == 'POST':
        # Identificar la acción del formulario
        action = request.POST.get('action')

        if action == 'update_profile':
            # Procesar formularios de actualización de perfil
            user_form = UserUpdateForm(
                request.POST, 
                instance=user, 
                region_selected=request.POST.get('region')
            )
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            else:
                messages.error(request, 'Hubo un error al actualizar tu perfil.')

        elif action == 'add_credential':
            # Manejar subida de credenciales
            credential_form = CredentialForm(request.POST, request.FILES)
            if credential_form.is_valid():
                new_credential = credential_form.save(commit=False)
                new_credential.profile = profile
                new_credential.save()
                messages.success(request, 'Credencial subida correctamente.')
            else:
                messages.error(request, 'Error al subir la credencial.')

        elif action == 'delete_credential':
            # Manejar eliminación de credenciales
            credential_id = request.POST.get('delete_credential_id')
            credential = get_object_or_404(Credential, id=credential_id, profile=profile)
            credential.file.delete(save=False)  # Elimina el archivo asociado
            credential.delete()
            messages.success(request, 'Credencial eliminada correctamente.')

        return redirect('perfil')

    # Obtener todas las credenciales del perfil
    credentials = profile.credentials.all()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'credential_form': credential_form,
        'credentials': credentials,
        'is_professional': user.groups.filter(name="profesional").exists(),
        'regiones_comunas': regiones_comunas,
    }

    return render(request, 'core/perfil.html', context)





#Eliminar credencial
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Credential

@login_required
def delete_credential(request, credential_id):
    credential = get_object_or_404(Credential, id=credential_id, profile=request.user.profile)

    try:
        # Eliminar archivo físico
        if credential.file:
            credential.file.delete(save=False)
        # Eliminar registro de la base de datos
        credential.delete()
        messages.success(request, 'La credencial ha sido eliminada correctamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar la credencial: {str(e)}')

    return redirect('perfil')


#Cotizaciones
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import Quotation, Profile, User

@login_required
def register_quotation(request, recipient_id):
    if request.method == 'POST':
        recipient = get_object_or_404(Profile, id=recipient_id).user
        Quotation.objects.create(sender=request.user, recipient=recipient, is_confirmed=False)
        return JsonResponse({'message': 'Cotización enviada. La página se actualizará.'}, status=200)
    return JsonResponse({'error': 'Método no permitido'}, status=405)


@login_required
def confirm_quotation(request, quotation_id):
    if request.method == 'POST':
        quotation = get_object_or_404(Quotation, id=quotation_id, recipient=request.user)

        # Confirmar la cotización
        quotation.is_confirmed = True
        quotation.save()
        return JsonResponse({'message': 'Cotización confirmada exitosamente.'}, status=200)
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def reject_quotation(request, quotation_id):
    if request.method == 'POST':
        quotation = get_object_or_404(Quotation, id=quotation_id, recipient=request.user)

        # Eliminar la cotización (o cambiar su estado si quieres mantener un registro)
        quotation.delete()

        return JsonResponse({'message': 'La cotización ha sido rechazada.'}, status=200)
    return JsonResponse({'error': 'Método no permitido'}, status=405)



@login_required
def check_pending_quotation(request):
    pending_quotation = Quotation.objects.filter(recipient=request.user, is_confirmed=False).first()
    if pending_quotation:
        return JsonResponse({
            'has_pending': True,
            'quotation_id': pending_quotation.id,
            'sender_name': f"{pending_quotation.sender.first_name} {pending_quotation.sender.last_name}",
        })
    return JsonResponse({'has_pending': False})




# Estadisticas
from django.db.models.functions import TruncDay
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from user.models import Quotation
from datetime import date, timedelta
import calendar
from django.db.models import Sum

@login_required
def estadisticas(request):
    user = request.user

    # Obtener el día de hoy
    today = date.today()

    # Generar las fechas para todos los días del mes actual
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    current_month_days = [
        date(today.year, today.month, day) for day in range(1, days_in_month + 1)
    ]

    # Generar las fechas para todos los días de la semana actual
    start_of_week = today - timedelta(days=today.weekday())
    current_week_days = [start_of_week + timedelta(days=i) for i in range(7)]

    # Cotizaciones por día del mes
    monthly_data = (
        Quotation.objects.filter(
            recipient=user,
            created_at__date__month=today.month,
            created_at__date__year=today.year,
        )
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
    )

    monthly_day_counts = {item['day'].date(): item['count'] for item in monthly_data}
    monthly_day_labels = [day.strftime('%Y-%m-%d') for day in current_month_days]
    monthly_counts = [monthly_day_counts.get(day, 0) for day in current_month_days]

    # Cotizaciones por día de la semana
    weekly_data = (
        Quotation.objects.filter(
            recipient=user,
            created_at__date__gte=start_of_week,
            created_at__date__lte=start_of_week + timedelta(days=6),
        )
        .annotate(day=TruncDay('created_at'))
        .values('day')
        .annotate(count=Count('id'))
    )

    weekly_day_counts = {item['day'].date(): item['count'] for item in weekly_data}
    weekly_day_labels = [day.strftime('%A') for day in current_week_days]
    weekly_counts = [weekly_day_counts.get(day, 0) for day in current_week_days]

    # Nombre del mes actual en español
    import locale
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")  # Cambia a español
    current_month_name = today.strftime('%B').capitalize()


    # Consultar las visitas recibidas por el perfil del usuario autenticado
    profile = Profile.objects.get(user=user)
    visit_count = profile.visit_count


  # Gráfico del mes
    plt.figure(figsize=(12, 6))
    plt.bar(
        [day.day for day in current_month_days],  # Solo el número del día
        monthly_counts,
        color='#1f77b4',  # Color azul atractivo
        edgecolor='black',  # Bordes negros para barras
        linewidth=0.5
    )
    plt.title(f'Cotizaciones del mes {current_month_name} {today.year}', fontsize=16, fontweight='bold')
    plt.xlabel('Día del Mes', fontsize=12)
    plt.ylabel('Cantidad de Cotizaciones', fontsize=12)
    plt.xticks(rotation=0, fontsize=10)  # Evitar inclinación en números del eje X
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Línea de referencia horizontal
    buffer_monthly = io.BytesIO()
    plt.savefig(buffer_monthly, format='png', bbox_inches='tight')  # Ajustar márgenes
    buffer_monthly.seek(0)
    monthly_image_png = buffer_monthly.getvalue()
    buffer_monthly.close()
    monthly_graphic = base64.b64encode(monthly_image_png).decode('utf-8')


    # Gráfico de la semana
    plt.figure(figsize=(8, 4))
    plt.bar(
        [day.strftime('%a') for day in current_week_days],  # Días abreviados (lun, mar, ...)
        weekly_counts,
        color='#2ca02c',  # Color verde atractivo
        edgecolor='black',  # Bordes negros para barras
        linewidth=0.5
    )
    plt.title('Cotizaciones de esta semana', fontsize=16, fontweight='bold')
    plt.xlabel('Día de la Semana', fontsize=12)
    plt.ylabel('Cantidad de Cotizaciones', fontsize=12)
    plt.xticks(rotation=0, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Línea de referencia horizontal
    buffer_weekly = io.BytesIO()
    plt.savefig(buffer_weekly, format='png', bbox_inches='tight')  # Ajustar márgenes
    buffer_weekly.seek(0)
    weekly_image_png = buffer_weekly.getvalue()
    buffer_weekly.close()
    weekly_graphic = base64.b64encode(weekly_image_png).decode('utf-8')


    context = {
        'weekly_graphic': weekly_graphic,
        'monthly_graphic': monthly_graphic,
        'visit_count': visit_count,  # Número de visitas recibidas
    }

    return render(request, 'graficos/estadisticas.html', context)


#Mostrar credenciales
from django.shortcuts import render, get_object_or_404
from user.models import Credential, Profile

@login_required
def profile_credentials(request, profile_id):
    # Obtiene el perfil del usuario seleccionado
    profile = get_object_or_404(Profile, id=profile_id)

    # Obtiene las credenciales asociadas al perfil
    credentials = Credential.objects.filter(profile=profile)

    # Renderiza la página con las credenciales
    return render(request, 'core/profile_credentials.html', {
        'profile': profile,
        'credentials': credentials,
    })



