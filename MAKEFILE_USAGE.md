# 📋 Guia de Uso do Makefile

Este documento explica como usar o Makefile para gerenciar e executar o projeto Pipes and Filters.

## 🚀 Início Rápido

### Primeira Execução
```bash
# 1. Navegar para o projeto
cd pipe-and-filters-ETL

# 2. Ver todos os comandos disponíveis
make help

# 3. Configuração inicial completa
make setup

# 4. Demonstração completa
make demo
```

### Inicialização Rápida (Um Comando)
```bash
make quick-start
```

## 📊 Geração de Dados

### Comandos de Geração
```bash
# Dataset padrão (100 comentários)
make generate-data

# Dataset pequeno para testes (20 comentários)
make generate-data-small

# Dataset grande para demonstrações (500 comentários)
make generate-data-large
```

### Exemplos de Uso
```bash
# Gerar dados e executar demonstração
make demo                    # Gera dados + executa demo

# Apenas gerar dados
make generate-data

# Verificar status dos dados
make show-status
```

## 🎯 Execução de Demonstrações

### Demonstrações Disponíveis
```bash
# Pipeline básico de texto
make basic-demo

# Análise de comentários sociais
make social-analysis

# Exemplos avançados
make examples

# Demonstração completa (inclui geração de dados)
make demo

# Script interativo
make run
```

### Fluxo de Demonstração
```bash
# 1. Gerar dados
make generate-data

# 2. Executar demonstração básica
make basic-demo

# 3. Executar análise social
make social-analysis

# 4. Ver exemplos avançados
make examples
```

## 🧪 Testes e Qualidade

### Execução de Testes
```bash
# Todos os testes com detalhes
make test

# Testes rapidamente (sem verbose)
make test-quick

# Testes com cobertura
make test-coverage
```

### Verificação de Código
```bash
# Verificar qualidade (flake8)
make lint

# Formatar código (black)
make format

# Todos os checks (testes + lint)
make check-all
```

### Desenvolvimento Contínuo
```bash
# Executar testes em modo watch (requer entr)
make watch-test

# Profiling de performance
make profile
```

## 🔧 Manutenção e Configuração

### Instalação e Dependências
```bash
# Instalar projeto localmente
make install

# Instalar dependências de desenvolvimento
make install-dev

# Desinstalar projeto
make uninstall
```

### Limpeza e Validação
```bash
# Limpar arquivos temporários
make clean

# Limpeza completa (inclui dados)
make clean-all

# Validar estrutura do projeto
make validate

# Ver informações do sistema
make info
```

### Configuração de Desenvolvimento
```bash
# Configuração para desenvolvimento
make dev-setup

# Ver estrutura do projeto
make show-structure

# Ver status atual
make show-status
```

## 📦 Distribuição e Build

### Construção de Pacotes
```bash
# Construir pacote para distribuição
make build

# Instalar localmente
make install-local
```

## 🎮 Comandos de Desenvolvimento

### Workflow Típico
```bash
# 1. Desenvolver código
# ... editar arquivos ...

# 2. Executar testes
make test-quick

# 3. Verificar qualidade
make lint

# 4. Formatar código
make format

# 5. Testes completos
make test

# 6. Verificar tudo
make check-all
```

### Comandos de Debug
```bash
# Ver status do projeto
make show-status

# Validar estrutura
make validate

# Informações do sistema
make info

# Limpar e recomeçar
make clean-all
```

## 🔍 Comandos Especiais

### Documentação
```bash
# Gerar documentação
make docs
```

### Monitoramento
```bash
# Ver estrutura do projeto
make show-structure

# Status atual
make show-status

# Validação completa
make validate
```

## ⚠️ Solução de Problemas

### Problemas Comuns
```bash
# Se os testes falharem
make clean
make test

# Se houver problemas de importação
make install
make validate

# Se precisar recomeçar
make clean-all
make setup
```

### Verificações de Sistema
```bash
# Ver informações do sistema
make info

# Validar estrutura
make validate

# Ver status
make show-status
```

## 📚 Exemplos de Uso Real

### Cenário 1: Primeira Vez
```bash
make help              # Ver comandos
make setup             # Configuração inicial
make demo              # Demonstração completa
```

### Cenário 2: Desenvolvimento
```bash
make dev-setup         # Configuração para dev
make test-quick        # Testes rápidos
make lint              # Verificar código
make format            # Formatar código
make check-all         # Todos os checks
```

### Cenário 3: Demonstração
```bash
make generate-data-large  # Dataset grande
make demo                  # Demonstração completa
make social-analysis       # Análise detalhada
```

### Cenário 4: Manutenção
```bash
make clean               # Limpar temporários
make validate            # Validar estrutura
make test                # Executar testes
make show-status         # Ver status
```

## 🎯 Dicas de Uso

1. **Sempre use `make help`** para ver comandos disponíveis
2. **Use `make setup`** para primeira configuração
3. **Use `make quick-start`** para inicialização rápida
4. **Use `make test-quick`** durante desenvolvimento
5. **Use `make check-all`** antes de commits
6. **Use `make clean`** se houver problemas
7. **Use `make show-status`** para verificar estado

## 🔗 Comandos Relacionados

- **`make help`** - Mostra todos os comandos
- **`make setup`** - Configuração inicial
- **`make demo`** - Demonstração completa
- **`make test`** - Executar testes
- **`make run`** - Script interativo
- **`make clean`** - Limpeza básica
- **`make validate`** - Validação do projeto
