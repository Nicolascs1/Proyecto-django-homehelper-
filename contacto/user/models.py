from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

#MODELO DE UESPECIALIDAD DE PROFESIONAL
class Speciality(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Regiones y comunas
regiones_comunas = {
    "Región de Arica y Parinacota": ["Arica", "Camarones", "Putre", "General Lagos"],
    "Región de Tarapacá": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"],
    "Región de Antofagasta": ["Antofagasta", "Mejillones", "Sierra Gorda", "Taltal", "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"],
    "Región de Atacama": ["Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro", "Vallenar", "Huasco", "Freirina", "Alto del Carmen"],
    "Región de Coquimbo": ["La Serena", "Coquimbo", "Ovalle", "Andacollo", "La Higuera", "Paihuano", "Vicuña", "Illapel", "Canela", "Los Vilos", "Salamanca"],
    "Región de Valparaíso": ["Valparaíso", "Viña del Mar", "Quilpué", "Villa Alemana", "Concón", "Quillota", "La Calera", "Hijuelas", "La Cruz", "Nogales", "Limache", "Olmué", "San Antonio", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo", "Isla de Pascua", "Petorca", "Cabildo", "La Ligua", "Papudo", "Zapallar", "San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María", "Los Andes", "Calle Larga", "Rinconada", "San Esteban"],
    "Región Metropolitana de Santiago": ["Santiago", "Vitacura", "Las Condes", "Providencia", "La Reina", "Ñuñoa", "Macul", "Peñalolén", "La Florida", "Puente Alto", "San José de Maipo", "San Bernardo", "Calera de Tango", "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor", "Melipilla", "Curacaví", "María Pinto", "San Pedro", "Buin", "Paine", "Colina", "Lampa", "Tiltil", "Pudahuel", "Quilicura", "Huechuraba", "Conchalí", "Renca", "Maipú", "Cerrillos", "Estación Central", "Lo Prado", "Cerro Navia", "Quinta Normal", "Lo Espejo", "Pedro Aguirre Cerda", "San Miguel", "San Joaquín", "La Cisterna", "El Bosque", "La Granja", "Lo Barnechea"],
    "Región de O’Higgins": ["Rancagua", "Machalí", "Graneros", "Codegua", "Rengo", "Requínoa", "Olivar", "Malloa", "San Vicente", "Las Cabras", "Peumo", "Pichidegua", "Coltauco", "San Fernando", "Chimbarongo", "Nancagua", "Placilla", "Santa Cruz", "Lolol", "Pumanque", "Marchigüe", "Pichilemu", "Litueche", "La Estrella", "Navidad", "Peralillo"],
    "Región del Maule": ["Talca", "Curicó", "Linares", "Cauquenes", "Constitución", "Molina", "San Clemente", "San Javier", "Teno", "Romeral", "Río Claro", "Sagrada Familia", "Hualañé", "Licantén", "Vichuquén", "Colbún", "Yerbas Buenas", "Longaví", "Parral", "Retiro", "Villa Alegre", "Cauquenes", "Pelluhue", "Chanco"],
    "Región de Ñuble": ["Chillán", "Chillán Viejo", "Bulnes", "Quillón", "San Ignacio", "El Carmen", "Pinto", "Pemuco", "Yungay", "San Carlos", "Coihueco", "Ñiquén", "San Fabián", "Ninhue", "San Nicolás", "Treguaco", "Portezuelo", "Ránquil", "Quirihue", "Cobquecura"],
    "Región del Biobío": ["Concepción", "Talcahuano", "Hualpén", "Penco", "Tomé", "San Pedro de la Paz", "Chiguayante", "Coronel", "Lota", "Hualqui", "Santa Juana", "Florida", "Arauco", "Curanilahue", "Los Álamos", "Lebu", "Tirúa", "Los Ángeles", "Nacimiento", "Laja", "San Rosendo", "Santa Bárbara", "Alto Biobío", "Mulchén", "Quilaco", "Quilleco", "Antuco"],
    "Región de La Araucanía": ["Temuco", "Padre Las Casas", "Carahue", "Nueva Imperial", "Villarrica", "Pucón", "Loncoche", "Toltén", "Cunco", "Melipeuco", "Curarrehue", "Vilcún", "Lautaro", "Perquenco", "Galvarino", "Traiguén", "Victoria", "Angol", "Renaico", "Collipulli", "Ercilla", "Los Sauces", "Lumaco", "Purén"],
    "Región de Los Ríos": ["Valdivia", "Panguipulli", "Los Lagos", "Lago Ranco", "Futrono", "La Unión", "Río Bueno", "Paillaco", "Corral", "Máfil", "Mariquina", "Lanco"],
    "Región de Los Lagos": ["Puerto Montt", "Puerto Varas", "Llanquihue", "Fresia", "Frutillar", "Calbuco", "Maullín", "Los Muermos", "Ancud", "Castro", "Quellón", "Quemchi", "Chonchi", "Dalcahue", "Curaco de Vélez", "Quinchao", "Hualaihué", "Chaitén", "Futaleufú", "Palena"],
    "Región de Aysén": ["Coyhaique", "Puerto Aysén", "Cisnes", "Guaitecas", "Río Ibáñez", "Chile Chico", "O’Higgins", "Tortel", "Cochrane"],
    "Región de Magallanes y de la Antártica Chilena": ["Punta Arenas", "Puerto Natales", "Porvenir", "Cabo de Hornos", "Primavera", "Laguna Blanca", "Río Verde", "Timaukel", "Torres del Paine", "Antártica"]
}


regiones = list(regiones_comunas.keys())

# MODELO DE USUARIO
class User(AbstractUser):
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name='Nombres')  # Nombre
    last_name = models.CharField(max_length=150, null=False, blank=False, verbose_name='Apellidos')  # Apellido
    location = models.CharField(max_length=60, null=False, blank=False, verbose_name='Dirección')
    telefono = models.CharField(max_length=15, null=False, blank=False, verbose_name='Teléfono')
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True, verbose_name="RUT")
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False, verbose_name='Correo electrónico')  # Correo obligatorio
    region = models.CharField(max_length=50, choices=[(region, region) for region in regiones], blank=False, verbose_name='Región')
    comuna = models.CharField(max_length=50, blank=False, verbose_name='Comuna')

#MODELO DE PERFIL
from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    specialties = models.ManyToManyField('Speciality', blank=True, related_name='profiles', verbose_name='Especialidades')
    visit_count = models.PositiveIntegerField(default=0)  # Nuevo campo para contar visitas
    bio = models.TextField(max_length=400, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='users/',  # Carpeta donde se guardarán las fotos
        default='profile_default.png',  # Ruta por defecto
        blank=True,
    )
    linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name="LinkedIn")
    instagram = models.URLField(max_length=255, null=True, blank=True, verbose_name="Instagram")
    facebook = models.URLField(max_length=255, null=True, blank=True, verbose_name="Facebook")
    twitter = models.URLField(max_length=255, null=True, blank=True, verbose_name="Twitter")
    website = models.URLField(max_length=255, null=True, blank=True, verbose_name="Página Web")

    def __str__(self):
        return f"Profile of {self.user.username}"

class Credential(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='credentials')
    title = models.CharField(max_length=255, verbose_name="Título")
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Descripción")
    file = models.FileField(upload_to='credentials/', verbose_name="Archivo (PDF o Imagen)")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.profile.user.username}"

    @property
    def is_image(self):
        return self.file.name.lower().endswith(('.png', '.jpg', '.jpeg'))

    @property
    def is_pdf(self):
        return self.file.name.lower().endswith('.pdf')



# MODELO DE RESEÑAS
class Review(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='reviews', verbose_name='Perfil reseñado')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews', verbose_name='Usuario que reseña')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Puntuación')  # Calificación de 1 a 5
    comment = models.TextField(max_length=1000, blank=True, null=True, verbose_name='Comentario')  # Comentario opcional
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    def __str__(self):
        return f"Review by {self.reviewer.username} on {self.profile.user.username}: {self.rating}/5"
    


# Cotizaciones
from django.db import models
from django.conf import settings

class Quotation(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_quotations')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_quotations')
    is_confirmed = models.BooleanField(default=False)  # Indica si la cotización ha sido confirmada
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Confirmada" if self.is_confirmed else "Pendiente"
        return f"Cotización de {self.sender} a {self.recipient} - {status}"

