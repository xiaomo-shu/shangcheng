# Generated by Django 2.1 on 2020-02-26 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_manage', '0006_yzyiso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yzyiso',
            name='sys_type',
        ),
        migrations.AddField(
            model_name='yzyiso',
            name='os_type',
            field=models.CharField(default='Other', max_length=64),
        ),
        migrations.AlterField(
            model_name='yzyiso',
            name='type',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='yzynodes',
            name='cpu_info',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='yzynodes',
            name='mem_info',
            field=models.CharField(max_length=100, null=True),
        ),
    ]