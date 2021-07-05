import sqlite3
import datetime


con = sqlite3.connect('DB_CONTROLE_FINANCEIRO.db')
cur = con.cursor()

# Função para criar tabela
# Tabela 01
create_table = ('CREATE TABLE IF NOT EXISTS dividas(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, divida varchar(100), valor int, data date)')
cur.execute(create_table)

# Tabela 02
create_table2 = ('CREATE TABLE IF NOT EXISTS cartao(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, cartao varchar(100), divida varchar(100), qtd_parcela int, valor int)')
cur.execute(create_table2)

# Tabela 03 com chave estrangeira
create_table3 = ('CREATE TABLE IF NOT EXISTS cartao_parcela(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,id_cartao integer,valor int,constraint fk_cartao foreign key (id_cartao) references cartao (id))')
cur.execute(create_table3)

# Create Trigger
create_trigger = ('CREATE TRIGGER IF NOT EXISTS tr_parcelado AFTER INSERT on cartao BEGIN INSERT INTO cartao_parcela (id_cartao, valor) VALUES (NEW.ID, NEW.VALOR); END;')
cur.execute(create_trigger)


class controleFinanceiro:


    # Método Contrutor
    def __init__(self):
        self.divida = []
        self.valor = []
        self.qtd=[]

    def getDivida(self):
        divida = self.divida
        valor = self.valor
        print(divida)
        print(valor)

    def setDivida(self, novaDivida, novoValor):
        divida = novaDivida
        valor = novoValor
        self.date_insert(divida.upper(), valor)

    def setCartao(self, nomeCartao, novaDivida, qtdParcela, valorParcela):
        cartao = nomeCartao
        divida = novaDivida
        qtd = qtdParcela
        valor = valorParcela
        self.date_insert_cartao(cartao.upper(),divida.upper(),qtd,valor)


    def  cadastroDivida(self):
        novoCadastro = '1'
        while novoCadastro == '1':
            nomeDivida = input("\nDigite o nome da divida: ")
            valorDivida = input("\nDigite o valor da divida: ")
            self.setDivida(nomeDivida, valorDivida)
            novoCadastro = input("\nDeseja Cadastrar uma nova divida? 1 = SIM / 2 = NAO: ")

    def dividaParcelado(self):
        novoCadastro = '1'
        while novoCadastro == '1':
            nomeCartao = input('\nDigite o nome do Cartão: ')
            nomeDivida = input('\nDigite a compra: ')
            qtdParcela = input('\nDigite a quantidade de parcelas: ')
            valorParcela = input('\nDigite o valor da parcela: ')
            self.setCartao(nomeCartao, nomeDivida,  qtdParcela, valorParcela)
            self.ajuste_parcela(qtdParcela)
            novoCadastro = input("\nDeseja Cadastrar uma nova divida? 1 = SIM / 2 = NAO: ")


    def ajuste_parcela(self, qtd):
        p = 1
        while int(p) < int(qtd):
            parcela = cur.execute('SELECT max(id),valor FROM cartao ')
            for i in parcela:
                cur.execute('INSERT INTO cartao_parcela (id_cartao, valor) VALUES (?, ?)', (i[0], i[1]))
                con.commit()
            p = p+1



    def mostrarValor(self):
        self.divida_total()

    def opcao(self, opcao):
        if opcao == '1':
            self.cadastroDivida()
        elif opcao == '2':
            self.dividaParcelado()
        elif opcao == '3':
            self.mostrarValor()
        elif opcao == '4':
            self.listar_dividas()
        else:
            print('Opção invalida')


# Funções para manipular o DB

    # Função para povoar tabela 01
    def date_insert(self, inDivida, inValor):
        bdDivida = inDivida
        bdValor = inValor
        bdDate = datetime.datetime.now()
        cur.execute('INSERT INTO dividas (divida, valor, data) VALUES (?, ?, ?)', (bdDivida, bdValor, bdDate))
        con.commit()

    # Função para povoar tabela 2
    def date_insert_cartao(self, cartao, divida, qtd, valor):
        bdCartao = cartao
        bdDivida = divida
        bdQTD = qtd
        bdValor = valor
        cur.execute('INSERT INTO cartao (cartao, divida, qtd_parcela, valor) VALUES (?, ?, ?, ?)', (bdCartao, bdDivida, bdQTD, bdValor))
        con.commit()


    # Função para ver total
    def divida_total(self):
        valor = cur.execute('select sum(valor) from dividas')
        for i in valor:
            print(i[0])

    # Função para listar dividas
    def listar_dividas(self):
        cur.execute('select * from dividas order by divida')
        for i in cur.fetchall():
            print(i)


def main():

    # Objeto
    divida = controleFinanceiro()
    continua = 'SIM'
    while continua.upper() == 'SIM':
        print('Deseja Realizar qual Operação? ')
        print('1 - Cadastrar divida avulso:')
        print('2 - Cadastrar dividas parceladas')
        print('3 - Velos Total da divida')
        print('4 - Listar Dividas')

        ops = input('Opção: ')
        divida.opcao(ops)
        continua = input('Deseja realizar outra Operação? SIM/NAO: ')


    cur.close()
    con.close()



# Executar o Programa
if __name__ == "__main__":
	main()