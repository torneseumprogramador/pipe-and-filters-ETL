"""
Implementação de pipes usando geradores Python para conectar filtros.
"""

from typing import Iterator, Callable, Any
from filters.text_filters import (
    remove_extra_spaces,
    filter_numeric_strings,
    convert_to_integers,
    filter_greater_than
)


class Pipeline:
    """
    Pipeline que conecta filtros usando geradores Python.
    
    Cada filtro é aplicado sequencialmente, processando os dados de forma lazy.
    """
    
    def __init__(self):
        """Inicializa um pipeline vazio."""
        self.filters = []
    
    def add_filter(self, filter_func: Callable[[Iterator], Iterator]) -> 'Pipeline':
        """
        Adiciona um filtro ao pipeline.
        
        Args:
            filter_func: Função filtro que recebe e retorna um iterador
            
        Returns:
            Self para permitir encadeamento de métodos
        """
        self.filters.append(filter_func)
        return self
    
    def process(self, data: Iterator) -> Iterator:
        """
        Processa os dados através de todos os filtros do pipeline.
        
        Args:
            data: Dados de entrada como iterador
            
        Returns:
            Iterador com os dados processados
        """
        result = data
        
        # Aplica cada filtro sequencialmente
        for filter_func in self.filters:
            result = filter_func(result)
        
        return result
    
    def execute(self, data: Iterator) -> list:
        """
        Executa o pipeline e retorna os resultados como lista.
        
        Args:
            data: Dados de entrada como iterador
            
        Returns:
            Lista com os resultados processados
        """
        return list(self.process(data))


def create_text_processing_pipeline() -> Pipeline:
    """
    Cria um pipeline pré-configurado para processamento de texto.
    
    Returns:
        Pipeline configurado com os filtros padrão
    """
    return (Pipeline()
            .add_filter(remove_extra_spaces)
            .add_filter(filter_numeric_strings)
            .add_filter(convert_to_integers)
            .add_filter(filter_greater_than))


def create_custom_pipeline(*filters: Callable[[Iterator], Iterator]) -> Pipeline:
    """
    Cria um pipeline customizado com filtros específicos.
    
    Args:
        *filters: Filtros a serem aplicados em sequência
        
    Returns:
        Pipeline configurado com os filtros especificados
    """
    pipeline = Pipeline()
    for filter_func in filters:
        pipeline.add_filter(filter_func)
    return pipeline
