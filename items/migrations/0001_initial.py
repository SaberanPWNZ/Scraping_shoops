# Generated by Django 5.1.3 on 2024-11-14 07:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статуси',
            },
        ),
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Гарантія',
                'verbose_name_plural': 'Гарантії',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('article', models.CharField(max_length=40, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='startup_logos/')),
                ('partner_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rrp_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ean', models.CharField(blank=True, max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.category')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.status')),
                ('warranty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='items.warranty')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товари',
            },
        ),
    ]