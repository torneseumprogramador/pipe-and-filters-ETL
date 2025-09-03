#!/usr/bin/env python3
"""
Script principal para executar o projeto Pipes and Filters.
Permite escolher entre diferentes demonstrações.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
    """Função principal que permite escolher a demonstração."""
    print("🚀 Projeto Pipes and Filters - Arquitetura de Software")
    print("=" * 60)
    print()
    print("Escolha uma opção:")
    print("1. Demonstração básica do pipeline")
    print("2. Exemplos avançados")
    print("3. Executar todos os testes")
    print("4. Sair")
    print()
    
    while True:
        try:
            choice = input("Digite sua escolha (1-4): ").strip()
            
            if choice == '1':
                print("\n" + "="*60)
                print("Executando demonstração básica...")
                print("="*60 + "\n")
                
                from main import demonstrate_pipeline, demonstrate_step_by_step
                demonstrate_pipeline()
                demonstrate_step_by_step()
                
            elif choice == '2':
                print("\n" + "="*60)
                print("Executando exemplos avançados...")
                print("="*60 + "\n")
                
                # Adiciona o diretório examples ao path
                examples_path = os.path.join(os.path.dirname(__file__), 'examples')
                sys.path.insert(0, examples_path)
                
                from advanced_usage import (
                    demonstrate_advanced_pipelines,
                    demonstrate_pipeline_composition
                )
                demonstrate_advanced_pipelines()
                demonstrate_pipeline_composition()
                
            elif choice == '3':
                print("\n" + "="*60)
                print("Executando todos os testes...")
                print("="*60 + "\n")
                
                import subprocess
                result = subprocess.run([
                    sys.executable, '-m', 'unittest', 'discover', 'tests', '-v'
                ], capture_output=True, text=True)
                
                print(result.stdout)
                if result.stderr:
                    print("Erros:", result.stderr)
                
            elif choice == '4':
                print("\n👋 Obrigado por usar o projeto Pipes and Filters!")
                break
                
            else:
                print("❌ Opção inválida. Por favor, escolha 1, 2, 3 ou 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Execução interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro durante a execução: {e}")
            import traceback
            traceback.print_exc()
        
        if choice in ['1', '2', '3']:
            print("\n" + "="*60)
            input("Pressione Enter para continuar...")
            print()


if __name__ == "__main__":
    main()
