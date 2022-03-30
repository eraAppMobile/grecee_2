# Generated by Django 4.0.3 on 2022-03-22 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_image_id_alter_image_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='image', serialize=False, to='main.answer'),
        ),
    ]