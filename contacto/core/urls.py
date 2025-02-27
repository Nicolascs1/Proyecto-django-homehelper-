

# url app core
from django.urls import path
from .views import home, lista, exit, register, perfil, verperfil, professional_detail,delete_credential, register_quotation, estadisticas, profile_credentials, confirm_quotation, reject_quotation, check_pending_quotation
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('lista/', lista, name='lista'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('perfil/', perfil, name='perfil'),
    path('verperfil/', verperfil, name='verperfil'),
    path('professional/<int:user_id>/', professional_detail, name='professional_detail'),
    path('delete_credential/<int:credential_id>/', delete_credential, name='delete_credential'),
    path('register-quotation/<int:recipient_id>/', register_quotation, name='register_quotation'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('perfil/<int:profile_id>/credenciales/', profile_credentials, name='profile_credentials'),
    path('confirm-quotation/<int:quotation_id>/', confirm_quotation, name='confirm_quotation'),
    path('reject-quotation/<int:quotation_id>/', reject_quotation, name='reject_quotation'),
    path('check-pending-quotation/', check_pending_quotation, name='check_pending_quotation'),

    
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password/password_reset_form.html',
            email_template_name='password/password_reset_email.html',
            subject_template_name='password/password_reset_subject.txt',
            success_url='/password_reset_done/'
        ),
        name='password_reset',
    ),

    path(
        'password_reset_done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
        name='password_reset_complete',
    ),
    
]
