import pytest  
from ..point import Point 
#Méthode AAA ->structure en  Arrange, Act, Assert
#Méthode should_return_correct_when() ->  test autodescriptif

def test_should_return_correct_when_x_is_valid():
    #arrange
    p1= Point(2, 3)
    #act
    x = p1.x
    #assert
    assert x == 2
    

def test_should_return_correct_when_y_is_valid():
    #arrange
    p1= Point(2, 3)
    #act
    y = p1.y
    #assert
    assert y == 3


def test_should_return_none_when_x_is_missing():
    #arrange
    p1 = Point(None, 3)
    #act
    x = p1.x
    #assert
    assert x is None


def test_should_return_none_when_y_is_missing():
    #arrange
    p1 = Point(2, None)
    #act
    y = p1.y
    #assert
    assert y is None

def test_should_return_correct_when_x_is_negative():
    #arrange
    p1 = Point(-2, 3)
    #act
    x = p1.x
    #assert
    assert x == -2

def test_should_return_correct_when_y_is_negative():
    #arrange
    p1 = Point(2, -3)
    #act
    y = p1.y
    #assert
    assert y == -3

def test_should_return_correct_when_x_is_zero():
    #arrange
    p1 = Point(0, 3)
    #act
    x = p1.x
    #assert
    assert x == 0

def test_should_return_correct_when_y_is_zero():
    #arrange
    p1 = Point(2, 0)
    #act
    y = p1.y
    #assert
    assert y == 0

def test_should_return_correct_when_x_is_float():
    #arrange
    p1 = Point(2.5, 3)
    #act
    x = p1.x
    #assert
    assert x == 2.5

def test_should_return_correct_when_y_is_float():
    #arrange
    p1 = Point(2, 3.5)
    #act
    y = p1.y
    #assert
    assert y == 3.5





