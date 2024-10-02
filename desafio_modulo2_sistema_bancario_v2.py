import textwrap

menu = """\n
Escolha uma opção:

[d]\tDepósito
[s]\tSaque
[e]\tExtrato
[c]\tCadastro Cliente
[n]\tNova Conta
[q]\tSair

    => """

def cadastrar(usuarios):
    cpf = input("Informe seu CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("********** Cliente já cadastrado! **********")
        return
    
    nome = input("Digite seu nome completo: ")
    data_nasc = input("Digite sua data de nascimento (DD/MM/AAAA): ")
    end = input("Digite seu endereço completo: \n\n Logradouro, Número, Complemento, Bairro, Cidade/Estado: ")

    usuarios.append({"nome": nome, "data_nasc": data_nasc, "cpf": cpf, "end": end})

    print("=== Cliente cadastrado com sucesso! ===")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado! @@@")
    return None

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito\tR$ {valor:.2f}\n"
        print("=== Depósito realizado com sucesso! ===\n")
    else:
        print("\n@@@ Depósito não realizado! Valor inválido. @@@")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Saldo insuficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! Valor de saque excede limite diário de saque. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===\n")
    else:
        print("Operação não realizada!")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("===============================")

def main():
    AGENCIA = "0001"
    LIMITE_SAQUES = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = input(textwrap.dedent(menu)).lower()

        if opcao == "d":
            try:
                valor = float(input("Digite o valor de depósito: R$ "))
                saldo, extrato = depositar(saldo, valor, extrato)
                print(f"Saldo atual: R$ {saldo:.2f}")
            except ValueError:
                print("\n@@@ Valor inválido! Tente novamente. @@@")

        elif opcao == "s":
            try:
                valor = float(input("Digite o valor de saque: R$ "))
                saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
                print(f"Saldo atual: R$ {saldo:.2f}")
            except ValueError:
                print("\n@@@ Operação inválida! @@@")

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "c":
            cadastrar(usuarios)

        elif opcao == "n":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "q":
            print("Obrigada por utilizar nossos canais.\n=== Operação encerrada! ===")
            break

        else:
            print("\n@@@ Opção inválida! Tente novamente. @@@")

if __name__ == "__main__":
    main()
