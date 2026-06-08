from flask import Flask
import pyodbc

app = Flask(__name__)

conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Samtop;"
    "DATABASE=RaizesDoNordeste;"
    "Trusted_Connection=yes;"
)

@app.route('/')
def home():
    return 'API Raizes do Nordeste funcionando'


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

    return produtos


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

    return clientes

if __name__ == '__main__':
    app.run(debug=True)