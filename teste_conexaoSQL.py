import pyodbc

conexao = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=Samtop;"
    "DATABASE=RaizesDoNordeste;"
    "Trusted_Connection=yes;"
)

print("Conexão realizada com sucesso!")