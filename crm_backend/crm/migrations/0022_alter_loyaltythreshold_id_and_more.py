# Generated by Django 5.0.6 on 2024-06-04 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_remove_loyaltythreshold_bonus_points_on_birthday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loyaltythreshold',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='discount',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='price',
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='types',
            field=models.JSONField(default=list),
        ),
    ]