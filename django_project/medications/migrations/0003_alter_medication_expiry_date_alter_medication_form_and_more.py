# Generated by Django 5.1.3 on 2024-11-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medications', '0002_alter_medication_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medication',
            name='expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medication',
            name='form',
            field=models.CharField(choices=[('tablet', 'Tablet'), ('capsules', 'Capsules'), ('liquid', 'Liquid'), ('topical', 'Topical'), ('drops', 'Drops'), ('suppositories', 'Suppositories'), ('inhalers', 'Inhalers'), ('injections', 'Injections'), ('others', 'Others')], max_length=100),
        ),
        migrations.AlterField(
            model_name='medication',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]