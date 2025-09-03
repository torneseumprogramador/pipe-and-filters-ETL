"""
Exemplos avançados de uso da arquitetura Pipes and Filters.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipes.pipeline import Pipeline, create_custom_pipeline
from filters.text_filters import (
    remove_extra_spaces,
    filter_numeric_strings,
    convert_to_integers,
    filter_greater_than
)


def create_data_validation_pipeline():
    """
    Cria um pipeline para validação de dados.
    """
    def validate_email(data):
        """Valida se as strings são emails válidos."""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for item in data:
            if isinstance(item, str) and re.match(email_pattern, item):
                yield item
    
    def validate_phone(data):
        """Valida se as strings são números de telefone válidos."""
        import re
        phone_pattern = r'^\+?[\d\s\-\(\)]{10,}$'
        
        for item in data:
            if isinstance(item, str) and re.match(phone_pattern, item):
                yield item
    
    return create_custom_pipeline(
        remove_extra_spaces,
        validate_email,
        validate_phone
    )


def create_data_transformation_pipeline():
    """
    Cria um pipeline para transformação de dados.
    """
    def to_uppercase(data):
        """Converte strings para maiúsculas."""
        for item in data:
            if isinstance(item, str):
                yield item.upper()
            else:
                yield item
    
    def add_prefix(data, prefix="ITEM_"):
        """Adiciona um prefixo às strings."""
        for item in data:
            if isinstance(item, str):
                yield f"{prefix}{item}"
            else:
                yield item
    
    def filter_length(data, min_length=5):
        """Filtra strings com comprimento mínimo."""
        for item in data:
            if isinstance(item, str) and len(item) >= min_length:
                yield item
    
    return create_custom_pipeline(
        remove_extra_spaces,
        to_uppercase,
        add_prefix,
        filter_length
    )


def create_conditional_pipeline():
    """
    Cria um pipeline que aplica filtros condicionalmente.
    """
    def conditional_filter(data, condition_func):
        """Aplica um filtro apenas se a condição for verdadeira."""
        for item in data:
            if condition_func(item):
                yield item
    
    def is_even_number(data):
        """Filtra apenas números pares."""
        for item in data:
            if isinstance(item, (int, float)) and item % 2 == 0:
                yield item
    
    def is_positive_number(data):
        """Filtra apenas números positivos."""
        for item in data:
            if isinstance(item, (int, float)) and item > 0:
                yield item
    
    return create_custom_pipeline(
        remove_extra_spaces,
        filter_numeric_strings,
        convert_to_integers,
        is_even_number,
        is_positive_number
    )


def demonstrate_advanced_pipelines():
    """Demonstra os pipelines avançados."""
    print("=== Exemplos Avançados de Pipes and Filters ===\n")
    
    # Pipeline de validação
    print("1. Pipeline de Validação de Dados:")
    validation_pipeline = create_data_validation_pipeline()
    
    validation_data = [
        "  user@example.com  ",
        "  invalid-email  ",
        "  +1-555-123-4567  ",
        "  not-a-phone  ",
        "  admin@test.org  "
    ]
    
    validation_result = validation_pipeline.execute(iter(validation_data))
    print(f"   Dados de entrada: {validation_data}")
    print(f"   Resultado validado: {validation_result}\n")
    
    # Pipeline de transformação
    print("2. Pipeline de Transformação de Dados:")
    transformation_pipeline = create_data_transformation_pipeline()
    
    transformation_data = [
        "  hello  ",
        "  world  ",
        "  test  ",
        "  python  "
    ]
    
    transformation_result = transformation_pipeline.execute(iter(transformation_data))
    print(f"   Dados de entrada: {transformation_data}")
    print(f"   Resultado transformado: {transformation_result}\n")
    
    # Pipeline condicional
    print("3. Pipeline Condicional:")
    conditional_pipeline = create_conditional_pipeline()
    
    conditional_data = [
        "  12  ",
        "  23  ",
        "  34  ",
        "  45  ",
        "  56  ",
        "  67  ",
        "  78  ",
        "  89  ",
        "  90  "
    ]
    
    conditional_result = conditional_pipeline.execute(iter(conditional_data))
    print(f"   Dados de entrada: {conditional_data}")
    print(f"   Resultado (números pares e positivos): {conditional_result}\n")


def demonstrate_pipeline_composition():
    """Demonstra como compor pipelines complexos."""
    print("=== Composição de Pipelines ===\n")
    
    # Cria pipelines menores
    preprocessing_pipeline = create_custom_pipeline(remove_extra_spaces)
    numeric_pipeline = create_custom_pipeline(
        filter_numeric_strings,
        convert_to_integers
    )
    
    # Combina os pipelines
    combined_pipeline = Pipeline()
    combined_pipeline.add_filter(preprocessing_pipeline.process)
    combined_pipeline.add_filter(numeric_pipeline.process)
    combined_pipeline.add_filter(lambda data: filter_greater_than(data, 50))
    
    # Dados de teste
    test_data = [
        "  123  ",
        "  abc  ",
        "  456  ",
        "  789  ",
        "  12   ",
        "  34   ",
        "  56   ",
        "  90   "
    ]
    
    print("Pipeline composto (pré-processamento + numérico + filtro > 50):")
    print(f"   Dados de entrada: {test_data}")
    
    result = combined_pipeline.execute(iter(test_data))
    print(f"   Resultado final: {result}")


if __name__ == "__main__":
    try:
        demonstrate_advanced_pipelines()
        demonstrate_pipeline_composition()
        
        print("\n=== Exemplos avançados executados com sucesso! ===")
        print("Estes exemplos demonstram a flexibilidade e poder")
        print("da arquitetura Pipes and Filters para casos complexos.")
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
