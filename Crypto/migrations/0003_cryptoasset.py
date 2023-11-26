# Generated by Django 4.2.7 on 2023-11-21 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crypto', '0002_historicalprice'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=5, max_digits=20)),
                ('high', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('low', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('price_change_24h', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('price_change_percentage_24h', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('market_cap', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('volume_24h', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
                ('circulating_supply', models.DecimalField(blank=True, decimal_places=5, max_digits=20, null=True)),
            ],
        ),
    ]