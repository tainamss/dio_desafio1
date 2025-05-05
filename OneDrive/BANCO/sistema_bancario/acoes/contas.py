from sistema_bancario.plots.historico import Historico
from sistema_bancario.acoes.transacoes import Saque, Transacao

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