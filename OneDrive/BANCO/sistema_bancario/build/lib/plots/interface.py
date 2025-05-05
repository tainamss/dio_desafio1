import textwrap
from unicodedata import numeric

from sistema_bancario.acoes.clientes import PessoaFisica
from sistema_bancario.acoes.contas import ContaCorrente
from sistema_bancario.acoes.transacoes import Deposito, Saque

def menu():
    menu = '''
    ================MENU================
    Escolha alguma das seguintes ações:
    [n] Novo Usuário
    [c] Criar conta
    [l] Listar contas
    [s] Saque
    [d] Depósito 
    [e] Extrato
    [q] Sair
    >>>
    '''
    return input(textwrap.dedent(menu))

def depositar(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nXXXXXXXXXX\nCliente não encontrado\nXXXXXXXXXX")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nXXXXXXXXXX\nCliente não possui conta!\nXXXXXXXXXX")
        return
    return cliente.contas[0]

def sacar(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nXXXXXXXXXX\nCliente não encontrado\nXXXXXXXXXX")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)
    
def exibir_extrato(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nXXXXXXXXXX\nCliente não encontrado\nXXXXXXXXXX")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n============ EXTRATO ============")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else: 
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("\n=================================")

def criar_cliente(clientes):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nXXXXXXXXXX\nJá existe um cliente com esse CPF\nXXXXXXXXXX")
        return
    nome = input("informe seu nome completo: ")
    data_nasc = input("Infome a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome = nome, data_nascimento= data_nasc, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nXXXXXXXXXX\nCliente não encontrado\nXXXXXXXXXX")
        return
    conta = ContaCorrente.nova_conta(cliente= cliente, numero = numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []
    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        
        elif opcao == "s":
            sacar(clientes)
        
        elif opcao =="e":
            exibir_extrato(clientes)
        
        elif opcao == "n":
            criar_cliente(clientes)
        
        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == "l":
            listar_contas(contas)
        
        elif opcao == 'q':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")