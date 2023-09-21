import textwrap
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty


class Conta:
    def __init__(self, _numero, _cliente):
        self._saldo = 0
        self._numero = _numero
        self._agencia = "0001"
        self._cliente = _cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        if valor > self.saldo:
            print(f"Não é possível sacar R$ {valor:.2f}, uma vez que o saldo de sua conta é de R$ {self.saldo:.2f}")
            return False
        else:
            self._saldo -= valor
            print(f"Foram sacados R$ {valor:.2f}")
            return True
       

    
    def depositar(self, valor):
        while valor <= 0:
            valor = float(input("Não é possível depositar valores negativos ou zero, favor digite novo valor positivo (somente números): "))
        self._saldo += valor
        print(f"Foram depositados R$ {valor:.2f}")
        return True
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, _limite=500, _limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = _limite
        self._limite_saques = _limite_saques

    @property
    def limite_saques(self):
        return self._limite_saques
    
    @property
    def limite(self):
        return self._limite
    
    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if numero_saques < self.limite_saques:
            while valor <= 0:
                valor = float(input("Não é possível sacar valores negativos ou zero, digite outro valor: "))
            while valor > self.limite:
                valor = float(input("Não é possível sacar mais de R$ 500,00, digite um valor menor: "))
                while valor <= 0:
                    valor = float(input("Não é possível sacar valores negativos ou zero, digite outro valor: "))
            
            return super().sacar(valor)
        else:
            print("Você já fez 3 saques na data de hoje, não é possível sacar mais.")
            return False
        
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Cliente:
    def __init__(self, _endereco):
        self._endereco = _endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, _cpf, _nome, _data_nascimento, _endereco):
        self._cpf = _cpf
        self._nome = _nome
        self._data_nascimento = _data_nascimento
        super().__init__(_endereco)
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def nome(self):
        return self._nome
   

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, Conta):
        pass


class Deposito(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, _valor):
        self._valor = _valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
    

class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )



def main():
    clientes = []
    contas = []
    menu = """

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [u] Cadastrar Usuário
    [c] Cadastrar Conta Corrente
    [l] Listar Usuários e contas
    [q] Sair

    => """

    while True:

        opcao = input(menu)

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'q':
            break

        elif opcao =='u':
            cadastrar_cliente(clientes)

        elif opcao == 'c':
            numero_conta = len(contas) + 1
            cadastrar_conta(numero_conta, clientes, contas)

        elif opcao == 'l':
            listar_contas(contas)

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


def sacar(clientes):
    cpf = informa_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    conta = recuperar_conta_cliente(cliente)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
    cpf = informa_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    conta = recuperar_conta_cliente(cliente)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    
    if not Conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = []
    for cliente in clientes:
        if cliente.cpf == cpf:
            clientes_filtrados.append(cliente)
    if clientes_filtrados:
        return clientes_filtrados[0]
    else:
        None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return
    else:
        return cliente.contas[0]


def exibir_extrato(clientes):
    cpf = informa_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    conta = recuperar_conta_cliente(cliente)
    transacoes = conta.historico.transacoes
    extrato = ""

    if not cliente:
        print("\nCliente não encontrado!")

    if not conta:
        return
    
    print("\n---------------EXTRATO-------------")

    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}: \n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")


def cadastrar_conta(numero_conta, clientes, contas):
    cpf = informa_cpf()
    cliente = filtrar_cliente(cpf, clientes)
    
    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def cadastrar_cliente(clientes):
    cpf = informa_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe um cliente com o CPF cadastrado!")
        return
    
    nome_usuario = input("Digite o nome do usuário\n")
    data_nascimento = input("Digite a Data de Nascimento do Usuário\n")
    logradouro =  input("Digite o logradouro do usuário\n")
    numero_logradouro = input("Digite o número da residência\n")
    bairro = input("Digite o bairro\n")
    cidade = input("Digite a cidade\n")
    estado = input("Digite o Estado\n")
    endereco = logradouro + ", " + numero_logradouro + " - " + bairro + " - " + cidade + "/" + estado
    cliente = PessoaFisica(cpf, nome_usuario, data_nascimento, endereco)

    clientes.append(cliente)

    print("\nCliente criado com sucesso")

def informa_cpf():
    cpf_informado = input("Informe o CPF (somente número):\n")
    cpf_informado = cpf_informado.replace(".", "").replace("-", "")
    return cpf_informado



main()