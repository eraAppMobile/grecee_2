# Generated by Django 4.0.3 on 2022-03-25 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_delete_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categorycode', models.TextField(blank=True, db_column='CategoryCode', null=True)),
                ('categorydescription', models.TextField(blank=True, db_column='CategoryDescription', null=True)),
                ('categorydisplaycode', models.TextField(blank=True, db_column='CategoryDisplayCode', null=True)),
                ('categoryid', models.IntegerField(blank=True, db_column='CategoryID', null=True)),
                ('categorydisplayindex', models.TextField(blank=True, db_column='CategoryDisplayIndex', null=True)),
                ('categorynewid', models.TextField(blank=True, db_column='CategoryNewID', primary_key=True, serialize=False)),
                ('comments', models.TextField(blank=True, db_column='Comments', null=True)),
                ('categorylevelindex', models.TextField(blank=True, db_column='CategoryLevelIndex', null=True)),
                ('displayorder', models.TextField(blank=True, db_column='DisplayOrder', null=True)),
                ('children', models.TextField(blank=True, db_column='Children', null=True)),
                ('strinternalgroupcode', models.TextField(blank=True, db_column='strInternalGroupCode', null=True)),
                ('strorigin', models.IntegerField(blank=True, db_column='strOrigin', null=True)),
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
        ),
    ]
