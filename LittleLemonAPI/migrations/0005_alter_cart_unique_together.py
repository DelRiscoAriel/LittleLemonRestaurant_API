# Generated by Django 5.0.6 on 2024-07-20 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0004_alter_cart_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set(),
        ),
    ]