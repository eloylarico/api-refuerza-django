from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from refuerzamas.ciudades.models import Ciudad
from refuerzamas.clases.managers import ClasesManager
from datetime import timedelta, datetime


class Genero(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Géneros"


class Nivel(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField("Descripción", blank=True, null=True)
    orden = models.PositiveIntegerField("Órden", blank=True, null=True)
    foto = models.ImageField(
        "Ícono del nivel", upload_to="clases/niveles/iconos", null=True, blank=True
    )

    class Meta:
        verbose_name_plural = "Niveles"
        verbose_name = "Nivel"

    def __str__(self):
        return self.nombre


class Grado(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField("Descripción", blank=True, null=True)
    orden = models.PositiveIntegerField(blank=True, null=True)
    nivel = models.ForeignKey(Nivel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.nivel}"


class Institucion(models.Model):
    nombre = models.CharField(max_length=255)
    ciudad = ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Ciudad",
        help_text="Campo que referencia a la ciudad del doctor en la aplicación",
    )
    nivel = models.ForeignKey(
        Nivel,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Nivel",
        help_text="Campo que referencia al nivel académico: Escolar, Preparatoria, Universidad",
    )
    foto = models.ImageField(
        "Foto de la institucion",
        upload_to="usuarios/institucion",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Instituciones"


class GradoInstruccion(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        verbose_name = "Grado de instrucción"
        verbose_name_plural = "Grados de instrucción"


class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    foto = models.ImageField(
        "Ícono del curso", upload_to="clases/cursos/fotos", null=True
    )

    def __str__(self):
        return self.nombre


class Curso(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT)
    grado = models.ForeignKey(
        Grado,
        on_delete=models.PROTECT,
        help_text="Campo que referencia al grado(1° de primaria, 2° de Secundaria, etc) del estudiante",
    )
    precio = models.DecimalField(max_digits=11, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.materia} - {self.grado}"


class Dia(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre}"


class Hora(models.Model):
    dia = models.ForeignKey(
        Dia, on_delete=models.CASCADE, related_name="horas_disponibles"
    )
    hora_inicio = models.IntegerField(default=0)
    hora_fin = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.dia} ({self.hora_inicio} - {self.hora_fin})"


class User(AbstractUser):
    """Default user para RefuerzaMas."""

    # Choices
    ESTUDIANTE = "ESTUDIANTE"
    DOCENTE = "DOCENTE"
    TUTOR = "TUTOR"
    TIPO_USUARIO_CHOICES = [
        (ESTUDIANTE, "Estudiante"),
        (DOCENTE, "Docente"),
        (TUTOR, "Tutor"),
    ]
    # Fields
    nickname = models.CharField(
        blank=True,
        null=True,
        max_length=255,
        help_text="Nombre que se le mostrará al demas de usuarios",
    )
    tipo_usuario = models.CharField(
        "Tipo de usuario",
        help_text="Tipo de usuario que el usuario será[Docente, Estudiante, Tutor], si es un usuario del admin, dejar en blanco",
        max_length=100,
        choices=TIPO_USUARIO_CHOICES,
        null=True,
        blank=True,
    )
    avatar = models.ImageField(
        "Foto de perfil", upload_to="users/avatar", null=True, blank=True
    )
    fecha_nacimiento = models.DateField("Fecha de nacimiento", null=True, blank=True)
    genero = models.ForeignKey(
        Genero, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Género"
    )
    celular = models.CharField(max_length=9, null=True, blank=True)
    email = models.EmailField("Correo electrónico", unique=True)
    ciudad = models.ForeignKey(
        Ciudad,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Campo que referencia a la ciudad del usuario en la aplicación",
    )
    direccion = models.CharField("Dirección", max_length=255, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    raw_password = models.CharField("Contraseña sin encriptar", max_length=255)
    # Auth Config
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def set_password(self, raw_password):
        """Sobreescribimos este método para poder asignar y guardar la contraseña sin encriptar en el campo raw_password"""
        self.password = make_password(raw_password)
        self._password = raw_password
        self.raw_password = raw_password

    def get_chats(self):
        return Chat.objects.filter(chats_users__user=self)

    def get_mis_docentes(self):
        reservas = self.get_mis_reservas()
        user_docentes_ids = reservas.values_list("docente__user_id")
        docentes = User.objects.filter(id__in=user_docentes_ids)
        return docentes

    def get_mis_reservas(self):
        if self.tipo_usuario == User.ESTUDIANTE:
            reservas = self.perfil_estudiante.mis_reservas.all()
        elif self.tipo_usuario == User.TUTOR:
            users_estudiante_ids = self.perfil_tutor.tutelados.all().values_list(
                "user_id", flat=True
            )
            reservas = Clase.objects.filter(
                estudiante__user_id__in=users_estudiante_ids
            )

        return reservas

    def crear_orden(self, curso_id, docente_id, fechas, estudiante_id):
        if self.tipo_usuario == self.ESTUDIANTE or self.tipo_usuario == self.TUTOR:
            if self.tipo_usuario == self.ESTUDIANTE:
                estudiante = self.perfil_estudiante
            elif self.tipo_usuario == self.TUTOR:
                tutelado_user = User.objects.get(pk=estudiante_id)
                estudiante = tutelado_user.perfil_estudiante


            curso = Curso.objects.get(pk=curso_id)
            docente = Docente.objects.get(pk=docente_id)
            numero_orden_compra = None
            compra = []
            precio_curso = curso.precio
            for fecha in fechas:
                hora = Hora.objects.get(pk=fecha["hora_id"])
                fecha_inicio = datetime.strptime(fecha["fecha"], "%d/%m/%Y").replace(
                    hour=hora.hora_inicio
                )
                fecha_fin = datetime.strptime(fecha["fecha"], "%d/%m/%Y").replace(
                    hour=hora.hora_fin
                )
                if not numero_orden_compra:
                    reserva = Reserva.objects.create(
                        estudiante=estudiante,
                        curso=curso,
                        docente=docente,
                        hora_inicio=fecha_inicio,
                        hora_fin=fecha_fin,
                        estado=Reserva.NO_PAGADA,
                        precio_estudiante=precio_curso,
                        precio_docente=precio_curso,
                        monto=precio_curso,
                        monto_total=precio_curso,
                        porcentaje_descuento=0,
                    )
                    numero_orden_compra = str(reserva.id).zfill(5)
                    reserva.orden_compra = numero_orden_compra
                    reserva.save()
                else:
                    reserva = Reserva.objects.create(
                        estudiante=estudiante,
                        curso=curso,
                        docente=docente,
                        orden_compra=numero_orden_compra,
                        hora_inicio=fecha_inicio,
                        hora_fin=fecha_fin,
                        estado=Reserva.NO_PAGADA,
                        precio_estudiante=precio_curso,
                        precio_docente=precio_curso,
                        monto=precio_curso,
                        monto_total=precio_curso,
                        porcentaje_descuento=0,
                    )
                compra.append(reserva)
        return compra

    @property
    def number_type(self):
        if self.tipo_usuario == User.DOCENTE:
            return 1
        return 0

    @property
    def display_name(self):
        # if self.get_full_name() != "":
        return self.get_full_name() or self.username or self.email

    @property
    def short_display_name(self):
        return self.display_name[:15]

    def clean(self) -> None:
        if (self.is_staff or self.is_superuser) and self.tipo_usuario is not None:
            raise ValidationError(
                "Un usuario de la aplicación no puede ser staff o superusuario, quitar el tipo de usuario o desactivar la opción 'es staff' o 'es superusuario'"
            )

    def __str__(self):
        show_name = ""
        if self.first_name != "" or self.first_name is not None:
            show_name += f" {self.first_name}"

        if self.last_name != "" or self.last_name is not None:
            show_name += f" {self.last_name}"

        if self.email != "" or self.email is not None:
            show_name += f" {self.email}"

        return show_name

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


class Tutor(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Tutor",
        on_delete=models.CASCADE,
        related_name="perfil_tutor",
    )

    class Meta:
        verbose_name = "Perfil del tutor"
        verbose_name_plural = "Perfiles de los tutores"

    def get_tutelados__user(self):
        ids_users_tutelados = self.tutelados.values_list("user_id", flat=True)
        return User.objects.filter(id__in=ids_users_tutelados)

    def __str__(self):
        return str(self.user)


class Estudiante(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="Estudiante",
        on_delete=models.CASCADE,
        related_name="perfil_estudiante",
    )
    institucion = models.ForeignKey(
        Institucion, on_delete=models.PROTECT, null=True, blank=True
    )
    grado = models.ForeignKey(Grado, blank=True, null=True, on_delete=models.PROTECT)
    tutor = models.ForeignKey(
        Tutor, blank=True, null=True, on_delete=models.PROTECT, related_name="tutelados"
    )
    breve_cv = models.TextField(null=True, blank=True)
    estrellas = models.PositiveSmallIntegerField(
        help_text="Calificación del 1 a 5 estrellas del docente.", default=5
    )

    class Meta:
        verbose_name = "Perfil del estudiante"
        verbose_name_plural = "Perfiles de los estudiantes"

    def __str__(self):
        return str(self.user)


class Docente(models.Model):
    # Choices
    MUY_BUENO = "MUY_BUENO"
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    MALO = "MALO"
    MALISIMO = "MALISIMO"

    ESCALA_EVALUACION_CHOICES = [
        (MUY_BUENO, "Muy bueno"),
        (BUENO, "Bueno"),
        (REGULAR, "Regular"),
        (MALO, "Malo"),
        (MALISIMO, "Malísimo"),
    ]

    # Fields
    orden_compra = models.CharField(
        "N° orden de compra", max_length=30, null=True, blank=True
    )
    user = models.OneToOneField(
        User,
        verbose_name="Docente",
        on_delete=models.CASCADE,
        related_name="perfil_docente",
    )
    grado_instruccion = models.ForeignKey(
        GradoInstruccion,
        verbose_name="Grado de instrucción",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    herramientas_videollamada = models.TextField(
        "Herramientas de videollamada", null=True, blank=True
    )
    entrevista = models.BooleanField(blank=True, null=True)
    confiabilidad = models.CharField(
        max_length=100, choices=ESCALA_EVALUACION_CHOICES, blank=True, null=True
    )
    señal = models.CharField(
        max_length=100, choices=ESCALA_EVALUACION_CHOICES, blank=True, null=True
    )
    breve_cv = models.TextField(null=True, blank=True)
    curriculum = models.CharField(
        max_length=100, choices=ESCALA_EVALUACION_CHOICES, blank=True, null=True
    )
    estrellas = models.PositiveSmallIntegerField(
        help_text="Calificación del 1 a 5 estrellas del docente.", default=5
    )
    docencia = models.BooleanField(blank=True, null=True)
    titulo = models.BooleanField(blank=True, null=True)
    filosofia = models.TextField(null=True, blank=True)
    cursos = models.ManyToManyField(Curso, related_name="cursos")
    horario = models.ManyToManyField(Hora, related_name="horario")

    def get_dias_habiles(self):
        dias_ids = list(set(self.horario.all().values_list("dia_id", flat=True)))
        dias_array = list(
            Dia.objects.filter(id__in=dias_ids).values_list("nombre", flat=True)
        )
        return dias_array

    def get_materias(self):
        materias_ids = self.cursos.values_list("materia_id", flat=True)
        return Materia.objects.filter(id__in=materias_ids)

    def set_horario(self, horario):
        self.horario.clear()
        for hora_id in horario:
            hora = Hora.objects.get(pk=hora_id)
            self.horario.add(hora)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Perfil del docente"
        verbose_name_plural = "Perfiles de los docentes"


# Quitar
class HorarioLibreDocente(models.Model):
    docente = models.ForeignKey(
        Docente,
        on_delete=models.CASCADE,
        verbose_name="Horarios Libres del Docente",
    )
    hora_inicio = models.DateTimeField("Fecha y hora del inicio del horario libre")
    hora_fin = models.DateTimeField("Fecha y hora del fin del horario libre")

    def clean(self) -> None:
        if self.hora_inicio > self.hora_fin:
            raise ValidationError(
                "La hora de inicio no puede ser mayor a la hora de fin"
            )

    def __str__(self):
        return f"{self.docente} [{self.hora_inicio} - {self.hora_fin}]"

    class Meta:
        verbose_name = "Horario Libre"
        verbose_name_plural = "Horarios Libres"


class TipoPago(models.Model):
    MODAL_TRANSFERENCIA_INTERBANCARIA = "MODAL_TRANSFERENCIA_INTERBANCARIA"
    MODAL_DEPOSITO_BANCARIO = "MODAL_DEPOSITO_BANCARIO"
    MODAL_TRANSFERENCIA_MOVIL = "MODAL_TRANSFERENCIA_MOVIL"
    TIPO_DE_MODAL = [
        (MODAL_TRANSFERENCIA_INTERBANCARIA, "MODAL TRANSFERENCIA INTERBANCARIA"),
        (MODAL_DEPOSITO_BANCARIO, "MODAL DEPOSITO BANCARIO"),
        (MODAL_TRANSFERENCIA_MOVIL, "MODAL TRANSFERENCIA MÓVIL"),
    ]
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.CharField(max_length=255, null=True, blank=True)
    icono = models.ImageField(
        "Ícono de tipo de pago",
        upload_to="clases/tipos_de_pago/",
        null=True,
        blank=True,
    )
    tipo_modal = models.CharField(
        max_length=250, choices=TIPO_DE_MODAL, null=True, blank=True
    )
    prioridad = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Tipo de pago"
        verbose_name_plural = "Tipos de pago"

    def __str__(self):
        return self.nombre


class MedioPago(models.Model):
    # Campos
    nombre = models.CharField(max_length=255, unique=True)
    tipo = models.ForeignKey(
        TipoPago,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="medios_pago",
    )
    nombre_destinatario = models.CharField(max_length=255, blank=True, null=True)
    dni_destinatario = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=255, blank=True, null=True)
    icono = models.ImageField(
        "Ícono de medio de pago",
        help_text="Este ícono solo es visible para los medios de pago de tipo 'Transferencia por celular'",
        null=True,
        blank=True,
        upload_to="clases/medios_de_pago/",
    )

    class Meta:
        verbose_name = "Medio de pago"
        verbose_name_plural = "Medios de pago"

    def __str__(self):
        return self.nombre


class Reserva(models.Model):
    # Choices
    NO_PAGADA = "NoPagada"
    PAGADA = "Pagada"
    PENDIENTE = "Pendiente"
    ACTIVA = "Activo"
    TERMINADA = "Terminada"
    REPROGRAMADA = "Reprogramada"
    CANCELADA = "Cancelada"
    REPORTADA = "Reportada"

    ESTADO_CLASE_CHOICES = [
        (NO_PAGADA, "No pagada"),
        (PAGADA, "Pagada"),
        (PENDIENTE, "Pendiente"),
        (ACTIVA, "Activo"),
        (TERMINADA, "Terminada"),
        (REPROGRAMADA, "Reprogramada"),
        (CANCELADA, "Cancelada"),
        (REPORTADA, "Reportada"),
    ]
    # Campos
    orden_compra = models.CharField(
        "N° Orden de compra", max_length=30, null=True, blank=True
    )
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.PROTECT,
        verbose_name="Estudiante",
        related_name="mis_reservas",
    )
    """ Se le coloca clases como related name, ya que si un profesor tiene reservas es porque esa reverva paso a ser clases """
    docente = models.ForeignKey(
        Docente, on_delete=models.PROTECT, null=True, blank=True, related_name="clases"
    )
    precio_estudiante = models.FloatField("Precio al Estudiante", default=0)
    precio_docente = models.FloatField("Precio al profesor", default=0)
    medio_pago = models.ForeignKey(
        MedioPago,
        verbose_name="Medio de pago",
        on_delete=models.CASCADE,
        related_name="medio_pago",
        null=True,
    )
    hora_inicio = models.DateTimeField()
    hora_fin = models.DateTimeField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="reservas")
    estado = models.CharField(
        max_length=100, choices=ESTADO_CLASE_CHOICES, default=PENDIENTE
    )
    motivo_reporte = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    enlace_videollamada = models.URLField(max_length=250)
    foto_pago = models.ImageField(
        "Foto de pago", null=True, blank=True, upload_to="clases/pagos/"
    )
    monto = models.DecimalField(
        "Monto sin descuento", max_digits=11, decimal_places=2, null=True, blank=True
    )
    porcentaje_descuento = models.IntegerField(
        "Porcentaje de descuento(%)", null=True, blank=True
    )
    monto_total = models.DecimalField(
        "Monto con descuento", max_digits=11, decimal_places=2, null=True, blank=True
    )

    # estado = models.ForeignKey(Estado, on_delete=models.PROTECT, help_text="Estado de la reserva")

    class Meta:
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"

    def asignar(self, docente_id):
        if self.estado != Reserva.PENDIENTE:
            raise ValidationError("Esta clase ya ha sido tomada")

        self.docente_id = docente_id
        self.estado = Reserva.ACTIVA
        self.save()
        return self

    def get_estudiante__user(self) -> User:
        return self.estudiante.user

    def aplicar_codigo_descuento(self, codigo):
        self.monto_total -= self.monto_total * codigo.porcentaje_descuento / 100
        self.porcentaje_descuento = codigo.porcentaje_descuento
        self.save()

    def adjuntar_comprobante_pago(self, foto_comprobante, medio_pago_id):
        self.foto_pago = foto_comprobante
        self.medio_pago_id = medio_pago_id
        self.estado = self.PAGADA
        self.save()

    def clean(self) -> None:
        # Comprobrando horas de inicio y fin
        if self.hora_inicio is None:
            raise ValidationError("Debes colocoar una hora de inicio válida")

        if self.hora_fin is None:
            raise ValidationError("Debes colocoar una hora de fin válida")

        if self.hora_inicio > self.hora_fin:
            raise ValidationError(
                "La hora de inicio no puede ser mayor a la hora de fin"
            )

        # Comprobrando estado, solo el estado pendiente puede estar sin profesor
        if self.estado == self.PENDIENTE and self.docente is not None:
            raise ValidationError(
                f"Una reserva {self.PENDIENTE} no puede tener un docente asignado."
            )
        if self.estado != self.PENDIENTE and self.docente is None:
            raise ValidationError(
                "Para que la reserva pase a este estado necesita de un docente"
            )

    def __str__(self):
        return f"Reserva de {self.estudiante} | Curso: + {self.curso} | Estado: {self.estado}"


class Clase(Reserva):
    """
    Modelo proxy para poder tener en el admin de django "Clase", el cuál traerá todas las reservas
    con un profesor asignado (a través del manager clases)"
    """

    clases = ClasesManager()

    def get_docente__user(self) -> User:
        return self.docente.user

    class Meta:
        proxy = True
        verbose_name = "Clase"
        verbose_name_plural = "Clases"


class Chat(models.Model):
    """
    Un chat entre usuarios
    """

    titulo = models.CharField("Título", null=True, blank=True, max_length=50)
    imagen = models.ImageField(
        "Imagen", null=True, blank=True, upload_to="clases/chats/imagen"
    )
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]

    def get_cantidad_usuarios(self):
        return self.chats_users.count()

    def get_mensajes_no_vistos(self, user: User):
        estado_no_vistos = ~Q(estado=Mensaje.VISTO)
        de_otros_usuarios = ~Q(chat_user__user=user)
        no_vistos_por_usuario = ~Q(users_visto__user=user)
        return Mensaje.objects.filter(
            estado_no_vistos,
            de_otros_usuarios,
            no_vistos_por_usuario,
            chat_user__chat=self,
        )

    def get_mensajes_vistos(self, user: User):
        de_otros_usuarios = ~Q(chat_user__user=user)
        vistos_por_usuario = Q(users_visto__user=user)

        return Mensaje.objects.filter(
            de_otros_usuarios, vistos_por_usuario, chat_user__chat=self
        )

    def get_mensajes(self):
        return Mensaje.objects.filter(chat_user__chat=self).order_by("-fecha")

    def get_ultimo_mensaje(self):
        # Se trae el primer mensaje porque está ordenado por fecha
        return self.get_mensajes().first()

    def get_titulo(self, current_user: User):
        if self.titulo == "" or self.titulo is None:
            chats_users = self.chats_users
            users_number = chats_users.count()
            if users_number > 1:
                chats_users = chats_users.exclude(user=current_user)
            first_user = chats_users.first()

            titulo = f"{first_user.user.short_display_name}"
            if users_number > 2:
                titulo += f" +{users_number - 2}"

            if first_user.user.tipo_usuario == User.DOCENTE:
                titulo = "Prof. " + titulo
            return titulo
        return self.titulo

    def get_imagen(self, current_user: User):
        if self.imagen.name:
            return self.imagen
        elif self.chats_users.all().count() >= 2:
            return (
                self.chats_users.filter(~Q(user_id=current_user.id)).first().user.avatar
            )
        elif self.chats_users.all().count() >= 1:
            return self.chats_users.filter(user_id=current_user.id).first().user.avatar
        else:
            return None

    def revisar(self, user: User):
        chat_user, _ = ChatUser.objects.get_or_create(user=user, chat=self)
        mensajes_vistos = []
        mensajes = self.get_mensajes().filter(
            ~Q(users_visto=chat_user), estado=Mensaje.ENTREGADO
        )
        for index, mensaje in enumerate(mensajes):
            mensaje.users_visto.add(chat_user)
            if mensaje.revisar_visto():
                mensajes_vistos.append(mensaje)
        return mensajes_vistos

    @property
    def get_participantes(self):
        user = User.objects.filter(chats_users__chat=self)
        names = []
        for u in user[:2]:
            names.append(u.display_name)
        if user.count() >= 3:
            names.append("y más ...")
        return names

    def __str__(self):
        return self.titulo or f"Chat {self.id}"


class ChatUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats_users")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="chats_users")

    class Meta:
        unique_together = [["user", "chat"]]

    # def clean(self) -> None:
    #     if self.user.tipo_usuario is None:
    #         raise ValidationError("Para que un usuario esté en un chat debe ser de tipo Docente, Alumno o Tutor.")

    def __str__(self):
        return f"{self.chat}: {self.user}"


class Mensaje(models.Model):
    # Choices
    VISTO = "VISTO"
    ENTREGADO = "ENTREGADO"
    ESTADO_MENSAJES_CHOICES = [
        (VISTO, "Visto"),
        (ENTREGADO, "Entregado"),
    ]

    chat_user = models.ForeignKey(
        ChatUser, on_delete=models.CASCADE, related_name="mensajes"
    )
    texto = models.TextField(blank=True, null=True)
    archivo = models.FileField(
        upload_to="clases/mensajes/archivos", blank=True, null=True
    )
    fecha = models.DateTimeField("Fecha y hora del mensaje", auto_now_add=True)
    # visto = models.BooleanField(default=False)
    estado = models.CharField(
        "Estado de mensaje",
        max_length=15,
        choices=ESTADO_MENSAJES_CHOICES,
        default=ENTREGADO,
    )
    users_visto = models.ManyToManyField(
        ChatUser,
        through="MensajeVisto",
        through_fields=(
            "mensaje",
            "chat_user",
        ),
    )

    def revisar_visto(self):
        cantidad_usuarios = self.chat_user.chat.get_cantidad_usuarios()
        # En caso en el que todos los usuarios hayan visto el mensaje, este pasará al estado de VISTO
        if self.users_visto.count() == cantidad_usuarios:
            self.estado = self.VISTO
            self.save()
            return True
        return False

    def get_chat_id(self):
        return self.chat_user.chat_id

    def get_user(self):
        return self.chat_user.user

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.chat_user}: [{self.texto or self.archivo}]"

    @property
    def date_formatting(self):
        fecha = self.fecha - timedelta(hours=5)
        return fecha.strftime("%d-%m-%Y %I:%M %p")

    def clean(self) -> None:
        if self.texto is None and self.archivo is None:
            raise ValidationError(
                "Debes enviar al menos un texto o un archivo para que sea un mensaje válido."
            )


class MensajeVisto(models.Model):
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE)
    chat_user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["chat_user", "mensaje"]]


class CodigoDescuento(models.Model):
    codigo = models.CharField(max_length=30)
    porcentaje_descuento = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Código de descuento"
        verbose_name_plural = "Códigos de descuento"

    def __str__(self):
        return f"{self.codigo} ({self.porcentaje_descuento}%)"
