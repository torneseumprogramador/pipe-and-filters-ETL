# 🔍 Guia Completo: Arquitetura Pipes and Filters

## 📚 Visão Geral

Este guia te ajudará a entender **cada passo** da arquitetura Pipes and Filters analisando o código do projeto. Vamos percorrer desde os conceitos básicos até a implementação prática.

## 🏗️ Conceitos Fundamentais

### O que é Pipes and Filters?

A arquitetura Pipes and Filters é um padrão que processa dados através de uma sequência de operações independentes:

```
Source → Filter1 → Filter2 → Filter3 → ... → FilterN → Sink
```

- **Source (Fonte)**: Gera ou fornece dados
- **Filters (Filtros)**: Processam dados independentemente
- **Pipes (Tubos)**: Conectam filtros, passando dados
- **Sink (Destino)**: Consome dados processados

## 🎯 Objetivos de Aprendizado

Ao final deste guia, você será capaz de:
- ✅ Entender cada componente da arquitetura
- ✅ Identificar como os filtros funcionam
- ✅ Compreender o processamento lazy
- ✅ Analisar o código passo a passo
- ✅ Criar seus próprios filtros e pipelines

---

## 🚀 PARTE 1: Estrutura do Projeto

### 📁 Organização dos Arquivos

```
src/
├── filters/           # 🎯 FILTROS (processamento de dados)
│   ├── text_filters.py      # Filtros básicos de texto
│   └── social_filters.py    # Filtros para análise social
├── pipes/            # 🔗 PIPES (conexões entre filtros)
│   ├── pipeline.py          # Pipeline base genérico
│   └── social_pipeline.py   # Pipeline especializado
├── main.py           # 🎬 DEMONSTRAÇÃO (exemplo prático)
└── analysis_engine.py # 📊 ANÁLISE (uso real dos filtros)
```

### 🔍 O que cada pasta representa:

- **`filters/`** = Operações de processamento (transformam dados)
- **`pipes/`** = Conexões e orquestração (ligam filtros)
- **`main.py`** = Exemplo prático (demonstra o conceito)
- **`analysis_engine.py`** = Aplicação real (usa os filtros)

---

## 🎯 PARTE 2: Análise dos Filtros

### 📖 Vamos analisar `src/filters/text_filters.py`

Este arquivo contém os **filtros básicos** que demonstram o conceito fundamental.

#### 🔍 Filtro 1: `remove_extra_spaces`

```python
def remove_extra_spaces(data: Iterator[str]) -> Iterator[str]:
    """Remove espaços extras e múltiplos."""
    for item in data:
        cleaned = ' '.join(item.split())
        yield cleaned
```

**O que faz:**
- Recebe um iterador de strings
- Para cada string, remove espaços extras
- **Retorna um novo iterador** (não modifica o original)

**Por que é um filtro:**
- ✅ **Independente**: Não depende de outros filtros
- ✅ **Testável**: Pode ser testado isoladamente
- ✅ **Reutilizável**: Pode ser usado em qualquer pipeline
- ✅ **Lazy**: Processa dados conforme necessário

#### 🔍 Filtro 2: `filter_numeric_strings`

```python
def filter_numeric_strings(data: Iterator[str]) -> Iterator[str]:
    """Filtra apenas strings que representam números."""
    for item in data:
        if item.isdigit():
            yield item
```

**O que faz:**
- Recebe strings
- **Filtra** apenas as que são números
- Passa adiante apenas os números

**Características do filtro:**
- ✅ **Seletivo**: Remove dados que não atendem ao critério
- ✅ **Não destrutivo**: Não modifica os dados válidos
- ✅ **Eficiente**: Processa um item por vez

#### 🔍 Filtro 3: `convert_to_integers`

```python
def convert_to_integers(data: Iterator[str]) -> Iterator[int]:
    """Converte strings numéricas para inteiros."""
    for item in data:
        yield int(item)
```

**O que faz:**
- Recebe strings numéricas
- **Transforma** cada string em inteiro
- Muda o tipo de dados

**Características do filtro:**
- ✅ **Transformador**: Muda o tipo/formato dos dados
- ✅ **Determinístico**: Sempre produz o mesmo resultado
- ✅ **Sequencial**: Processa na ordem recebida

#### 🔍 Filtro 4: `filter_greater_than`

```python
def filter_greater_than(data: Iterator[int], threshold: int = 10) -> Iterator[int]:
    """Filtra números maiores que um limite."""
    for item in data:
        if item > threshold:
            yield item
```

**O que faz:**
- Recebe números inteiros
- **Filtra** apenas os maiores que o limite
- Permite configuração (threshold)

**Características do filtro:**
- ✅ **Configurável**: Aceita parâmetros
- ✅ **Condicional**: Aplica lógica de negócio
- ✅ **Flexível**: Pode ser usado com diferentes limites

---

## 🔗 PARTE 3: Análise dos Pipes

### 📖 Vamos analisar `src/pipes/pipeline.py`

Este arquivo implementa a **conexão** entre os filtros.

#### 🔍 Classe `Pipeline`

```python
class Pipeline:
    def __init__(self):
        self.filters = []
    
    def add_filter(self, filter_func):
        self.filters.append(filter_func)
        return self  # Permite encadeamento
    
    def process(self, data: Iterator) -> Iterator:
        """Aplica filtros sequencialmente."""
        result = data
        for filter_func in self.filters:
            result = filter_func(result)
        return result
```

**Como funciona:**

1. **Inicialização**: Lista vazia de filtros
2. **Adição**: Cada filtro é adicionado à lista
3. **Processamento**: Dados passam por cada filtro em sequência

#### 🔍 Método `process()` - O Coração do Pipeline

```python
def process(self, data: Iterator) -> Iterator:
    result = data
    for filter_func in self.filters:
        result = filter_func(result)
    return result
```

**Passo a passo:**

1. **`result = data`**: Começa com os dados originais
2. **`for filter_func in self.filters`**: Para cada filtro na lista
3. **`result = filter_func(result)`**: Aplica o filtro aos dados atuais
4. **`return result`**: Retorna o resultado final

**Exemplo visual:**
```
Dados originais: ['  123  ', '  abc  ', '  456  ']
    ↓
Filtro 1 (remove_extra_spaces): ['123', 'abc', '456']
    ↓
Filtro 2 (filter_numeric_strings): ['123', '456']
    ↓
Filtro 3 (convert_to_integers): [123, 456]
    ↓
Filtro 4 (filter_greater_than): [123, 456]
```

---

## 🎬 PARTE 4: Análise da Demonstração

### 📖 Vamos analisar `src/main.py`

Este arquivo **demonstra** como tudo funciona junto.

#### 🔍 Função `demonstrate_pipeline()`

```python
def demonstrate_pipeline():
    # 1. Dados de entrada
    input_data = ['  123  ', '  abc  ', '  456  ', ...]
    
    # 2. Cria pipeline padrão
    pipeline = create_text_processing_pipeline()
    
    # 3. Executa pipeline
    result = pipeline.execute(iter(input_data))
```

**O que acontece em cada passo:**

1. **Dados de entrada**: Lista estática para demonstração
2. **Criação do pipeline**: Função factory cria pipeline configurado
3. **Execução**: Pipeline processa todos os dados de uma vez

#### 🔍 Função `demonstrate_step_by_step()`

```python
def demonstrate_step_by_step():
    # Etapa 1: Remover espaços extras
    step1 = list(remove_extra_spaces(iter(input_data)))
    
    # Etapa 2: Filtrar strings numéricas
    step2 = list(filter_numeric_strings(iter(step1)))
    
    # Etapa 3: Converter para inteiros
    step3 = list(convert_to_integers(iter(step2)))
    
    # Etapa 4: Filtrar maiores que 10
    step4 = list(filter_greater_than(iter(step3), 10))
```

**Por que `list()` e `iter()`?**

- **`iter(input_data)`**: Converte lista em iterador (lazy)
- **`list(...)`**: Coleta todos os resultados para mostrar
- **Demonstração**: Mostra o resultado de cada etapa

---

## 🔄 PARTE 5: Processamento Lazy

### 💡 O que é Processamento Lazy?

**Processamento lazy** significa que os dados são processados **conforme necessário**, não todos de uma vez.

#### 🔍 Exemplo no código:

```python
# Pipeline lazy
lazy_pipeline = create_text_processing_pipeline()
lazy_result = lazy_pipeline.process(iter(input_data))

# Processa um por vez
for item in lazy_result:
    print(f"Item: {item}")
```

**Vantagens do Lazy:**

- ✅ **Memória eficiente**: Não carrega todos os dados
- ✅ **Processamento sob demanda**: Só processa quando necessário
- ✅ **Escalabilidade**: Funciona com datasets grandes
- ✅ **Responsividade**: Pode começar a mostrar resultados imediatamente

---

## 🧪 PARTE 6: Testes dos Filtros

### 📖 Vamos analisar `tests/test_text_filters.py`

Os testes mostram como **cada filtro funciona isoladamente**.

#### 🔍 Teste do Filtro `remove_extra_spaces`:

```python
def test_remove_extra_spaces(self):
    input_data = ['  hello  ', '  world  ']
    result = list(remove_extra_spaces(iter(input_data)))
    expected = ['hello', 'world']
    self.assertEqual(result, expected)
```

**O que o teste verifica:**

1. **Entrada**: Dados com espaços extras
2. **Processamento**: Aplicação do filtro
3. **Saída**: Dados limpos
4. **Validação**: Resultado esperado

#### 🔍 Teste do Filtro `filter_numeric_strings`:

```python
def test_filter_numeric_strings(self):
    input_data = ['123', 'abc', '456', 'def']
    result = list(filter_numeric_strings(iter(input_data)))
    expected = ['123', '456']
    self.assertEqual(result, expected)
```

**O que o teste verifica:**

1. **Entrada**: Mistura de números e texto
2. **Processamento**: Filtro seleciona apenas números
3. **Saída**: Apenas strings numéricas
4. **Validação**: Filtro funcionou corretamente

---

## 🔧 PARTE 7: Como Criar Seus Próprios Filtros

### 📝 Template para Novos Filtros:

```python
def meu_filtro_personalizado(data: Iterator[TipoEntrada]) -> Iterator[TipoSaida]:
    """
    Descrição do que o filtro faz.
    
    Args:
        data: Iterador com dados de entrada
        
    Yields:
        Dados processados um por vez
    """
    for item in data:
        # Lógica de processamento
        processed_item = processar(item)
        
        # Condição para incluir/excluir
        if condicao_valida(processed_item):
            yield processed_item
```

### 🎯 Exemplo Prático:

```python
def filter_positive_numbers(data: Iterator[int]) -> Iterator[int]:
    """Filtra apenas números positivos."""
    for number in data:
        if number > 0:
            yield number

def add_metadata(data: Iterator[str]) -> Iterator[dict]:
    """Adiciona metadados aos dados."""
    for item in data:
        metadata = {
            'value': item,
            'length': len(item),
            'timestamp': time.time()
        }
        yield metadata
```

---

## 🚀 PARTE 8: Como Criar Seus Próprios Pipelines

### 📝 Template para Novos Pipelines:

```python
def create_meu_pipeline():
    """Cria um pipeline personalizado."""
    pipeline = Pipeline()
    
    # Adiciona filtros na ordem desejada
    pipeline.add_filter(filtro1)
    pipeline.add_filter(filtro2)
    pipeline.add_filter(filtro3)
    
    return pipeline
```

### 🎯 Exemplo Prático:

```python
def create_data_cleaning_pipeline():
    """Pipeline para limpeza de dados."""
    pipeline = Pipeline()
    
    pipeline.add_filter(remove_duplicates)
    pipeline.add_filter(remove_empty_values)
    pipeline.add_filter(normalize_text)
    pipeline.add_filter(validate_format)
    
    return pipeline
```

---

## 🔍 PARTE 9: Análise Passo a Passo do Código

### 📋 Vamos seguir o fluxo completo:

#### 1. **Entrada de Dados**
```python
input_data = ['  123  ', '  abc  ', '  456  ']
```

#### 2. **Criação do Pipeline**
```python
pipeline = create_text_processing_pipeline()
# Internamente: adiciona 4 filtros na ordem correta
```

#### 3. **Processamento Sequencial**
```python
# Dados originais: ['  123  ', '  abc  ', '  456  ']
#    ↓
# Filtro 1 (remove_extra_spaces): ['123', 'abc', '456']
#    ↓
# Filtro 2 (filter_numeric_strings): ['123', '456']
#    ↓
# Filtro 3 (convert_to_integers): [123, 456]
#    ↓
# Filtro 4 (filter_greater_than): [123, 456]
```

#### 4. **Resultado Final**
```python
result = [123, 456]  # Apenas números > 10
```

---

## 🎯 PARTE 10: Exercícios Práticos

### 📝 Exercício 1: Criar um Filtro de Validação

Crie um filtro que valide se as strings têm pelo menos 3 caracteres:

```python
def filter_min_length(data: Iterator[str], min_length: int = 3) -> Iterator[str]:
    """Filtra strings com comprimento mínimo."""
    # Seu código aqui
    pass
```

### 📝 Exercício 2: Criar um Pipeline de Validação

Crie um pipeline que valide e limpe dados:

```python
def create_validation_pipeline():
    """Pipeline para validação de dados."""
    # Seu código aqui
    pass
```

### 📝 Exercício 3: Analisar o Comportamento

Execute o código e observe:
1. Como os dados mudam em cada etapa
2. Qual filtro remove mais dados
3. Como o processamento lazy funciona

---

## 🔍 PARTE 11: Debugging e Troubleshooting

### 🐛 Problemas Comuns:

#### **Erro: "Iterator is exhausted"**
```python
# ❌ Erro: Tentar usar iterador duas vezes
data = iter(['a', 'b', 'c'])
result1 = list(data)  # Funciona
result2 = list(data)  # Lista vazia!

# ✅ Solução: Criar novo iterador
data = ['a', 'b', 'c']
result1 = list(iter(data))
result2 = list(iter(data))
```

#### **Erro: "Filter not callable"**
```python
# ❌ Erro: Adicionar função incorreta
pipeline.add_filter("not_a_function")

# ✅ Solução: Adicionar função válida
pipeline.add_filter(remove_extra_spaces)
```

#### **Erro: "Data type mismatch"**
```python
# ❌ Erro: Filtro espera int, recebe str
filter_greater_than(iter(['a', 'b', 'c']))

# ✅ Solução: Usar filtros na ordem correta
# Primeiro converter, depois filtrar
```

---

## 📚 PARTE 12: Recursos Adicionais

### 🔗 Arquivos para Estudar:

1. **`src/filters/text_filters.py`** - Filtros básicos
2. **`src/pipes/pipeline.py`** - Implementação do pipeline
3. **`src/main.py`** - Demonstração prática
4. **`tests/test_text_filters.py`** - Testes dos filtros

### 🎯 Comandos para Executar:

```bash
# Executar demonstração básica
make basic-demo

# Executar testes
make test

# Ver estrutura do projeto
make show-structure

# Análise rápida
make analysis-quick
```

### 📖 Conceitos Relacionados:

- **Generators (yield)**: Como funcionam os iteradores
- **Iterator Protocol**: Padrão Python para iteração
- **Functional Programming**: Paradigma de programação
- **Data Processing**: Processamento de dados em larga escala

---

## 🎉 Conclusão

### ✅ O que você aprendeu:

1. **Arquitetura Pipes and Filters**: Conceito e implementação
2. **Filtros**: Como criar operações independentes
3. **Pipelines**: Como conectar filtros sequencialmente
4. **Processamento Lazy**: Eficiência e escalabilidade
5. **Testes**: Como validar cada componente
6. **Debugging**: Como resolver problemas comuns

### 🚀 Próximos Passos:

1. **Experimente**: Modifique os filtros existentes
2. **Crie**: Desenvolva seus próprios filtros
3. **Teste**: Valide com diferentes tipos de dados
4. **Aplique**: Use em seus próprios projetos
5. **Explore**: Estude os filtros sociais para casos mais complexos

### 💡 Dica Final:

A arquitetura Pipes and Filters é poderosa porque **separa responsabilidades**. Cada filtro faz uma coisa bem, e os pipelines permitem combinações flexíveis. É como LEGO para processamento de dados! 🧱

---

**🎯 Agora você está pronto para entender e trabalhar com a arquitetura Pipes and Filters!**

Execute o código, modifique os filtros, crie novos pipelines e veja como tudo funciona na prática. A melhor forma de aprender é experimentando! 🚀
