from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

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

# Verifica se a API está funcionando
@app.route('/')
def home():
    return 'API Raizes do Nordeste funcionando'


# ==========================================
# PRODUTOS
# ==========================================

# Retorna todos os produtos cadastrados
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

    # Retorna os dados em formato JSON
    return jsonify(produtos)


# ==========================================
# CLIENTES
# ==========================================

# Retorna todos os clientes cadastrados
@app.route('/clientes')
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

    # Retorna os dados em formato JSON
    return jsonify(clientes)


# Cadastra um novo cliente
@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():

    # Recebe os dados enviados pelo Postman
    dados = request.get_json()

    nome = dados['nome']
    email = dados['email']
    telefone = dados['telefone']

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO CLIENTE (nome, email, telefone)
        VALUES (?, ?, ?)
    """, nome, email, telefone)

    # Salva as alterações no banco
    conexao.commit()

    return jsonify({
        "mensagem": "Cliente cadastrado com sucesso"
    }), 201


# ==========================================
# PEDIDOS
# ==========================================

# Retorna todos os pedidos cadastrados
@app.route('/pedidos')
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

    # Retorna os dados em formato JSON
    return jsonify(pedidos)


# Cria um novo pedido para um cliente
@app.route('/pedidos', methods=['POST'])
def cadastrar_pedido():

    # Recebe os dados enviados pelo Postman
    dados = request.get_json()

    id_cliente = dados['id_cliente']
    valor_total = dados['valor_total']

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO PEDIDO
        (id_cliente, valor_total)
        VALUES (?, ?)
    """, id_cliente, valor_total)

    # Salva as alterações no banco
    conexao.commit()

    return jsonify({
        "mensagem": "Pedido criado com sucesso"
    }), 201


# ==========================================
# INICIALIZAÇÃO DA API
# ==========================================

# Executa a aplicação Flask em modo de desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)