# Generated by Django 4.0rc1 on 2021-11-27 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10, verbose_name='Nome')),
                ('value', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Papel',
                'verbose_name_plural': 'Papeis',
            },
        ),
        migrations.RemoveField(
            model_name='stockasset',
            name='name',
        ),
        migrations.AddField(
            model_name='stockasset',
            name='ticket',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='core.ticket', verbose_name='Papel'),
            preserve_default=False,
        ),
    ]
