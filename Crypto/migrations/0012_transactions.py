# Generated by Django 4.2.5 on 2023-11-29 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crypto', '0011_userdetails_identity_userdetails_identity_uploaded'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('tranType', models.CharField(max_length=100)),
                ('symbol', models.CharField(max_length=10)),
                ('unit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
