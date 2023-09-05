# Generated by Django 4.2.4 on 2023-09-03 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car', '0001_initial'),
        ('user', '0001_initial'),
        ('maintenance', '0002_alter_maintenancecenter_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserReviews', to='user.profile'),
        ),
        migrations.AddField(
            model_name='pricehistory',
            name='car',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='price_history', to='car.car'),
        ),
        migrations.AddField(
            model_name='positiveaspect',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positive_aspects', to='car.car'),
        ),
        migrations.AddField(
            model_name='negativeaspect',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='negative_aspects', to='car.car'),
        ),
        migrations.AddField(
            model_name='interiorimage',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interior_images', to='car.car'),
        ),
        migrations.AddField(
            model_name='exteriorimage',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exterior_images', to='car.car'),
        ),
        migrations.AddField(
            model_name='car',
            name='maintenance_centers',
            field=models.ManyToManyField(blank=True, default=None, related_name='maintenance_centers', to='maintenance.maintenancecenter'),
        ),
        migrations.AddField(
            model_name='car',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_cars', to='user.profile'),
        ),
        migrations.AddField(
            model_name='car',
            name='tags',
            field=models.ManyToManyField(blank=True, default=None, related_name='tags', to='car.tag'),
        ),
        migrations.AddField(
            model_name='car',
            name='tech_and_safety_features',
            field=models.ManyToManyField(blank=True, default=None, related_name='cars', to='car.techandsafetyfeatures'),
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.CheckConstraint(check=models.Q(('release_year__gte', 1900), ('release_year__lte', 2025)), name='valid_release_year'),
        ),
    ]