"""
    Desafio Python DIO SQL Alchemy.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    DECIMAL
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base
)


engine = create_engine('sqlite:///:memory:', echo=True)

Sessao = sessionmaker(bind=engine)
sessao = Sessao()

Base = declarative_base()


class Cliente(Base):
    """
    Classe cliente do banco de dados com os seguintes campos.
    nome = String
    cpf = string(9)
    endereco = string(9)
    """
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    def __repr__(self):
        return f'Cliente: {self.nome}'


class Conta(Base):
    """
    Classe conta do banco de dados com os seguintes campos.

    tipo = string
    agencia = string
    num = integer
    id_cliente = chave estrangeira relacionada à classe Cliente
    saldo = decimal
    """
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey('cliente.id'))
    saldo = Column(DECIMAL)

    def __repr__(self):
        return f'Conta: {self.num}\nAgência: {self.agencia}\nCliente: {self.id_cliente}'


# Criando as tabelas dentro do banco
Base.metadata.create_all(engine)

# Criando novos registros
cliente = Cliente(nome='Daniel Silva', cpf='000000000', endereco='Rua 1')
conta = Conta(tipo='corrente', agencia='0001', num='1', id_cliente=1, saldo=100.0)

# Persistindo registros no banco
sessao.add(cliente)
sessao.add(conta)
sessao.commit()

# Criando consulta ao banco
consulta_usuario = sessao.query(Cliente).filter(Cliente.nome.like('%Daniel%'))
consulta_conta = sessao.query(Conta).filter(Conta.id_cliente.like(1))

print(consulta_usuario.all())
print(consulta_conta.all())
