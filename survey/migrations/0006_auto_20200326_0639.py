# Generated by Django 3.0.3 on 2020-03-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_auto_20200326_0246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyanswer',
            name='postcode',
            field=models.IntegerField(default=1000, max_length=4),
        ),
    ]
