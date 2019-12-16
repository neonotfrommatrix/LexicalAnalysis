import Compiler as sut
from parameterized import parameterized

@parameterized.expand([
    'int a ;',
    'int aa , bee ;',
    'float a3 , f$ , hhh ;',
    'int num , nu2m , large$ ;'
])
def test_positive_declarations(statement):
    assert sut.is_declaration(statement) == True

@parameterized.expand([
    'int a ',
    'it aa , bee ;',
    'float a3 f$ , hhh ;',
    'bool 3a3 , f$ , hhh ;',
])
def test_negative_declarations(statement):
    assert sut.is_declaration(statement) == False

@parameterized.expand([
    'a = b ;',
    'aa = true ;',
    'see3$ = 0 ;',
    'dee = false ;'
])
def test_positive_assignments(statement):
    assert sut.is_assignment(statement) == True

@parameterized.expand([
    'int a = 12 ;',
    'int = 2 ;',
    '0 = a ;',
    '1 = 2 ;',
    'one = two ',
])
def test_negative_assignments(statement):
    assert sut.is_assignment(statement) == False

@parameterized.expand([
    'a * b ;',
    'see3$ - 0 ;',
    '3 / 2 ;',
    ' 1 + 2 * 3 / 4 - large$ ;'
])
def test_positive_expressions(statement):
    assert sut.is_expression(statement) == True

# @parameterized.expand([
#     'int a = 12 ;',
#     'int = 2 ;',
#     '0 = a ;',
#     '1 = 2 ;',
#     'one = two ',
# ])
# def test_negative_assignments(statement):
#     assert sut.is_assignment(statement) == False