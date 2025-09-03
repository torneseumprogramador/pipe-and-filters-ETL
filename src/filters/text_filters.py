"""
Filtros para processamento de texto.
Cada filtro recebe um iterador e retorna um novo iterador com os dados processados.
"""

from typing import Iterator


def remove_extra_spaces(data: Iterator[str]) -> Iterator[str]:
    """
    Remove espaços extras (múltiplos espaços, espaços no início/fim) de cada string.
    
    Args:
        data: Iterador de strings
        
    Yields:
        Strings com espaços extras removidos
    """
    for item in data:
        if isinstance(item, str):
            # Remove espaços múltiplos e espaços no início/fim
            cleaned = ' '.join(item.split())
            yield cleaned
        else:
            # Se não for string, passa adiante sem modificação
            yield item


def filter_numeric_strings(data: Iterator[str]) -> Iterator[str]:
    """
    Filtra apenas strings que representam números.
    
    Args:
        data: Iterador de strings
        
    Yields:
        Apenas strings numéricas
    """
    for item in data:
        if isinstance(item, str):
            # Verifica se a string representa um número (incluindo negativos)
            if item.replace('-', '').replace('.', '').replace(',', '').isdigit():
                yield item
        else:
            # Se não for string, passa adiante sem modificação
            yield item


def convert_to_integers(data: Iterator[str]) -> Iterator[int]:
    """
    Converte strings numéricas para inteiros.
    
    Args:
        data: Iterador de strings numéricas
        
    Yields:
        Inteiros convertidos das strings
    """
    for item in data:
        if isinstance(item, str):
            try:
                # Remove vírgulas e converte para float primeiro, depois para int
                cleaned = item.replace(',', '')
                number = float(cleaned)
                yield int(number)
            except (ValueError, TypeError):
                # Se não conseguir converter, pula o item
                continue
        else:
            # Se não for string, passa adiante sem modificação
            yield item


def filter_greater_than(data: Iterator[int], threshold: int = 10) -> Iterator[int]:
    """
    Filtra apenas números maiores que um valor limite.
    
    Args:
        data: Iterador de números
        threshold: Valor limite (padrão: 10)
        
    Yields:
        Apenas números maiores que o limite
    """
    for item in data:
        if isinstance(item, (int, float)) and item > threshold:
            yield item
        elif not isinstance(item, (int, float)):
            # Se não for número, passa adiante sem modificação
            yield item
