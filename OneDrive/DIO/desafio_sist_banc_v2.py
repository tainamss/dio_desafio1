from datetime import datetime
import random

def saque(saldo, valor, limite, limite_saque, extrato ):
    if valor <= saldo and valor <= limite_saque and limite < 10:
        saldo -= valor
        extrato += f'Saque no valor de R${valor}\nSaldo atual: R${saldo}.\n{data_hora()}\n'
        limite += 1
    elif valor > limite_saque:
        print("O valor do saque excede o limite permitido por saque de R$500.00")
    elif valor > saldo:
        print("Saldo insuficiente!")
    elif limite == 10:
        print(transacoes_diarias())
    return saldo, extrato, limite

def deposito (saldo, valor, extrato, limite, /):
    if limite <  10:
        saldo += valor
        extrato += f'Deposito no valor de R${valor}\nSaldo atual: R${saldo}.{data_hora()}\n'
        limite += 1
    else:
        print(transacoes_diarias())

    return saldo, extrato, limite 

def mostrar_extrato( extrato):
    print("\n====== EXTRATO ======")
    print(extrato if extrato else "Nenhuma movimentação realizada.")
    print("=====================\n")

usuarios = {}

def criar_usuario(nome, data_nasc, cpf, logradouro, num, bairro, cidade, estado):
    for usuario in usuarios.values():
        if usuario['cpf'] == cpf:
            print("Usuário com este CPF já existe.")
            return
        
    endereco = f"{logradouro}, {num} - {bairro}, {cidade}/{estado}"
    endereco = {
        "logradouro": logradouro,
        "numero": num,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado
    }

    novo_usuario = {
        "nome": nome,
        "data_nasc": data_nasc,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios[cpf] = novo_usuario
    print("Usuário criado com sucesso!")
    
contas = []

def criar_conta(numero, cpf):
    usuario = usuarios.get(cpf)
    if not usuario:
        print("Usuário não encontrado. Crie o usuário antes de criar a conta.")
        return
    
    conta = {
        "agencia": "0001",
        "numero": numero,
        "usuario": usuario
    }

    contas.append(conta)
    print("Conta criada com sucesso!")
def data_hora():
    return f"Data e hora da transação: {datetime.now()}"

def transacoes_diarias():
    return "Limite de transações diárias excedido!"

menu = '''
======MENU======
Escolha alguma das seguintes ações:
[n] Novo Usuário
[c] Criar conta
[s] Saque
[d] Depósito 
[e] Extrato
[q] Sair
>>>
'''

saldo = 0
limite_saque = 500
extrato = ''
quant_transacoes = 0

while True:
    opcao = input(menu)

    if opcao == 'n':
        print("========CRIAÇÃO DE CONTA========")
        print("\nPara criarmos sua conta você deve responder as seguintes perguntas:")
        nome = input("\nInfome seu nome: ")
        nascimento= int(input("\nInforme apenas em numeros sua data de nascimento: "))
        cpf= int(input("\nInforme apenas em numeros seu cpf: "))
        logradouro = input("\nInforme seu logradouro: ")
        num = int(input("\nInforme o numero da sua residencia: "))
        bairro = input("\nInforme seu bairro: ")
        cidade = input("\nInforme sua cidade: ")
        estado = input("\nEm sigla, informe seu estado: ")
        criar_usuario(nome, nascimento, cpf, logradouro, num, bairro, cidade, estado)
        print(usuarios)

    if opcao == 'c':
        cpf = int(input("Informe seu CPF: "))
        numero = str(random.randint(100000, 999999))
        criar_conta(numero, cpf)
        

    if opcao == 's':
        sacar = int(input("DIgite o valor que deseja sacar: "))
        saldo, extrato, quant_transacoes = saque(saldo, sacar, quant_transacoes, limite_saque, extrato)
            
    elif opcao == 'd':
        depositar = int(input("Digite o valor que deseja depositar: "))
        saldo, extrato, quant_transacoes = deposito(saldo, depositar, extrato, quant_transacoes)            

    elif opcao == 'e':
        mostrar_extrato(extrato = extrato)

    elif opcao == 'q':
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")

        