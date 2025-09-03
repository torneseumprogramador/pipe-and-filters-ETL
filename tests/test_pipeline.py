"""
Testes unitários para a classe Pipeline.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipes.pipeline import Pipeline, create_text_processing_pipeline, create_custom_pipeline
from filters.text_filters import remove_extra_spaces, filter_numeric_strings


class TestPipeline(unittest.TestCase):
    """Testa a funcionalidade do pipeline."""
    
    def test_pipeline_initialization(self):
        """Testa a inicialização de um pipeline vazio."""
        pipeline = Pipeline()
        self.assertEqual(len(pipeline.filters), 0)
    
    def test_add_filter(self):
        """Testa a adição de filtros ao pipeline."""
        pipeline = Pipeline()
        
        # Adiciona filtros
        pipeline.add_filter(remove_extra_spaces)
        pipeline.add_filter(filter_numeric_strings)
        
        # Verifica se foram adicionados
        self.assertEqual(len(pipeline.filters), 2)
        self.assertEqual(pipeline.filters[0], remove_extra_spaces)
        self.assertEqual(pipeline.filters[1], filter_numeric_strings)
    
    def test_add_filter_chain(self):
        """Testa o encadeamento de métodos ao adicionar filtros."""
        pipeline = Pipeline()
        
        # Deve retornar self para permitir encadeamento
        result = pipeline.add_filter(remove_extra_spaces)
        self.assertIs(result, pipeline)
        
        # Deve permitir múltiplas adições em cadeia
        pipeline.add_filter(filter_numeric_strings).add_filter(remove_extra_spaces)
        self.assertEqual(len(pipeline.filters), 3)
    
    def test_process_empty_pipeline(self):
        """Testa o processamento com pipeline vazio."""
        pipeline = Pipeline()
        input_data = ["test", "data"]
        
        # Pipeline vazio deve retornar os dados originais
        result = list(pipeline.process(iter(input_data)))
        self.assertEqual(result, input_data)
    
    def test_process_with_filters(self):
        """Testa o processamento com filtros."""
        pipeline = Pipeline()
        pipeline.add_filter(remove_extra_spaces)
        
        input_data = ["  hello  ", "  world  "]
        expected = ["hello", "world"]
        
        result = list(pipeline.process(iter(input_data)))
        self.assertEqual(result, expected)
    
    def test_execute_method(self):
        """Testa o método execute que retorna lista."""
        pipeline = Pipeline()
        pipeline.add_filter(remove_extra_spaces)
        
        input_data = ["  hello  ", "  world  "]
        expected = ["hello", "world"]
        
        result = pipeline.execute(iter(input_data))
        self.assertEqual(result, expected)
        self.assertIsInstance(result, list)
    
    def test_multiple_filters_sequence(self):
        """Testa a sequência de múltiplos filtros."""
        pipeline = Pipeline()
        pipeline.add_filter(remove_extra_spaces)
        pipeline.add_filter(filter_numeric_strings)
        
        input_data = ["  123  ", "  abc  ", "  456  "]
        expected = ["123", "456"]
        
        result = list(pipeline.process(iter(input_data)))
        self.assertEqual(result, expected)
    
    def test_create_text_processing_pipeline(self):
        """Testa a criação do pipeline pré-configurado."""
        pipeline = create_text_processing_pipeline()
        
        # Deve ter 4 filtros
        self.assertEqual(len(pipeline.filters), 4)
        
        # Testa o processamento
        input_data = ["  123  ", "  abc  ", "  456  "]
        result = pipeline.execute(iter(input_data))
        
        # Deve retornar apenas números > 10
        self.assertEqual(result, [123, 456])
    
    def test_create_custom_pipeline(self):
        """Testa a criação de pipeline customizado."""
        pipeline = create_custom_pipeline(remove_extra_spaces, filter_numeric_strings)
        
        # Deve ter 2 filtros
        self.assertEqual(len(pipeline.filters), 2)
        
        # Testa o processamento
        input_data = ["  123  ", "  abc  ", "  456  "]
        result = list(pipeline.process(iter(input_data)))
        
        # Deve retornar apenas strings numéricas sem espaços
        self.assertEqual(result, ["123", "456"])
    
    def test_pipeline_with_empty_input(self):
        """Testa o comportamento com entrada vazia."""
        pipeline = create_text_processing_pipeline()
        empty_data = []
        
        result = pipeline.execute(iter(empty_data))
        self.assertEqual(result, [])
    
    def test_pipeline_with_single_item(self):
        """Testa o comportamento com um único item."""
        pipeline = create_text_processing_pipeline()
        single_data = ["  123  "]
        
        result = pipeline.execute(iter(single_data))
        self.assertEqual(result, [123])
    
    def test_pipeline_lazy_evaluation(self):
        """Testa que o pipeline processa dados de forma lazy."""
        pipeline = create_text_processing_pipeline()
        input_data = ["  123  ", "  abc  ", "  456  "]
        
        # Não deve processar até iterar
        result_iterator = pipeline.process(iter(input_data))
        
        # Deve ser um iterador, não uma lista
        self.assertTrue(hasattr(result_iterator, '__iter__'))
        
        # Processa item por item
        items = []
        for item in result_iterator:
            items.append(item)
        
        self.assertEqual(items, [123, 456])


if __name__ == '__main__':
    unittest.main()
