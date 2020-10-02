# Generated by Django 3.0.10 on 2020-10-02 19:39

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ciudades', '0001_initial'),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='users/avatar', verbose_name='Foto de perfil')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('celular', models.CharField(blank=True, max_length=9, null=True)),
                ('tipo_usuario', models.CharField(blank=True, choices=[('ESTUDIANTE', 'Estudiante'), ('PROFESOR', 'Profesor'), ('TUTOR', 'Tutor')], max_length=100, null=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo electrónico')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breve_cv', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('filosofia', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='perfil_docente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Género',
                'verbose_name_plural': 'Géneros',
            },
        ),
        migrations.CreateModel(
            name='Nivel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', ckeditor.fields.RichTextField(default='', verbose_name='Descripción')),
                ('orden', models.PositiveIntegerField(blank=True, null=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='usuarios/niveles', verbose_name='Icono del nivel')),
            ],
            options={
                'verbose_name': 'Nivel',
                'verbose_name_plural': 'Niveles',
            },
        ),
        migrations.CreateModel(
            name='Institucion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='usuarios/institucion', verbose_name='Foto de la institucion')),
                ('ciudad', models.ForeignKey(blank=True, help_text='Campo que referencia a la ciudad de la instición', null=True, on_delete=django.db.models.deletion.CASCADE, to='ciudades.Ciudad')),
                ('nivel', models.ForeignKey(blank=True, help_text='Campo que referencia al nivel académico: Escolar, Preparatoria, Universidad', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Nivel')),
            ],
            options={
                'verbose_name': 'Institución',
                'verbose_name_plural': 'Instituciones',
            },
        ),
        migrations.CreateModel(
            name='HorarioLibreDocente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.DateTimeField(verbose_name='Fecha y hora del inicio del horario libre')),
                ('hora_fin', models.DateTimeField(verbose_name='Fecha y hora del fin del horario libre')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Docente', verbose_name='Horarios Libres del Docente')),
            ],
            options={
                'verbose_name': 'Horario Libre',
                'verbose_name_plural': 'Horarios Libres',
            },
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciclo_universidad', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('grado_colegio', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('institucion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.Institucion')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='perfil_estudiante', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='genero',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Genero', verbose_name='Género'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
