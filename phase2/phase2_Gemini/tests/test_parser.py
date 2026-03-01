import os
import pytest
from tempfile import NamedTemporaryFile
from src.io.parser import CsvPointParser
from src.domain.exceptions import ParsingError
from src.domain.models import Point2D

def create_temp_file(content: str) -> str:
    temp_file = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

class TestCsvPointParser:
    
    def test_Should_ReturnPoints_Given_ValidFile_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        content = "1,2\n3.5, 4.5\n  10 , 20  \n"
        filepath = create_temp_file(content)
        
        try:
            # Act
            points = parser.parse(filepath)
            
            # Assert
            assert len(points) == 3
            assert Point2D(1.0, 2.0) in points
            assert Point2D(3.5, 4.5) in points
            assert Point2D(10.0, 20.0) in points
        finally:
            os.remove(filepath)

    def test_Should_IgnoreEmptyLines_Given_FileWithEmptyLines_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        content = "1,2\n\n3,4\n   \n5,6\n"
        filepath = create_temp_file(content)
        
        try:
            # Act
            points = parser.parse(filepath)
            
            # Assert
            assert len(points) == 3
        finally:
            os.remove(filepath)

    def test_Should_DeduplicatePoints_Given_FileWithDuplicates_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        content = "1,2\n3,4\n1,2\n5,6\n3.0 , 4.0\n" # 1,2 et 3,4 en double
        filepath = create_temp_file(content)
        
        try:
            # Act
            points = parser.parse(filepath)
            
            # Assert
            assert len(points) == 3
        finally:
            os.remove(filepath)

    def test_Should_RaiseParsingError_Given_MissingFile_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        filepath = "chemin_inexistant.txt"
        
        # Act & Assert
        with pytest.raises(ParsingError) as context:
            parser.parse(filepath)
        assert "introuvable" in str(context.value)

    def test_Should_RaiseParsingError_Given_InvalidFormat_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        content = "1,2\n3,4,5\n"
        filepath = create_temp_file(content)
        
        try:
            # Act & Assert
            with pytest.raises(ParsingError) as context:
                parser.parse(filepath)
            assert "format attendu" in str(context.value)
        finally:
            os.remove(filepath)

    def test_Should_RaiseParsingError_Given_NonNumeric_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        content = "1,2\n12.5, ABC\n"
        filepath = create_temp_file(content)
        
        try:
            # Act & Assert
            with pytest.raises(ParsingError) as context:
                parser.parse(filepath)
            assert "non numériques" in str(context.value)
        finally:
            os.remove(filepath)

    def test_Should_RaiseParsingError_Given_TooFewPoints_When_Parsed(self):
        # Arrange
        parser = CsvPointParser()
        content = "1,2\n3,4\n" # Seulement 2 points
        filepath = create_temp_file(content)
        
        try:
            # Act & Assert
            with pytest.raises(ParsingError) as context:
                parser.parse(filepath)
            assert "minimum 3" in str(context.value)
        finally:
            os.remove(filepath)