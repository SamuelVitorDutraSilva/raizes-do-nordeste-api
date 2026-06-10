from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import pyodbc

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "chave-secreta-raizes-do-nordeste"
jwt = JWTManager(app)

# ==========================================
# Conexão com o banco de dados SQL Server
# ==========================================
conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Samtop;"
    "DATABASE=RaizesDoNordeste;"
    "Trusted_Connection=yes;"
)

# ==========================================
# ENDPOINT INICIAL
# ==========================================

@app.route('/')
def home():
    return 'API Raizes do Nordeste funcionando'


# ==========================================
# AUTENTICAÇÃO
# ==========================================

@app.route('/login', methods=['POST'])
def login():

    dados = request.get_json()

    email = dados['email']
    senha = dados['senha']

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_usuario, nome, email
        FROM USUARIO
        WHERE email = ? AND senha = ?
    """, email, senha)

    usuario = cursor.fetchone()

    if usuario is None:
        return jsonify({
            "erro": "E-mail ou senha inválidos"
        }), 401

    token = create_access_token(identity=str(usuario.id_usuario))

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "access_token": token
    }), 200


# ==========================================
# PRODUTOS
# ==========================================

@app.route('/produtos')
def listar_produtos():

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_produto, nome, preco
        FROM PRODUTO
    """)

    produtos = []

    for produto in cursor.fetchall():

        produtos.append({
            "id": produto.id_produto,
            "nome": produto.nome,
            "preco": float(produto.preco)
        })

    return jsonify(produtos)


# ==========================================
# CLIENTES
# ==========================================

@app.route('/clientes')
@jwt_required()
def listar_clientes():

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_cliente, nome, email, telefone
        FROM CLIENTE
    """)

    clientes = []

    for cliente in cursor.fetchall():

        clientes.append({
            "id": cliente.id_cliente,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone
        })

    return jsonify(clientes)


@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():

    dados = request.get_json()

    if not dados.get('nome'):
        return jsonify({
            "erro": "Campo nome é obrigatório"
        }), 422

    nome = dados['nome']
    email = dados['email']
    telefone = dados['telefone']

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO CLIENTE (nome, email, telefone)
        VALUES (?, ?, ?)
    """, nome, email, telefone)

    conexao.commit()

    return jsonify({
        "mensagem": "Cliente cadastrado com sucesso"
    }), 201


# ==========================================
# PEDIDOS
# ==========================================

@app.route('/pedidos')
@jwt_required()
def listar_pedidos():

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_pedido,
               id_cliente,
               data_pedido,
               status,
               valor_total
        FROM PEDIDO
    """)

    pedidos = []

    for pedido in cursor.fetchall():

        pedidos.append({
            "id_pedido": pedido.id_pedido,
            "id_cliente": pedido.id_cliente,
            "data_pedido": str(pedido.data_pedido),
            "status": pedido.status,
            "valor_total": float(pedido.valor_total)
        })

    return jsonify(pedidos)


@app.route('/pedidos', methods=['POST'])
@jwt_required()
def cadastrar_pedido():

    dados = request.get_json()

    id_cliente = dados['id_cliente']
    valor_total = dados['valor_total']

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_cliente
        FROM CLIENTE
        WHERE id_cliente = ?
    """, id_cliente)

    cliente = cursor.fetchone()

    if cliente is None:
        return jsonify({
            "erro": "Cliente não encontrado"
        }), 404

    cursor.execute("""
        INSERT INTO PEDIDO
        (id_cliente, valor_total)
        VALUES (?, ?)
    """, id_cliente, valor_total)

    conexao.commit()

    return jsonify({
        "mensagem": "Pedido criado com sucesso"
    }), 201


# ==========================================
# PAGAMENTOS
# ==========================================

@app.route('/pagamentos')
@jwt_required()
def listar_pagamentos():

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_pagamento,
               id_pedido,
               status,
               data_pagamento,
               metodo_pagamento
        FROM PAGAMENTO
    """)

    pagamentos = []

    for pagamento in cursor.fetchall():

        pagamentos.append({
            "id_pagamento": pagamento.id_pagamento,
            "id_pedido": pagamento.id_pedido,
            "status": pagamento.status,
            "data_pagamento": str(pagamento.data_pagamento),
            "metodo_pagamento": pagamento.metodo_pagamento
        })

    return jsonify(pagamentos)


@app.route('/pagamentos', methods=['POST'])
@jwt_required()
def cadastrar_pagamento():

    dados = request.get_json()

    id_pedido = dados['id_pedido']
    metodo_pagamento = dados['metodo_pagamento']
    aprovado = dados['aprovado']

    if aprovado == True:
        status_pagamento = 'APROVADO'
        status_pedido = 'PAGO'
    else:
        status_pagamento = 'RECUSADO'
        status_pedido = 'PAGAMENTO_RECUSADO'

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_pedido
        FROM PEDIDO
        WHERE id_pedido = ?
    """, id_pedido)

    pedido = cursor.fetchone()

    if pedido is None:
        return jsonify({
            "erro": "Pedido não encontrado"
        }), 404

    cursor.execute("""
        INSERT INTO PAGAMENTO
        (id_pedido, status, metodo_pagamento)
        VALUES (?, ?, ?)
    """, id_pedido, status_pagamento, metodo_pagamento)

    cursor.execute("""
        UPDATE PEDIDO
        SET status = ?
        WHERE id_pedido = ?
    """, status_pedido, id_pedido)

    conexao.commit()

    return jsonify({
        "mensagem": "Pagamento processado com sucesso",
        "status_pagamento": status_pagamento,
        "status_pedido": status_pedido
    }), 201


# ==========================================
# INICIALIZAÇÃO DA API
# ==========================================

if __name__ == '__main__':
    app.run(debug=True)