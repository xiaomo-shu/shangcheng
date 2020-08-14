# Generated by Django 2.1 on 2020-02-25 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YzyBaseImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(max_length=64, unique=True)),
                ('path', models.CharField(max_length=64, unique=True)),
                ('os_type', models.CharField(max_length=64)),
                ('size', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('publish', models.IntegerField(default=0)),
                ('deleted', models.IntegerField(default=0)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resource_pool', models.ForeignKey(db_column='pool_uuid', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='yzy_base_images', to='web_manage.YzyResourcePools', to_field='uuid')),
            ],
            options={
                'db_table': 'yzy_base_images',
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='yzynodes',
            name='data_img_uuid',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='yzynodes',
            name='sys_img_uuid',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='yzynodes',
            name='vm_data_uuid',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='yzynodes',
            name='vm_sys_uuid',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
