import textwrap

def exibir_menu(conta_logada=None):
    if not conta_logada:
            menu = """\n
    ================ MENU ================
    [l]\tLogin
    [nc]\tNova conta
    [nu]\tNovo usuario
    [q]\tSair
    ======================================
    => """
    else:
        info_conta = f"Ag: {conta_logada['agencia']} | C/C: {conta_logada['numero_conta']} | Titular: {conta_logada['usuario']['nome']}"
        menu = f"""
    ======= BANCO (LOGADO) ========
    {info_conta}
    ---------------------------------
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [lc]\tListar contas
    [t]\tTrocar de conta (Logout)
    [q]\tSair
    ======================================
    => """
    return input(textwrap.dedent(menu))

def login(usuarios, contas):
    cpf = input("Informe o CPF do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n>>> Usuario não encontrado. <<<")
        return None

    contas_do_usuario = [conta for conta in contas if conta['usuario']['cpf'] == cpf]
    
    if not contas_do_usuario:
        print("\n>>> Nenhuma conta encontrada para este usuario. <<<")
        return None
        
    print("\n--- Contas encontradas ---")
    for conta in contas_do_usuario:
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}")
    
    num_conta_escolhida = int(input("Digite o número da conta que deseja logar: "))
    
    for conta in contas_do_usuario:
        if conta['numero_conta'] == num_conta_escolhida:
            print(f"\n=== Login realizado com sucesso na conta {num_conta_escolhida}! ===")
            return conta
            
    print("\n>>> Número da conta inválido. <<<")
    return None
    

def depositar(conta):

    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n>>> Operação falhou! O valor informado é inválido. >>>")


def sacar(conta, limite, numero_saques):

    valor = float(input("Informe o valor do saque: "))

    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite_valor = valor > limite
    excedeu_limite_saques = conta["numero_saques"] >= numero_saques

    if excedeu_saldo:
        print("\n>>> Operação falhou! Você não tem saldo suficiente. <<<")
    elif excedeu_limite_valor:
        print(f"\n>>> Operação falhou! O valor do saque excede o limite de R$ {limite:.2f}. <<<")
    elif excedeu_limite_saques:
        print("\n>>> Operação falhou! Número máximo de saques excedido. <<<")
    elif valor > 0:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta["numero_saques"] += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n>>> Operação falhou! O valor informado é inválido. <<<")
    

def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    extrato = conta["extrato"]
    saldo = conta["saldo"]
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n>>> Já existe um usuario com este CPF! <<<")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    
    usuarios.append({
        "nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco
    })
    print("\n=== Usuario criado com sucesso! ===")

def criar_conta(agencia, contas, usuarios):
    cpf = input("Informe o CPF do usuario para vincular a conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        numero_conta = len(contas) + 1
        contas.append({
            "agencia": agencia, "numero_conta": numero_conta, "usuario": usuario,
            "saldo": 0, "extrato": "", "numero_saques": 0
        })
        print(f"\n=== Conta criada com sucesso! Agência: {agencia}, Conta: {numero_conta} ===")
    else:
        print("\n>>> usuario não encontrado! Crie o usuario antes de criar uma conta. <<<")

def listar_contas(contas):
    if not contas:
        print("\nNenhuma conta foi criada ainda.")
        return
        
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print(linha)
        print("-" * 40)
    print("===============================================")


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    usuarios = []
    contas = []
    limite = 500
    conta_logada = None

    while True:
        opcao = exibir_menu(conta_logada)

        if not conta_logada:
            if opcao == "l":
                conta_logada = login(usuarios, contas)
            elif opcao == "nu":
                criar_usuario(usuarios)
            elif opcao == "nc":
                criar_conta(AGENCIA, contas, usuarios)
            elif opcao == "q":
                break
            else:
                print("Operação inválida, selecione novamente a operação.")
        
        else:
            if opcao == "d":
                depositar(conta_logada)
            elif opcao == "s":
                sacar(conta_logada, limite, LIMITE_SAQUES)
            elif opcao == "e":
                exibir_extrato(conta_logada)
            elif opcao == "lc":
                listar_contas(contas)
            elif opcao == "t":
                conta_logada = None
                print("\n=== Logout realizado com sucesso! ===")
            elif opcao == "q":
                break
            else:
                print("Operação inválida, selecione novamente a operação.")

    print("\nObrigado por utilizar nosso sistema. Até logo!")


if __name__ == "__main__":
    main()
