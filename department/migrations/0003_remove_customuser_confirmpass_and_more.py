# Generated by Django 5.0.4 on 2024-04-16 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0002_customuser_confirmpass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='confirmPass',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='allocation_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='userType',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Project_Manager', 'Project_Manager'), ('Team_Leader', 'Team_Leader'), ('Employee', 'Employee')], max_length=100),
        ),
    ]
