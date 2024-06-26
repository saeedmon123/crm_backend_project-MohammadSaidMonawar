# Generated by Django 5.0.6 on 2024-06-04 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0022_alter_loyaltythreshold_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loyaltythreshold',
            name='points_for_next_tier',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='loyaltythreshold',
            name='tier_discount',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='loyaltythreshold',
            name='tier_name',
            field=models.JSONField(),
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
