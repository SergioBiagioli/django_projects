# Generated by Django 4.2.7 on 2024-06-10 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicles', '0014_category_created_at_category_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aplication',
            name='market',
            field=models.CharField(choices=[('US', 'United States'), ('EU', 'Europe'), ('ARG', 'Argentina'), ('AU', 'Australia')], default='US', max_length=3),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AplicationPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('photo', models.ImageField(upload_to='aplication_photos/')),
                ('aplication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='vehicles.aplication')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_%(class)s_set', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='updated_%(class)s_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]