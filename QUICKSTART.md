# 🚀 Guia de Início Rápido - Pipes and Filters

## ⚡ Execução Rápida

### 🎯 Com Makefile (Recomendado)
```bash
# Ver todos os comandos disponíveis
make help

# Inicialização rápida completa
make quick-start

# Ou passo a passo:
make setup              # Configuração inicial
make demo              # Demonstração completa
```

### 📝 Comandos Individuais
```bash
# 1. Gerar Dados Simulados
make generate-data

# 2. Executar Demonstração Básica
make basic-demo

# 3. Executar Análise de Comentários Sociais
make social-analysis

# 4. Executar Exemplos Avançados
make examples

# 5. Executar Todos os Testes
make test

# 6. Usar o Script Interativo
make run
```

### 🔧 Comandos de Desenvolvimento
```bash
make test-quick         # Testes rapidamente
make lint               # Verificar qualidade do código
make format             # Formatar código
make clean              # Limpar arquivos temporários
make show-status        # Ver status do projeto
```

## 🏗️ Estrutura Rápida

```
pipe-and-filters-ETL/
├── src/                    # Código fonte
│   ├── filters/           # Filtros de processamento
│   ├── pipes/             # Implementação dos pipes
│   └── main.py            # Demonstração principal
├── examples/               # Exemplos avançados
├── tests/                  # Testes unitários
└── run.py                  # Script interativo
```

## 🔧 Uso Básico

### Pipeline de Texto:
```python
from src.pipes.pipeline import create_text_processing_pipeline

# Cria pipeline pré-configurado
pipeline = create_text_processing_pipeline()

# Dados de entrada
data = ["  123  ", "  abc  ", "  456  "]

# Processa os dados
result = pipeline.execute(iter(data))
print(result)  # [123, 456]
```

### Pipeline de Análise Social:
```python
from src.pipes.social_pipeline import create_sentiment_analysis_pipeline

# Cria pipeline para análise de sentimentos
pipeline = create_sentiment_analysis_pipeline().add_sentiment_filter("positive")

# Carrega comentários
with open('data/comments_dataset.json', 'r') as f:
    comments = json.load(f)

# Analisa comentários positivos
positive_comments = pipeline.execute(iter(comments))
print(f"Encontrados {len(positive_comments)} comentários positivos")
```

## 📚 O que Aprender

- **Arquitetura Pipes and Filters**: Padrão para processamento de dados
- **Processamento Lazy**: Uso de geradores Python
- **Modularidade**: Filtros independentes e reutilizáveis
- **Testabilidade**: Código bem estruturado para testes

## 🎯 Próximos Passos

1. Execute a demonstração básica
2. Explore os exemplos avançados
3. Modifique os filtros existentes
4. Crie seus próprios filtros
5. Experimente diferentes combinações de pipeline

## ❓ Dúvidas?

Consulte o `README.md` completo para explicações detalhadas sobre:
- Conceitos da arquitetura
- Vantagens e desvantagens
- Casos de uso
- Implementação técnica
