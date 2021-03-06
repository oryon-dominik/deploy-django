# Generated by Django 3.1.3 on 2020-11-21 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DeployProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.create_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.create_dt.verbose_name')),
                ('update_dt', models.DateTimeField(blank=True, editable=False, help_text='ModelTimetrackingMixin.update_dt.help_text', null=True, verbose_name='ModelTimetrackingMixin.update_dt.verbose_name')),
                ('logging_output', models.TextField(help_text='The output of the deployment')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
