"""
Testes unitários para os filtros de texto.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from filters.text_filters import (
    remove_extra_spaces,
    filter_numeric_strings,
    convert_to_integers,
    filter_greater_than
)


class TestTextFilters(unittest.TestCase):
    """Testa os filtros de processamento de texto."""
    
    def test_remove_extra_spaces(self):
        """Testa a remoção de espaços extras."""
        # Dados de teste
        input_data = ["  hello  ", "world   ", "   test", "normal", "   multiple    spaces   "]
        expected = ["hello", "world", "test", "normal", "multiple spaces"]
        
        # Executa o filtro
        result = list(remove_extra_spaces(iter(input_data)))
        
        # Verifica o resultado
        self.assertEqual(result, expected)
    
    def test_filter_numeric_strings(self):
        """Testa a filtragem de strings numéricas."""
        # Dados de teste
        input_data = ["123", "abc", "456", "def", "789", "12.34", "-100", "0"]
        expected = ["123", "456", "789", "12.34", "-100", "0"]
        
        # Executa o filtro
        result = list(filter_numeric_strings(iter(input_data)))
        
        # Verifica o resultado
        self.assertEqual(result, expected)
    
    def test_convert_to_integers(self):
        """Testa a conversão de strings para inteiros."""
        # Dados de teste
        input_data = ["123", "456", "789", "12.34", "-100", "0"]
        expected = [123, 456, 789, 12, -100, 0]
        
        # Executa o filtro
        result = list(convert_to_integers(iter(input_data)))
        
        # Verifica o resultado
        self.assertEqual(result, expected)
    
    def test_filter_greater_than_default(self):
        """Testa a filtragem de números maiores que 10 (padrão)."""
        # Dados de teste
        input_data = [5, 10, 15, 20, 25, 30]
        expected = [15, 20, 25, 30]
        
        # Executa o filtro
        result = list(filter_greater_than(iter(input_data)))
        
        # Verifica o resultado
        self.assertEqual(result, expected)
    
    def test_filter_greater_than_custom_threshold(self):
        """Testa a filtragem com limite customizado."""
        # Dados de teste
        input_data = [5, 10, 15, 20, 25, 30]
        expected = [25, 30]
        
        # Executa o filtro com limite 20
        result = list(filter_greater_than(iter(input_data), 20))
        
        # Verifica o resultado
        self.assertEqual(result, expected)
    
    def test_filter_greater_than_mixed_types(self):
        """Testa a filtragem com tipos mistos de dados."""
        # Dados de teste
        input_data = [5, "abc", 15, "def", 25, 30]
        
        # Executa o filtro
        result = list(filter_greater_than(iter(input_data)))
        
        # Verifica que contém os números > 10 e as strings não numéricas
        # A ordem pode variar, então verificamos o conteúdo
        self.assertIn(15, result)
        self.assertIn(25, result)
        self.assertIn(30, result)
        self.assertIn("abc", result)
        self.assertIn("def", result)
        self.assertNotIn(5, result)  # 5 não é > 10
        self.assertEqual(len(result), 5)
    
    def test_empty_input(self):
        """Testa o comportamento com entrada vazia."""
        # Testa com lista vazia
        empty_data = []
        
        # Todos os filtros devem retornar iteradores vazios
        self.assertEqual(list(remove_extra_spaces(iter(empty_data))), [])
        self.assertEqual(list(filter_numeric_strings(iter(empty_data))), [])
        self.assertEqual(list(convert_to_integers(iter(empty_data))), [])
        self.assertEqual(list(filter_greater_than(iter(empty_data))), [])
    
    def test_single_item(self):
        """Testa o comportamento com um único item."""
        # Testa com um item
        single_data = ["  test  "]
        
        # Remove espaços extras
        result = list(remove_extra_spaces(iter(single_data)))
        self.assertEqual(result, ["test"])
        
        # Filtra numérico
        numeric_data = ["123"]
        result = list(filter_numeric_strings(iter(numeric_data)))
        self.assertEqual(result, ["123"])
        
        # Converte para inteiro
        result = list(convert_to_integers(iter(numeric_data)))
        self.assertEqual(result, [123])
        
        # Filtra maior que 10
        number_data = [15]
        result = list(filter_greater_than(iter(number_data)))
        self.assertEqual(result, [15])


if __name__ == '__main__':
    unittest.main()
