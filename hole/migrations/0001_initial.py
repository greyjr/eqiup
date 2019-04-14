# Generated by Django 2.0 on 2019-02-15 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_area', models.CharField(max_length=100)),
                ('picture_area', models.BinaryField()),
                ('description_area', models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name='Equip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_equip', models.CharField(max_length=50)),
                ('short_name', models.CharField(max_length=20, unique=True)),
                ('station_number', models.IntegerField()),
                ('picture_equip', models.BinaryField()),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hole.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Ie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ie', models.CharField(max_length=20)),
                ('content_ie', models.CharField(max_length=65535)),
            ],
        ),
        migrations.CreateModel(
            name='Reset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('time', models.TimeField()),
                ('comment', models.CharField(max_length=2048)),
                ('equip_short_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hole.Equip')),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
                ('surname_name', models.CharField(max_length=255)),
                ('profession', models.CharField(max_length=100)),
                ('area_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hole.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='reset',
            name='new_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hole.Status'),
        ),
        migrations.AddField(
            model_name='equip',
            name='ie_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hole.Ie'),
        ),
    ]
