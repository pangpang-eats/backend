# Generated by Django 3.2.5 on 2021-07-05 07:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
        ('order', '0002_selection_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='selection',
            name='orderer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='purchased_credit_card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.creditcard'),
        ),
        migrations.AddField(
            model_name='order',
            name='selections',
            field=models.ManyToManyField(to='order.Selection'),
        ),
    ]
