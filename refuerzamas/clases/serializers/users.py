#Rest
from rest_framework import serializers

#Model
from refuerzamas.clases.models import User, Estudiante, Tutor, Docente, Institucion, Grado

#Serializer
from refuerzamas.clases.serializers import GenerosSerializer, GradoModelSerializer

class InstitucionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Institucion
        fields = ("nombre", "ciudad", "nivel", "foto")



class DocenteModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Docente
        fields = ("grado_instruccion","herramientas_videollamada","entrevista", "confiabilidad", "señal", "breve_cv", "curriculum", "docencia", "titulo", "filosofia","cursos")



class TutorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        


class EstudianteModelSerializer(serializers.ModelSerializer):

    # institucion = InstitucionModelSerializer(required=False, read_only=True)
    # grado = GradoModelSerializer(required=False, read_only=True)
    # tutor = TutorModelSerializer(required=False, read_only=True)

    # institucion_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)
    # grado_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = Estudiante
        fields = ("institucion", "grado", "tutor")


class UserEstudianteModelSerializer(serializers.ModelSerializer):

    genero = GenerosSerializer(required=False)
    perfil_estudiante = EstudianteModelSerializer(required=False)

    class Meta:
        model = User
        fields = ("username", "nickname", "tipo_usuario", "avatar", "fecha_nacimiento", "celular", "email", "direccion", "observaciones", "genero", "perfil_estudiante")
        read_only_fields = ("email", "username", "tipo_usuario")

    def update(self, instance, validated_data):
        estudiante = instance.perfil_estudiante
        if validated_data.get("perfil_estudiante"):
            data = validated_data.get("perfil_estudiante")


        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.celular = validated_data.get('celular', instance.celular)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.observaciones = validated_data.get('observaciones', instance.observaciones)
    
        if data:
            estudiante.institucion = data.get("institucion", estudiante.institucion)
            estudiante.grado = data.get("grado", estudiante.grado)
            estudiante.save()
        return instance


class UserDocenteModelSerializer(serializers.ModelSerializer):
    
    genero = GenerosSerializer(required=False)
    perfil_docente = DocenteModelSerializer(required=False)

    class Meta:
        model = User
        fields = ("username", "nickname", "tipo_usuario", "avatar", "fecha_nacimiento", "celular", "email", "direccion", "observaciones", "genero", "perfil_docente")
        read_only_fields = ("username", "email",  "tipo_usuario", "fecha_nacimiento", "genero", "perfil_docente")

    
    def update(self, instance, validated_data):
        docente = instance.perfil_docente
        if validated_data.get("perfil_docente"):
            data = validated_data.get("perfil_docente")

        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.celular = validated_data.get('celular', instance.celular)
        instance.direccion = validated_data.get('direccion', instance.direccion)
        instance.observaciones = validated_data.get('observaciones', instance.observaciones)

        if data:
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

    
class UserTutorModelSerializer(serializers.ModelSerializer):
    genero = GenerosSerializer(required=False)
    perfil_tutor = TutorModelSerializer(required=False)

    class Meta:
        model = User
        fields = ("username","nickname", "tipo_usuario", "avatar", "fecha_nacimiento", "celular", "email", "direccion", "observaciones", "genero", "perfil_tutor")
        read_only_fields = ("email", "username", "tipo_usuario", "fecha_nacimiento", "genero", "perfil_tutor")
