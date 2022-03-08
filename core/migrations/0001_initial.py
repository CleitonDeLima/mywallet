# Generated by Django 4.0.2 on 2022-02-24 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=10, verbose_name='Nome')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor')),
                ('type', models.PositiveSmallIntegerField(choices=[(0, 'Ação'), (1, 'FII'), (2, 'BDR'), (3, 'ETF')], verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Papel',
                'verbose_name_plural': 'Papeis',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Carteira',
                'verbose_name_plural': 'Carteiras',
            },
        ),
        migrations.CreateModel(
            name='WalletItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('started_in', models.DateField(blank=True, null=True, verbose_name='Início')),
                ('closed_in', models.DateField(blank=True, null=True, verbose_name='Encerrado')),
                ('allocation', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Alocação')),
                ('entry_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Preço de Entrada')),
                ('ceiling_price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Preço Teto')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ticker', verbose_name='Papel')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.wallet', verbose_name='Carteira')),
            ],
            options={
                'verbose_name': 'Item da Carteira',
                'verbose_name_plural': 'Itens da Carteira',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date', models.DateField(verbose_name='Data da Negociação')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Valor Unitário')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantidade')),
                ('order', models.CharField(choices=[('b', 'Compra'), ('s', 'Venda')], max_length=1, verbose_name='Ordem')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.ticker', verbose_name='Papel')),
                ('wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='core.wallet', verbose_name='Carteira')),
            ],
            options={
                'verbose_name': 'Transação',
                'verbose_name_plural': 'Transações',
            },
        ),
    ]
