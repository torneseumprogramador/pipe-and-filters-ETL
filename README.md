# Pipes and Filters - Arquitetura de Software

Este projeto demonstra a implementação da arquitetura **Pipes and Filters** em Python, usando geradores para processamento lazy de dados.

## 📚 O que é Pipes and Filters?

A arquitetura **Pipes and Filters** é um padrão arquitetural que permite processar dados através de uma sequência de operações independentes (filtros) conectadas por canais (pipes).

### Componentes Principais:

- **Source (Fonte)**: Gera ou fornece os dados de entrada
- **Filters (Filtros)**: Processam os dados de forma independente
- **Pipes (Tubos)**: Conectam os filtros, passando dados entre eles
- **Sink (Destino)**: Consome os dados processados

### Fluxo de Dados:
```
Source → Filter1 → Filter2 → Filter3 → ... → FilterN → Sink
```

## 🎯 Problemas que Resolve

1. **Processamento Complexo**: Divide operações complexas em etapas simples
2. **Reutilização**: Filtros podem ser reutilizados em diferentes pipelines
3. **Manutenibilidade**: Cada filtro é independente e fácil de testar
4. **Escalabilidade**: Filtros podem ser executados em paralelo
5. **Flexibilidade**: Fácil reordenar, adicionar ou remover filtros

## ✅ Vantagens

- **Modularidade**: Cada filtro tem uma responsabilidade única
- **Testabilidade**: Filtros podem ser testados isoladamente
- **Reutilização**: Filtros podem ser combinados de diferentes formas
- **Manutenibilidade**: Mudanças em um filtro não afetam outros
- **Processamento Lazy**: Dados são processados conforme necessário

## ❌ Desvantagens

- **Overhead**: Pode haver overhead de comunicação entre filtros
- **Complexidade**: Para pipelines simples, pode ser excessivo
- **Debugging**: Pode ser difícil rastrear problemas através do pipeline
- **Performance**: Para datasets pequenos, o overhead pode não valer a pena

## 🏗️ Estrutura do Projeto

```
pipe-and-filters-ETL/
├── src/
│   ├── filters/
│   │   ├── __init__.py
│   │   ├── text_filters.py      # Filtros básicos de texto
│   │   └── social_filters.py    # Filtros para análise de comentários sociais
│   ├── pipes/
│   │   ├── __init__.py
│   │   ├── pipeline.py          # Pipeline base genérico
│   │   └── social_pipeline.py   # Pipeline especializado para comentários sociais
│   ├── __init__.py
│   ├── main.py                  # Demonstração básica do pipeline
│   └── social_analysis.py       # Análise de comentários sociais
├── data/
│   ├── __init__.py
│   ├── generator.py             # Gerador de comentários simulados
│   └── comments_dataset.json    # Dataset de exemplo
├── examples/
│   ├── __init__.py
│   └── advanced_usage.py        # Exemplos avançados
├── tests/
│   ├── __init__.py
│   ├── test_text_filters.py     # Testes dos filtros básicos
│   ├── test_pipeline.py         # Testes do pipeline base
│   └── test_social_filters.py   # Testes dos filtros sociais
├── run.py                       # Script interativo principal
├── setup.py                     # Configuração de instalação
├── LICENSE                      # Licença MIT
├── .gitignore                   # Arquivo gitignore
├── README.md                    # Documentação completa
└── QUICKSTART.md                # Guia de início rápido
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.7+
- Make (para usar o Makefile)
- Não são necessárias bibliotecas externas (Python puro)

### 🎯 Execução Rápida com Makefile (Recomendado)
```bash
# Navegar para o diretório do projeto
cd pipe-and-filters-ETL

# Ver todos os comandos disponíveis
make help

# Configuração inicial completa
make setup

# Demonstração completa (gera dados + executa demo)
make demo

# Inicialização rápida completa
make quick-start
```

### 🔧 Comandos Principais do Makefile
```bash
# Geração de dados
make generate-data          # Gera 100 comentários
make generate-data-small    # Gera 20 comentários (testes)
make generate-data-large    # Gera 500 comentários (demo)

# Execução de demonstrações
make basic-demo            # Pipeline básico
make social-analysis       # Análise de comentários sociais
make examples              # Exemplos avançados
make demo                  # Demonstração completa
make run                   # Script interativo

# Testes e qualidade
make test                  # Executa todos os testes
make test-quick           # Testes rapidamente
make test-coverage        # Testes com cobertura
make lint                 # Verificação de código
make format               # Formatação de código
make check-all            # Todos os checks

# Manutenção
make clean                # Limpa arquivos temporários
make install              # Instala dependências
make validate             # Valida estrutura do projeto
make show-status          # Mostra status atual
```

### 📝 Execução Manual (Alternativa)
```bash
# 1. Gerar dados simulados de comentários
python data/generator.py -n 100

# 2. Executar demonstração básica
python src/main.py

# 3. Executar análise de comentários sociais
python src/social_analysis.py

# 4. Usar script interativo
python run.py
```

### Executar os Testes
```bash
# Executar todos os testes
python -m unittest discover tests

# Executar testes específicos
python -m unittest tests.test_text_filters
python -m unittest tests.test_pipeline

# Executar com mais detalhes
python -m unittest discover tests -v
```

## 🔧 Implementação

### Filtros Implementados

#### Filtros Básicos de Texto:
1. **`remove_extra_spaces`**: Remove espaços extras e múltiplos
2. **`filter_numeric_strings`**: Filtra apenas strings numéricas
3. **`convert_to_integers`**: Converte strings para inteiros
4. **`filter_greater_than`**: Filtra números maiores que um limite

#### Filtros para Análise de Comentários Sociais:
5. **`clean_text`**: Limpa e normaliza texto dos comentários
6. **`filter_by_sentiment`**: Filtra por sentimento (positivo/negativo)
7. **`filter_by_language`**: Filtra por idioma detectado
8. **`filter_by_country`**: Filtra por países específicos
9. **`filter_by_likes_threshold`**: Filtra por faixa de likes
10. **`add_engagement_score`**: Calcula score de engajamento
11. **`detect_spam`**: Detecta comentários spam
12. **`normalize_user_names`**: Normaliza nomes de usuário
13. **`add_text_metrics`**: Adiciona métricas de texto

### Pipeline de Exemplo

#### Pipeline Básico de Texto:
O projeto implementa um pipeline que:
1. Remove espaços extras das strings
2. Filtra apenas strings numéricas
3. Converte strings para inteiros
4. Filtra apenas números maiores que 10

#### Pipeline de Análise de Comentários Sociais:
Pipeline especializado que:
1. Limpa e normaliza texto dos comentários
2. Normaliza nomes de usuário
3. Adiciona métricas de texto
4. Calcula score de engajamento
5. Detecta comentários spam
6. Filtra por sentimento, idioma, país ou likes

### Exemplo de Uso

#### Pipeline Básico:
```python
from src.pipes.pipeline import create_text_processing_pipeline

# Cria pipeline pré-configurado
pipeline = create_text_processing_pipeline()

# Dados de entrada
input_data = ["  123  ", "  abc  ", "  456  "]

# Processa os dados
result = pipeline.execute(iter(input_data))
print(result)  # [123, 456]
```

#### Pipeline de Análise Social:
```python
from src.pipes.social_pipeline import create_sentiment_analysis_pipeline

# Cria pipeline para análise de sentimentos
pipeline = create_sentiment_analysis_pipeline().add_sentiment_filter("positive")

# Carrega comentários de arquivo JSON
with open('data/comments_dataset.json', 'r') as f:
    comments = json.load(f)

# Analisa comentários positivos
positive_comments = pipeline.execute(iter(comments))
print(f"Encontrados {len(positive_comments)} comentários positivos")
```

## 🧪 Testes

O projeto inclui testes unitários abrangentes para:

- **Filtros individuais**: Testa cada filtro isoladamente
- **Pipeline**: Testa a funcionalidade de conexão dos filtros
- **Casos extremos**: Entrada vazia, tipos mistos, etc.
- **Processamento lazy**: Verifica que os dados são processados conforme necessário

## 🔍 Características Técnicas

- **Processamento Lazy**: Usa geradores Python para processar dados conforme necessário
- **Tipagem**: Inclui type hints para melhor documentação e IDE support
- **Iteradores**: Todos os filtros trabalham com iteradores para eficiência
- **Modularidade**: Cada filtro é independente e testável
- **Encadeamento**: Pipeline suporta encadeamento de métodos

## 📖 Casos de Uso

Esta arquitetura é ideal para:

- **ETL (Extract, Transform, Load)**: Processamento de dados
- **Streaming de dados**: Processamento de dados em tempo real
- **Pipeline de ML**: Pré-processamento de dados
- **Análise de logs**: Filtragem e transformação de logs
- **Processamento de arquivos**: Validação e transformação de dados
- **Análise de redes sociais**: Processamento de comentários e sentimentos
- **Moderação de conteúdo**: Detecção de spam e conteúdo inadequado
- **Análise de engajamento**: Métricas de interação e performance
- **Análise geográfica**: Filtragem por localização e região
- **Análise multilingue**: Processamento de conteúdo em diferentes idiomas

## 🤝 Contribuindo

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Implemente suas mudanças
4. Adicione testes para novas funcionalidades
5. Execute os testes existentes
6. Faça commit das mudanças
7. Abra um Pull Request

## 📄 Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## 🎓 Aprendizado

Este projeto serve como exemplo educacional para:

- Entender arquiteturas de software
- Aprender padrões de design
- Praticar programação funcional com Python
- Implementar processamento de dados eficiente
- Desenvolver código testável e modular
