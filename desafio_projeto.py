menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
LIMITE_SAQUES = 3
quantidade_saque = 0

while True:

    opcao = input(menu)

    if opcao == 'd':
        valor_deposito = float(input("Digite o valor que você quer depositar (somente números): "))
        while valor_deposito <= 0:
            valor_deposito = float(input("Não é possível depositar valores negativos ou zero, favor digite novo valor positivo (somente números): "))
        saldo += valor_deposito
        extrato += f"Depósito - R$ {valor_deposito:.2f}\n"
        print(f"Foram depositados R$ {valor_deposito:.2f}")
        continue

    elif opcao == 's':
        if quantidade_saque < LIMITE_SAQUES:
            valor_saque = float(input("Digite um valor de saque abaixo de R$ 500,00: "))
            while valor_saque <= 0:
                valor_saque = float(input("Não é possível sacar valores negativos ou zero, digite outro valor: "))
            while valor_saque > limite:
                valor_saque = float(input("Não é possível sacar mais de R$ 500,00, digite um valor menor: "))
                while valor_saque <= 0:
                    valor_saque = float(input("Não é possível sacar valores negativos ou zero, digite outro valor: "))
            if valor_saque > saldo:
                print(f"Não é possível sacar R$ {valor_saque:.2f}, uma vez que o saldo de sua conta é de R$ {saldo:.2f}")
            saldo -= valor_saque
            quantidade_saque += 1
            extrato += f"Saque - R$ {valor_saque:.2f}\n"
            print(f"Foram sacados R$ {valor_saque:.2f}")
        else:
            print("Você já fez 3 saques na data de hoje, não é possível sacar mais.")
        
        continue

    elif opcao == 'e':
        print(f'''
Extrato de sua conta
--------------------
{extrato}
--------------------
Saldo - R$ {saldo:.2f}\n
''')
        continue

    elif opcao == 'q':
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")