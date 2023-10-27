"""
    Desafio Python DIO Pymongo.
"""

from pymongo.mongo_client import MongoClient
from pprint import pprint
from urllib.parse import quote_plus


# Conecta ao servidor local
nome_usuario = quote_plus('') # aqui vai o usuário
senha = quote_plus('') # aqui vai a senha
uri = "mongodb+srv://" + nome_usuario + ":" + senha + "@cluster0.kww6ztf.mongodb.net/?retryWrites=true&w=majority"
cliente = MongoClient(uri)
banco = cliente.banco

# Verifica o status do servidor
try:
    cliente.admin.command('ping')
    print("Ping confirmado. Você está conectado ao MongoDB!")
except Exception as e:
    print(e)

# Criando coleção
banco.bank

# Criando objetos com dados a serem persistidos no banco
objeto_cliente = {
    "nome": "Daniel Silva",
    "cpf": "00000000",
    "endereco": "Rua 1",
    "conta": {
        "tipo": "corrente",
        "agencia": "0001",
        "num": 1,
        "saldo": "100.00",
        "cliente_id": 1
    }
}


# Persistindo dados no banco
cliente_id = banco.bank.insert_one(objeto_cliente).inserted_id

# Localizando dados nas coleções
daniel = banco.bank.find_one({"nome": "Daniel Silva"})
print(daniel)
