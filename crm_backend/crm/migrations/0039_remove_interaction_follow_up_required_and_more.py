# Generated by Django 5.0.6 on 2024-06-05 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0038_alter_order_order_message_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interaction',
            name='follow_up_required',
        ),
        migrations.AddField(
            model_name='interaction',
            name='follow_up_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interaction',
            name='follow_up_notes',
            field=models.TextField(blank=True),
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
