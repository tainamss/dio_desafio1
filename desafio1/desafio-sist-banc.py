menu = '''
======MENU======
Escolha alguma das seguintes ações:
[s] Saque
[d] Depósito 
[e] Extrato
[q] Sair
>>>
'''

saldo = 0
limite_saque = 500
extrato = ''
quant_saques = 0

while True:
    opcao = input(menu)

    if opcao == 's':
        saque = int(input("Digite o valor que deseja sacar: "))
        if saque <= saldo and saque <= limite_saque:
            saldo -= saque
            extrato_att = f'Saque no valor de R${saque}\nSaldo atual: R${saldo}.\n'
            extrato += extrato_att
        elif saque > limite_saque:
            print("O valor do saque excede o limite permitido por saque de R$500.00")
        elif saque > saldo:
            print("Saldo insuficiente!")

    elif opcao == 'd':
        deposito = int(input("Digite o valor que deseja depositar: "))
        saldo += deposito
        extrato_att = f'Deposito no valor de R${deposito}\nSaldo atual: R${saldo}.\n'
        extrato += extrato_att

    elif opcao == 'e':
        print("\n====== EXTRATO ======")
        print(extrato if extrato else "Nenhuma movimentação realizada.")
        print("=====================\n")

    elif opcao == 'q':
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")

        


    