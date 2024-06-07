# Generated by Django 5.0.6 on 2024-06-04 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0023_alter_loyaltythreshold_points_for_next_tier_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loyaltythreshold',
            name='last_updated',
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
