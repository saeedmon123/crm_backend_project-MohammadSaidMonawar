# Generated by Django 5.0.6 on 2024-06-03 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('crm', '0015_alter_interaction_responsible_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='interaction_type',
            field=models.CharField(choices=[('Phone_Call', 'Phone Call'), ('Email', 'Email'), ('Meeting', 'Meeting')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='participant_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='interaction',
            name='participant_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
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
