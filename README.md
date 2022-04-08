# mywallet

Cadastre seus ativos e veja a melhor oportunidade de compra com base nas suas metas pré-definidas.

## Como usar

1. Crie um ambiente virtual para o projeto:

```shell
poetry shell
```

2. Instale as dependencias do projeto:

```shell
poetry install
```

3. Crie seu banco de dados e rode as migrações:

```shell
python manage.py migrate
```

4. Crie um usuario para acessar o admin:

```shell
python manage.py createsuperuser
```

5. Execute o servidor local:

```shell
python manage.py runserver
```


## Atualizando preço das ações

Rode o comando para atualizar:

```shell
python manage.py sync_tickets_prices
```
