import pyodbc

conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Samtop;"
    "DATABASE=RaizesDoNordeste;"
    "Trusted_Connection=yes;"
)

cursor = conexao.cursor()

cursor.execute("""
    SELECT id_produto, nome, preco
    FROM PRODUTO
""")

for produto in cursor.fetchall():
    print(produto)