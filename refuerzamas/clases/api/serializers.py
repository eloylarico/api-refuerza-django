# Rest
from rest_framework import serializers

# Model
from refuerzamas.clases.models import (
    Chat,
    Mensaje,
    User,
    Estudiante,
    Tutor,
    Docente,
    Institucion,
    Grado,
    Genero,
    GradoInstruccion,
    Clase,
    Curso,
    Materia,
    Grado,
    Nivel,
    Mensaje,
)
from refuerzamas.ciudades.models import Pais, Region, Ciudad


# Other Serialziers
class NivelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = ("id", "nombre", "descripcion", "orden", "foto")


class MateriaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ("nombre", "foto")


class GradoModelSerializer(serializers.ModelSerializer):
    nivel = NivelModelSerializer(required=False, read_only=True)

    class Meta:
        model = Grado
        fields = ("id", "nombre", "descripcion", "orden", "nivel")


class CursoModelSerializer(serializers.ModelSerializer):
    materia = MateriaModelSerializer(required=False, read_only=True)
    grado = GradoModelSerializer(required=False, read_only=True)

    class Meta:
        model = Curso
        fields = ("materia", "grado")


class PaisModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = ("nombre",)


class RegionModelSerializer(serializers.ModelSerializer):
    pais = PaisModelSerializer(required=False, read_only=True)

    class Meta:
        model = Region
        fields = ("nombre", "pais")


class CiudadModelSerializer(serializers.ModelSerializer):
    region = RegionModelSerializer(required=False, read_only=True)

    class Meta:
        model = Ciudad
        fields = ("nombre", "region")


class InstitucionModelSerializer(serializers.ModelSerializer):
    ciudad = CiudadModelSerializer(required=False, read_only=True)

    class Meta:
        model = Institucion
        fields = ("id", "nombre", "ciudad", "nivel", "foto")
        read_only_fields = ("id",)


class GenerosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ("id", "nombre")


class GradoInstruccionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradoInstruccion
        fields = ("nombre",)


# Serializers User
class DocenteModelSerializer(serializers.ModelSerializer):
    # user =
    grado_instruccion = GradoInstruccionModelSerializer(required=False, read_only=True)
    grado_instruccion_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    cursos = CursoModelSerializer(required=False, read_only=True, many=True)
    materias = MateriaModelSerializer(source="get_materias", required=False, read_only=True, many=True)

    class Meta:
        model = Docente
        fields = (
            "grado_instruccion",
            "grado_instruccion_id",
            "herramientas_videollamada",
            "entrevista",
            "confiabilidad",
            "señal",
            "breve_cv",
            "curriculum",
            "docencia",
            "titulo",
            "filosofia",
            "cursos",
            "materias",
            "estrellas",
        )


class TutorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = "__all__"


class UserTutorModelSerializer(serializers.ModelSerializer):
    genero = GenerosSerializer(required=False, read_only=True)
    perfil_tutor = TutorModelSerializer(required=False)
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "display_name",
            "nickname",
            "tipo_usuario",
            "avatar",
            "fecha_nacimiento",
            "celular",
            "email",
            "direccion",
            "observaciones",
            "genero",
            "perfil_tutor",
        )
        read_only_fields = (
            "email",
            "username",
            "tipo_usuario",
            "fecha_nacimiento",
            "genero",
            "perfil_tutor",
        )


class EstudianteModelSerializer(serializers.ModelSerializer):
    # class TutorModelSerializer(serializers.ModelSerializer):
    #     """
    #     Se colocó este serializer dentro de EstudianteModelSerializer porque se
    #     """
    #
    #     class Meta:
    #         model = Tutor
    #         fields = "__all__"

    institucion = InstitucionModelSerializer(required=False, read_only=True)
    grado = GradoModelSerializer(required=False, read_only=True)
    tutor = UserTutorModelSerializer(required=False, read_only=True)

    institucion_id = serializers.IntegerField(required=False, allow_null=True)
    grado_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Estudiante
        fields = ("institucion", "grado", "tutor", "institucion_id", "grado_id")
        read_only_fields = ("tutor",)


class UserEstudianteModelSerializer(serializers.ModelSerializer):
    genero = GenerosSerializer(required=False, read_only=True)
    perfil_estudiante = EstudianteModelSerializer(required=False)

    genero_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "nickname",
            "tipo_usuario",
            "avatar",
            "fecha_nacimiento",
            "celular",
            "email",
            "direccion",
            "observaciones",
            "genero",
            "perfil_estudiante",
            "genero_id",
        )
        read_only_fields = (
            "email",
            "tipo_usuario",
            "fecha_nacimiento",
            "genero",
        )
        depth = 5

    def update(self, instance, validated_data):
        estudiante = instance.perfil_estudiante
        data = False
        if validated_data.get("perfil_estudiante"):
            data = validated_data.get("perfil_estudiante")

        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.fecha_nacimiento = validated_data.get("fecha_nacimiento", instance.fecha_nacimiento)
        instance.celular = validated_data.get("celular", instance.celular)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.observaciones = validated_data.get("observaciones", instance.observaciones)
        instance.genero_id = validated_data.get("genero_id", instance.genero_id)
        instance.save()

        if data:
            estudiante.institucion_id = data.get("institucion_id", estudiante.institucion_id)
            estudiante.grado_id = data.get("grado_id", estudiante.grado_id)
            estudiante.save()
        return instance


class UserDocenteModelSerializer(serializers.ModelSerializer):
    genero = GenerosSerializer(required=False, read_only=True)
    perfil_docente = DocenteModelSerializer(required=False)
    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "display_name",
            "nickname",
            "tipo_usuario",
            "avatar",
            "fecha_nacimiento",
            "celular",
            "email",
            "direccion",
            "observaciones",
            "genero",
            "perfil_docente",
        )
        read_only_fields = (
            "email",
            "tipo_usuario",
            "fecha_nacimiento",
            "genero",
        )

    def update(self, instance, validated_data):
        docente = instance.perfil_docente
        data = False
        if validated_data.get("perfil_docente"):
            data = validated_data.get("perfil_docente")

        instance.username = validated_data.get("username", instance.username)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.fecha_nacimiento = validated_data.get("fecha_nacimiento", instance.fecha_nacimiento)
        instance.celular = validated_data.get("celular", instance.celular)
        instance.direccion = validated_data.get("direccion", instance.direccion)
        instance.observaciones = validated_data.get("observaciones", instance.observaciones)

        if data:
            docente.grado_instruccion_id = data.get("grado_instruccion_id", docente.grado_instruccion_id)
            docente.herramientas_videollamada = data.get("herramientas_videollamada", docente.herramientas_videollamada)
            docente.entrevista = data.get("entrevista", docente.entrevista)
            docente.confiabilidad = data.get("confiabilidad", docente.confiabilidad)
            docente.señal = data.get("señal", docente.señal)
            docente.breve_cv = data.get("breve_cv", docente.breve_cv)
            docente.curriculum = data.get("curriculum", docente.curriculum)
            docente.docencia = data.get("docencia", docente.docencia)
            docente.titulo = data.get("titulo", docente.titulo)
            docente.filosofia = data.get("filosofia", docente.filosofia)
            docente.save()
        return instance


class ClaseModelSerializer(serializers.ModelSerializer):
    # docente = DocenteModelSerializer()
    docente = UserDocenteModelSerializer(source="get_docente__user", read_only=True)
    user = UserEstudianteModelSerializer(source="get_estudiante__user", read_only=True)
    curso = CursoModelSerializer(required=False, read_only=True)

    class Meta:
        model = Clase
        fields = (
            "id",
            "docente",
            "user",
            "precio_estudiante",
            "enlace_videollamada",
            "precio_docente",
            "medio_pago",
            "hora_inicio",
            "hora_fin",
            "estado",
            "motivo_reporte",
            "observaciones",
            "curso",
        )


class MensajeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = "__all__"


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["display_name"]


class ChatModelSerializer(serializers.ModelSerializer):
    ultimo_mensaje = MensajeModelSerializer(read_only=True)
    user1 = UserModelSerializer(read_only=True)
    user2 = UserModelSerializer(read_only=True)

    class Meta:
        model = Chat
        exclude = ["activo"]
