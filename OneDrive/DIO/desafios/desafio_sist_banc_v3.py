
from abc import ABC, abstractmethod
from datetime import datetime
import textwrap
from unicodedata import numeric

# Interface Transacao
class Transacao(ABC):
    @property
    @abstractmethod
    def registrar(self, conta):
        pass
    def valor(self):
        pass

# Saque e Depósito herdam Transacao
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor) # registrar(): executa o método sacar() na conta informada, usando o valor armazenado.
        if sucesso:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor  

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor) 
        if sucesso:
            conta.historico.adicionar_transacao(self)  #registrar(): executa o método depositar() na conta com o valor.

# Histórico de transações
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):       #recebe qual transação foi feita e adiciona na lista
        self._transacoes.append(
            {
                "tipo": transacao.__clas__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

# Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):        #recebe a conta feita e adiciona na lista de contas ja existentes
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        

# Conta
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property                #O @property transforma um método em um atributo de leitura.
    def saldo(self):
        print("Acessando saldo...")
        return self._saldo
    
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
        saldo =  self.saldo
        if valor > saldo:
            print("\nXXXXXXXXX\nA operação não foi concluída pois o saldo atual é insuficiente\nXXXXXXXXX")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n=========\nSaque realizado com sucesso!\n=========")
            return True
        
        else:
            print("\nXXXXXXXXX\nFalha na operação! O valor informado é invalido\nXXXXXXXXX")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=========\nDepósito realizado com sucesso!\n=========")
            return True
        else:
            print("\nXXXXXXXXX\nFalha na operação! O valor informado é invalido\nXXXXXXXXX")
            return False
# Pessoa Física herda Cliente
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Conta Corrente herda Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite = 500, limite_saques = 3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques =  len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nXXXXXXXXX\nA operação não foi concluída pois o valor do saque excede o limite\nXXXXXXXXX")

        elif excedeu_saques:
            print("\nXXXXXXXXX\nA operação não foi concluída pois o número máximo de saques foi atingido\nXXXXXXXXX")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}        
        """
    
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

main()    



