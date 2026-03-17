def test_valido():
    saida = verificar_cadastro(18,'adulto',60,True)
    assert saida == "Inscrição realizada com sucesso."
    
def test_idade_invalida_menor():
    saida = verificar_cadastro(9,'infantil',100,True)
    assert saida == "Idade não permitida para inscrição. Deve ter entre 10 e 60 anos."

def test_idade_invalida_maior():
    saida = verificar_cadastro(61,'adulto',60,True)
    assert saida == "Idade não permitida para inscrição. Deve ter entre 10 e 60 anos."

def test_categoria_invalida_infantil():
    saida = verificar_cadastro(15,'infantil',80,True)
    assert saida == "Categoria incorreta para a idade."
    
def test_categoria_invalida_juvenil():
    saida = verificar_cadastro(20,'juvenil',110,True)
    assert saida == "Categoria incorreta para a idade."

def test_categoria_invalida_adulto():
    saida = verificar_cadastro(17,'adulto',100,True)
    assert saida == "Categoria incorreta para a idade."
    
def test_tempo_invalido_menor():
    saida = verificar_cadastro(30,'adulto',25,True)
    assert saida == "Tempo estimado deve estar entre 30 e 180 minutos."
    
def test_tempo_invalido_maior():
    saida = verificar_cadastro(30,'adulto',200,True)
    assert saida == "Tempo estimado deve estar entre 30 e 180 minutos."

def test_termos_nao_aceitos():
    saida = verificar_cadastro(22,'adulto',45,False)
    assert saida == "Assinatura deve ser feita para inscrição."
    
def verificar_cadastro(idade, categoria, tempo_estimado, termos_aceitos):
    # Regra 1 - idade
    if idade < 10 or idade > 60:
        return "Idade não permitida para inscrição. Deve ter entre 10 e 60 anos."

    # Regra 2 - categoria
    if categoria == 'infantil' and (not(idade >= 10 and idade <= 14)):
        return "Categoria incorreta para a idade."
    elif categoria == 'juvenil' and (not(idade >= 15 and idade <= 17)):
        return "Categoria incorreta para a idade."
    elif categoria == 'adulto' and (not(idade >= 18 and idade <= 60)):
        return "Categoria incorreta para a idade."

    # Regra 3 - tempo estimado
    if tempo_estimado < 30 or tempo_estimado > 180:
        return "Tempo estimado deve estar entre 30 e 180 minutos."
      
    # Regra 4 - assinatura
    if termos_aceitos == False:
        return "Assinatura deve ser feita para inscrição."
    
    return "Inscrição realizada com sucesso."
