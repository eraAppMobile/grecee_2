# Generated by Django 4.0.3 on 2022-03-22 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_image_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='id',
        ),
        migrations.AlterField(
            model_name='image',
            name='answer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.answer'),
        ),
    ]
