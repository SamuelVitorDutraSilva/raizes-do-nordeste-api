# Raízes do Nordeste API

API REST desenvolvida em Python e Flask para gerenciamento de clientes, produtos, pedidos e pagamentos da franquia Raízes do Nordeste.

## Tecnologias Utilizadas

* Python
* Flask
* Flask-JWT-Extended (JWT)
* Microsoft SQL Server
* PyODBC
* GitHub

## Como Executar

### Instalar dependências

```bash
pip install flask pyodbc flask-jwt-extended
```

### Configurar o banco de dados

Criar o banco de dados RaizesDoNordeste no Microsoft SQL Server e executar os scripts de criação das tabelas.

### Executar a aplicação

```bash
python app.py
```

A API será iniciada em:

```text
http://127.0.0.1:5000
```

## Endpoints

| Método | Endpoint    | Descrição            |
| ------ | ----------- | -------------------- |
| POST   | /login      | Autenticação JWT     |
| GET    | /produtos   | Consultar produtos   |
| GET    | /clientes   | Consultar clientes   |
| POST   | /clientes   | Cadastrar cliente    |
| GET    | /pedidos    | Consultar pedidos    |
| POST   | /pedidos    | Criar pedido         |
| GET    | /pagamentos | Consultar pagamentos |
| POST   | /pagamentos | Registrar pagamento  |

## Autenticação

A API utiliza autenticação JWT.

Fluxo:

1. Realizar login através do endpoint `/login`
2. Receber o token JWT
3. Informar o token no cabeçalho `Authorization` utilizando o padrão `Bearer Token`
4. Acessar os endpoints protegidos

## Autor

Samuel Vitor Dutra Silva

