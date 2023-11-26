
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cryptocurrency', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=5, max_digits=20)),
                ('date', models.DateField()),
            ],
        ),
    ]
