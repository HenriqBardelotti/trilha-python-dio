def exibir_menu(): 
    menu = """
--------------------------------
[D]   Depósito
[S]   Saque
[E]   Extrato
[nU]  Cadastrar Novo Usuário
[nC]  Nova Conta
[lC]  Listar Contas 
[Q]   Sair
--------------------------------
"""
    return print(menu)

def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        print("Valor inválido para depósito")
    else:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    return saldo, extrato

def saque(*, saldo, valor, extrato, limites_de_saque, limite):
    if saldo == 0:
        print("Operação falhou! Saldo insuficiente")  
        return saldo, extrato, limites_de_saque
    elif limites_de_saque >= 3:
        print("Operação falhou! Limite de saques diário atingido")
        return saldo, extrato, limites_de_saque    
    if valor <= 0:
        print("Operação falhou! Valor de saque inválido")
        return saldo, extrato, limites_de_saque      
    if valor > saldo:
        print("Operação falhou! Saldo insuficiente")
    elif valor > limite:
        print("Valor de saque maior que o limite disponível")  
    else:
        limites_de_saque += 1
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
    return saldo, extrato, limites_de_saque
        
def exibir_extrato(saldo, /, *, extrato):
    if extrato == "":
        print("Operação falhou! Não foram realizadas movimentações")
    else:
        titulo = "EXTRATO"
        print(titulo.center(21, "="))
        print(f"Saldo = R$ {saldo:.2f}\n" + extrato.rstrip("\n"))
        titulo = ""
        print(titulo.center(21, "="))

def filtrar_usuarios(cpf, usuarios):
    filtro = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return filtro[0] if filtro else None

def criar_usuario(usuarios):
    cpf = int(input("Informe o CPF: "))
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario:
        print("Usuário já cadastrado...")
        return
    
    nome = input("Nome: ")
    data_nascimento = input("Data de nascimento dd-mm-aaaa: ")
    endereco = input("Endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append( {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("======= Usuário Cadastrado com Sucesso! =======")

def criar_conta(agencia, numero_da_conta, usuarios):
    cpf = int(input("Informe o CPF: "))
    usuario = filtrar_usuarios(cpf, usuarios)
    
    if usuario: 
        print("=== Conta Criada com Sucesso ===")
        numero_da_conta += 1
        return {"agencia": agencia, "numero_da_conta": numero_da_conta, "usuario": usuario}, numero_da_conta 
    
    print("=== Usuário não Encontrado, Operação Encerrada ===")

def listar_contas(contas):
    for conta in contas:
        print(f"""\
            Agência:   {conta['agencia' ]}
            C/C:       {conta['numero_da_conta' ]}
            Titular:   {conta['usuario' ] ['nome' ]}
            """)
        print("=" * 60)
        
saldo = 0
extrato = ""
deposito = 0.0
limites_de_saque = 0
limite = 500
usuarios = []
contas = []
agencia = "0001"
numero_da_conta = 0


while True:
    exibir_menu()
    opcao = (input("Menu: "))
    
    if opcao.upper() == 'D':
        valor = float(input("Informe o valor do depósito: "))
        saldo, extrato = depositar(saldo, valor, extrato)
    elif opcao.upper() == 'S':
        valor = float(input("Informe o valor do saque: "))
        saldo, extrato, limites_de_saque = saque(saldo=saldo, valor=valor, extrato=extrato, limites_de_saque=limites_de_saque, limite=limite)
    elif opcao.upper() == 'E':
        exibir_extrato(saldo, extrato=extrato)
    elif opcao == 'nU':
        criar_usuario(usuarios)
    elif opcao == 'nC':
        conta, numero_da_conta = criar_conta(agencia, numero_da_conta, usuarios)       
        if conta:
            contas.append(conta)
    elif opcao == 'lC':
        listar_contas(contas)
    elif opcao.upper() == 'Q':
        break
    else:
        print("Operação falhou! Opção inválida!\n")
