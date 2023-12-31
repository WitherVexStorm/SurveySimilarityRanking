# Generated by Django 4.2.5 on 2023-09-13 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('survey_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('survey_name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Similarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey')),
                ('user_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_1', to=settings.AUTH_USER_MODEL)),
                ('user_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=50)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.survey')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField(choices=[(0, 'NONE'), (1, 'ONE'), (2, 'TWO'), (3, 'THREE'), (4, 'FOUR'), (5, 'FIVE'), (6, 'SIX'), (7, 'SEVEN'), (8, 'EIGHT'), (9, 'NINE'), (10, 'TEN')], default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
