# Generated by Django 2.1.5 on 2019-03-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_student_profilecompleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='aptitude',
            field=models.SmallIntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='student',
            name='cpi',
            field=models.SmallIntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to='profile_pics'),
        ),
    ]
