# Generated by Django 3.2.5 on 2021-07-15 08:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=40)),
                ('picture', models.ImageField(upload_to='restaurant_pictures')),
                ('minimum_order_cost', models.IntegerField()),
                ('minimum_delivery_cost', models.IntegerField()),
                ('telephone_number', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(9)])),
                ('description', models.TextField()),
                ('notice', models.TextField()),
                ('origin_information', models.TextField()),
                ('nuturition_facts', models.TextField()),
                ('allergens_facts', models.TextField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MenuInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=100)),
                ('picture', models.ImageField(upload_to='menu_pictures')),
                ('price', models.PositiveIntegerField()),
                ('is_available', models.BooleanField(default=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('address', models.CharField(max_length=40)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('restaurant', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BusinessInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('owner_name', models.CharField(max_length=5)),
                ('business_name', models.CharField(max_length=40)),
                ('business_registration_number', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(10)])),
                ('restaurant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='restaurant.restaurant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
