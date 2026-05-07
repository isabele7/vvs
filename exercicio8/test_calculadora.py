import pytest
from calculadora import add

def test_empty_string():
    assert add("") == 0

def test_single_value():
    assert add("5") == 5

def test_multiple_values_comma():
    assert add("1,2,3") == 6

def test_newline():
    assert add("1\n2\n3") == 6

def test_delimiter():
    assert add("//;\n1;2;3") == 6

def test_negative_number():
    with pytest.raises(ValueError, match="negativos não permitidos: -2"):
        add("1,-2,3")

def test_multiple_negative_numbers():
    with pytest.raises(ValueError, match="-2, -5"):
        add("1,-2,3,-5")

def test_boundary_1001():
    assert add("2,1001") == 2

def test_boundary_1000():
    assert add("2,1000") == 1002

def test_boundary_999():
    assert add("2,999") == 1001

def test_long_delimiter():
    assert add("//[***]\n1***2***3") == 6

def test_multiple_delimiters():
    assert add("//[*][%]\n1*2%3") == 6

def test_multiple_long_delimiters():
    assert add("//[**][%%]\n1**2%%3") == 6
