# Generated by Django 4.2.4 on 2023-08-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceCenter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('brand', models.CharField(choices=[('Acura', 'Acura'), ('Alfa Romeo', 'Alfa Romeo'), ('Aston Martin', 'Aston Martin'), ('Audi', 'Audi'), ('BMW', 'BMW'), ('Bentley', 'Bentley'), ('Buick', 'Buick'), ('Cadillac', 'Cadillac'), ('Chevrolet', 'Chevrolet'), ('Chrysler', 'Chrysler'), ('Daewoo', 'Daewoo'), ('Daihatsu', 'Daihatsu'), ('Dodge', 'Dodge'), ('Eagle', 'Eagle'), ('FIAT', 'FIAT'), ('Ferrari', 'Ferrari'), ('Fisker', 'Fisker'), ('Ford', 'Ford'), ('Freightliner', 'Freightliner'), ('GMC', 'GMC'), ('Genesis', 'Genesis'), ('Geo', 'Geo'), ('HUMMER', 'HUMMER'), ('Honda', 'Honda'), ('Hyundai', 'Hyundai'), ('INFINITI', 'INFINITI'), ('Isuzu', 'Isuzu'), ('Jaguar', 'Jaguar'), ('Jeep', 'Jeep'), ('Kia', 'Kia'), ('Lamborghini', 'Lamborghini'), ('Land Rover', 'Land Rover'), ('Lexus', 'Lexus'), ('Lincoln', 'Lincoln'), ('Lotus', 'Lotus'), ('MAZDA', 'MAZDA'), ('MINI', 'MINI'), ('Maserati', 'Maserati'), ('Maybach', 'Maybach'), ('McLaren', 'McLaren'), ('Mercedes-Benz', 'Mercedes-Benz'), ('Mercury', 'Mercury'), ('Mitsubishi', 'Mitsubishi'), ('Nissan', 'Nissan'), ('Oldsmobile', 'Oldsmobile'), ('Panoz', 'Panoz'), ('Plymouth', 'Plymouth'), ('Polestar', 'Polestar'), ('Pontiac', 'Pontiac'), ('Porsche', 'Porsche'), ('Ram', 'Ram'), ('Rivian', 'Rivian'), ('Rolls-Royce', 'Rolls-Royce'), ('SRT', 'SRT'), ('Saab', 'Saab'), ('Saturn', 'Saturn'), ('Scion', 'Scion'), ('Subaru', 'Subaru'), ('Suzuki', 'Suzuki'), ('Tesla', 'Tesla'), ('Toyota', 'Toyota'), ('Volkswagen', 'Volkswagen'), ('Volvo', 'Volvo'), ('smart', 'smart')], max_length=50, null=True)),
                ('contact_number', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]