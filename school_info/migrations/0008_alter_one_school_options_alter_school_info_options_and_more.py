# Generated by Django 4.2 on 2023-04-24 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_info', '0007_one_school_pictures'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='one_school',
            options={'ordering': ['id'], 'verbose_name': '学校详细信息', 'verbose_name_plural': '学校详细信息'},
        ),
        migrations.AlterModelOptions(
            name='school_info',
            options={'ordering': ['id'], 'verbose_name': '学校基本信息', 'verbose_name_plural': '学校基本信息'},
        ),
        migrations.AlterModelOptions(
            name='school_score',
            options={'ordering': ['id'], 'verbose_name': '学校分数', 'verbose_name_plural': '学校分数'},
        ),
    ]
