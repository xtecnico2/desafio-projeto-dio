import random


menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[u] Cadastrar Usuário
[c] Cadastrar Conta Corrente
[l] Listar Usuários e contas
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
LIMITE_SAQUES = 3
quantidade_saque = 0
usuarios = {}
contas_correntes = {}


def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques < LIMITE_SAQUES:
        # valor_saque = float(input("Digite um valor de saque abaixo de R$ 500,00: "))
        while valor <= 0:
            valor = float(input("Não é possível sacar valores negativos ou zero, digite outro valor: "))
        while valor > limite:
            valor = float(input("Não é possível sacar mais de R$ 500,00, digite um valor menor: "))
            while valor <= 0:
                valor = float(input("Não é possível sacar valores negativos ou zero, digite outro valor: "))
        if valor > saldo:
            print(f"Não é possível sacar R$ {valor:.2f}, uma vez que o saldo de sua conta é de R$ {saldo:.2f}")
        saldo -= valor
        quantidade_saque += 1
        extrato += f"Saque - R$ {valor:.2f}\n"
        print(f"Foram sacados R$ {valor:.2f}")
    else:
        print("Você já fez 3 saques na data de hoje, não é possível sacar mais.")

    return saldo, extrato


def depositar(saldo, valor, extrato):
    # valor_deposito = float(input("Digite o valor que você quer depositar (somente números): "))
    while valor <= 0:
        valor = float(input("Não é possível depositar valores negativos ou zero, favor digite novo valor positivo (somente números): "))
    saldo += valor
    extrato += f"Depósito - R$ {valor:.2f}\n"
    print(f"Foram depositados R$ {valor:.2f}")

    return saldo, extrato


def exibir_extrato(saldo, extrato=extrato):
    return f'''
        Extrato de sua conta
        --------------------
        {extrato}
        --------------------
        Saldo - R$ {saldo:.2f}\n
    '''


def cadastrar_usuario(nome, nascimento, cpf: str, logradouro, numero, bairro, cidade, estado):
    cpf = cpf.replace(".", "").replace("-", "")
    for chave in usuarios.keys():
        if chave == cpf:
            return print("Usuário já cadastrado")
        
    usuario = {
        cpf: 
            {
             "Nome": nome,
             "CPF": cpf,
             "Data de Nascimento": nascimento,
             "Endereço": logradouro + ", " + numero + " - " + bairro + " - " + cidade + "/" + estado,
            }
        }
    
    usuarios.update(usuario)
    
    return usuarios


def cadastrar_conta(usuario):
    for chave, valor in usuarios.items():
        if usuario != chave:
            return print("Usuário não cadastrado.")
    conta_corrente = {
        random.randint(0, 10000000000): {
            "Numero da Conta": len(contas_correntes) + 1,
            "Numedo da Agencia": "0001",
            "CPF do Titular": usuario
        }
    }

    contas_correntes.update(conta_corrente)

    return contas_correntes



while True:

    opcao = input(menu)

    if opcao == 'd':
        valor_deposito = float(input("Digite o valor que você quer depositar (somente números): "))
        saldo_temp, extrato_temp = depositar(saldo, valor_deposito, extrato)
        saldo += saldo_temp
        extrato += extrato_temp

        continue

    elif opcao == 's':
        valor_saque = float(input("Digite um valor de saque abaixo de R$ 500,00: "))
        saldo_temp, extrato_temp = sacar(saldo=saldo, valor=valor_saque, extrato=extrato, limite=limite, numero_saques=quantidade_saque, limite_saques=LIMITE_SAQUES)
        saldo += saldo_temp
        extrato += extrato_temp
        
        continue

    elif opcao == 'e':
        exibir_extrato(saldo, extrato=extrato)
        
        continue

    elif opcao == 'q':
        break

    elif opcao =='u':
        nome_usuario = input("Digite o nome do usuário\n")
        data_nascimento = input("Digite a Data de Nascimento do Usuário\n")
        cpf = input("Digite o CPF do usuário\n")
        logradouro =  input("Digite o logradouro do usuário\n")
        numero_logradouro = input("Digite o número da residência\n")
        bairro = input("Digite o bairro\n")
        cidade = input("Digite a cidade\n")
        estado = input("Digite o Estado\n")
        cadastrar_usuario(nome_usuario, data_nascimento, cpf, logradouro, numero_logradouro, bairro, cidade, estado)

    elif opcao == 'c':
        cpf_usuario_conta = input("Digite o cpf do usuário da conta corrente\n")
        cadastrar_conta(cpf_usuario_conta)

    elif opcao == 'l':
        print(f"Usuários:\n{usuarios}\n\nContas Correntes\n{contas_correntes}")

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")