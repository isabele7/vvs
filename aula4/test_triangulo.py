def test_equilatero():
    assert classifica_triangulo(2,2,2) == 'equilátero'

def test_isosceles_ab():
    assert classifica_triangulo(2,2,3) == 'isósceles'

def test_isosceles_bc():
    assert classifica_triangulo(2,3,3) == 'isósceles'
    
def test_isosceles_ac():
    assert classifica_triangulo(2,3,2) == 'isósceles'
    
def test_escaleno():
    assert classifica_triangulo(2,3,4) == 'escaleno'

def test_nao_triangulo_soma_igual():
    assert classifica_triangulo(1,2,3) == 'não é um triângulo'

def test_nao_triangulo_soma_menor_a():
    assert classifica_triangulo(5,1,1) == 'não é um triângulo'

def test_nao_triangulo_soma_menor_b():
    assert classifica_triangulo(1,5,2) == 'não é um triângulo'
    
def test_nao_triangulo_soma_menor_c():
    assert classifica_triangulo(1,10,12) == 'não é um triângulo'

def test_nao_triangulo_lados_negativos():
    assert classifica_triangulo(-1,2,3) == 'não é um triângulo'

def test_nao_triangulo_lados_zero():
    assert classifica_triangulo(0,2,3) == 'não é um triângulo'
      
def classifica_triangulo(a, b, c):
    if ((a<(b+c) and b<(a+c) and c<(a+b)) and (a>0 and b>0 and c>0)):
        if (a == b and b == c and a == c):
            return 'equilátero'
        if (a == b or b == c or a == c):
            return 'isósceles'
        return 'escaleno'
    return 'não é um triângulo'
