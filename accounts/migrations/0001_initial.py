# Generated by Django 4.2.3 on 2023-07-17 19:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('abbreviation', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=16, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('number', models.BigIntegerField(default=1000000000000000, null=True, validators=[django.core.validators.MinValueValidator(1000000000000000), django.core.validators.MaxValueValidator(9999999999999999)])),
                ('curency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='accounts.currency')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accounts', to='accounts.accounttype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
