"""
Arquivo principal que demonstra o uso da arquitetura Pipes and Filters.
"""

from pipes.pipeline import create_text_processing_pipeline, create_custom_pipeline
from filters.text_filters import (
    remove_extra_spaces, 
    filter_numeric_strings,
    convert_to_integers,
    filter_greater_than
)


def generate_sample_data() -> list[str]:
    """
    Gera dados de exemplo para demonstrar o pipeline.
    
    Returns:
        Lista de strings com dados variados para processamento
    """
    return [
        "  123  ",
        "  abc  ",
        "  456  ",
        "  789  ",
        "  def  ",
        "  12   ",
        "  34   ",
        "  56   ",
        "  78   ",
        "  90   ",
        "  100  ",
        "  200  ",
        "  300  ",
        "  400  ",
        "  500  "
    ]


def demonstrate_pipeline():
    """Demonstra o uso do pipeline de processamento de texto."""
    print("=== Demonstração da Arquitetura Pipes and Filters ===\n")
    
    # Dados de entrada
    input_data = generate_sample_data()
    print(f"Dados de entrada ({len(input_data)} itens):")
    print(f"  {input_data}\n")
    
    # Cria e executa o pipeline padrão
    print("1. Executando pipeline padrão:")
    pipeline = create_text_processing_pipeline()
    result = pipeline.execute(iter(input_data))
    print(f"   Resultado: {result}")
    print(f"   Total de itens processados: {len(result)}\n")
    
    # Demonstra o pipeline customizado
    print("2. Executando pipeline customizado (apenas limpeza de espaços):")
    custom_pipeline = create_custom_pipeline(remove_extra_spaces)
    custom_result = custom_pipeline.execute(iter(input_data))
    print(f"   Resultado: {custom_result}\n")
    
    # Demonstra o processamento lazy
    print("3. Demonstração de processamento lazy:")
    print("   Processando dados um por vez:")
    lazy_pipeline = create_text_processing_pipeline()
    lazy_result = lazy_pipeline.process(iter(input_data))
    
    count = 0
    for item in lazy_result:
        count += 1
        print(f"   Item {count}: {item}")
    
    print(f"\n   Total processado: {count} itens")


def demonstrate_step_by_step():
    """Demonstra cada etapa do pipeline separadamente."""
    print("\n=== Demonstração Passo a Passo ===\n")
    
    input_data = generate_sample_data()
    print(f"Dados originais: {input_data}\n")
    
    # Etapa 1: Remover espaços extras
    print("Etapa 1 - Remover espaços extras:")
    step1 = list(remove_extra_spaces(iter(input_data)))
    print(f"  {step1}\n")
    
    # Etapa 2: Filtrar strings numéricas
    print("Etapa 2 - Filtrar strings numéricas:")
    step2 = list(filter_numeric_strings(iter(step1)))
    print(f"  {step2}\n")
    
    # Etapa 3: Converter para inteiros
    print("Etapa 3 - Converter para inteiros:")
    step3 = list(convert_to_integers(iter(step2)))
    print(f"  {step3}\n")
    
    # Etapa 4: Filtrar maiores que 10
    print("Etapa 4 - Filtrar maiores que 10:")
    step4 = list(filter_greater_than(iter(step3), 10))
    print(f"  {step4}\n")
    
    print(f"Resultado final: {step4}")


if __name__ == "__main__":
    try:
        demonstrate_pipeline()
        demonstrate_step_by_step()
        
        print("\n=== Pipeline executado com sucesso! ===")
        print("Este exemplo demonstra como a arquitetura Pipes and Filters")
        print("permite processar dados de forma modular e eficiente.")
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()
