from flask import Flask, request, jsonify
import pyodbc

app = Flask(__name__)

conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Samtop;"
    "DATABASE=RaizesDoNordeste;"
    "Trusted_Connection=yes;"
)

# Página inicial
@app.route('/')
def home():
    return 'API Raizes do Nordeste funcionando'


# Listar produtos
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


# Listar clientes
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

    return jsonify(clientes)


# Cadastrar cliente
@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():

    dados = request.get_json()

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


if __name__ == '__main__':
    app.run(debug=True)