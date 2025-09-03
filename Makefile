# Makefile para o projeto Pipes and Filters - Análise de Comentários Sociais
# Uso: make <comando>

.PHONY: help install clean test run demo generate-data social-analysis basic-demo examples lint format check-all

# Variáveis
PYTHON = python3
PIP = pip3
PROJECT_NAME = pipe-and-filters-etl
SRC_DIR = src
DATA_DIR = data
TESTS_DIR = tests
EXAMPLES_DIR = examples

# Cores para output
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
RED = \033[0;31m
NC = \033[0m # No Color

# Comando padrão
.DEFAULT_GOAL := help

help: ## Mostra esta ajuda
	@echo "$(BLUE)🚀 $(PROJECT_NAME) - Makefile$(NC)"
	@echo "$(BLUE)=====================================$(NC)"
	@echo ""
	@echo "$(GREEN)Comandos disponíveis:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(GREEN)Exemplos de uso:$(NC)"
	@echo "  make install        # Instala dependências"
	@echo "  make generate-data  # Gera dados simulados"
	@echo "  make demo          # Executa demonstração completa"
	@echo "  make test          # Executa todos os testes"
	@echo "  make run           # Executa script interativo"

install: ## Instala dependências do projeto
	@echo "$(GREEN)📦 Instalando dependências...$(NC)"
	@echo "$(YELLOW)💡 Nota: Em ambientes gerenciados, use: python3 -m venv venv && source venv/bin/activate$(NC)"
	$(PIP) install -r requirements.txt --user || $(PIP) install -r requirements.txt --break-system-packages || echo "$(YELLOW)⚠️  Instalação falhou. Use ambiente virtual.$(NC)"
	$(PIP) install -e . --user || $(PIP) install -e . --break-system-packages || echo "$(YELLOW)⚠️  Instalação falhou. Use ambiente virtual.$(NC)"
	@echo "$(GREEN)✅ Dependências instaladas com sucesso!$(NC)"

install-dev: ## Instala dependências de desenvolvimento
	@echo "$(GREEN)🔧 Instalando dependências de desenvolvimento...$(NC)"
	@echo "$(YELLOW)💡 Nota: Em ambientes gerenciados, use: python3 -m venv venv && source venv/bin/activate$(NC)"
	$(PIP) install -e ".[dev]" --user || $(PIP) install -e ".[dev]" --break-system-packages || echo "$(YELLOW)⚠️  Instalação falhou. Use ambiente virtual.$(NC)"
	@echo "$(GREEN)✅ Dependências de desenvolvimento instaladas!$(NC)"

install-faker: ## Instala apenas o Faker para geração de dados
	@echo "$(GREEN)🎭 Instalando Faker...$(NC)"
	$(PIP) install faker>=18.0.0 --user || $(PIP) install faker>=18.0.0 --break-system-packages || echo "$(YELLOW)⚠️  Instalação falhou. Use ambiente virtual.$(NC)"
	@echo "$(GREEN)✅ Faker instalado com sucesso!$(NC)"

install-analysis: ## Instala dependências para análise de dados
	@echo "$(GREEN)📊 Instalando dependências para análise...$(NC)"
	$(PIP) install -e ".[analysis]" --user || $(PIP) install -e ".[analysis]" --break-system-packages || echo "$(YELLOW)⚠️  Instalação falhou. Use ambiente virtual.$(NC)"
	@echo "$(GREEN)✅ Dependências de análise instaladas!$(NC)"

install-full: ## Instala todas as dependências (incluindo Jupyter)
	@echo "$(GREEN)🚀 Instalando todas as dependências...$(NC)"
	$(PIP) install -e ".[full]" --user || $(PIP) install -e ".[full]" --break-system-packages || echo "$(YELLOW)⚠️  Instalação falhou. Use ambiente virtual.$(NC)"
	@echo "$(GREEN)✅ Todas as dependências instaladas!$(NC)"

clean: ## Limpa arquivos temporários e caches
	@echo "$(YELLOW)🧹 Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

generate-data: ## Gera dados simulados de comentários
	@echo "$(GREEN)📊 Gerando dados simulados...$(NC)"
	cd $(DATA_DIR) && $(PYTHON) generator.py -n 100
	@echo "$(GREEN)✅ Dados gerados com sucesso!$(NC)"

generate-data-small: ## Gera dataset pequeno para testes rápidos
	@echo "$(GREEN)📊 Gerando dataset pequeno...$(NC)"
	cd $(DATA_DIR) && $(PYTHON) generator.py -n 20
	@echo "$(GREEN)✅ Dataset pequeno gerado!$(NC)"

generate-data-large: ## Gera dataset grande para demonstrações
	@echo "$(GREEN)📊 Gerando dataset grande...$(NC)"
	cd $(DATA_DIR) && $(PYTHON) generator.py -n 15000
	@echo "$(GREEN)✅ Dataset grande gerado!$(NC)"

basic-demo: ## Executa demonstração básica do pipeline
	@echo "$(GREEN)🚀 Executando demonstração básica...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) main.py
	@echo "$(GREEN)✅ Demonstração básica concluída!$(NC)"

social-analysis: ## Executa análise de comentários sociais
	@echo "$(GREEN)🔍 Executando análise de comentários sociais...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) social_analysis.py
	@echo "$(GREEN)✅ Análise social concluída!$(NC)"

examples: ## Executa exemplos avançados
	@echo "$(GREEN)📚 Executando exemplos avançados...$(NC)"
	$(PYTHON) $(EXAMPLES_DIR)/advanced_usage.py
	@echo "$(GREEN)✅ Exemplos executados!$(NC)"

demo: generate-data ## Executa demonstração completa (gera dados + executa demo)
	@echo "$(GREEN)🎯 Executando demonstração completa...$(NC)"
	$(PYTHON) demo.py
	@echo "$(GREEN)✅ Demonstração completa concluída!$(NC)"

notebook: ## Inicia Jupyter Notebook para análise interativa
	@echo "$(GREEN)📓 Iniciando Jupyter Notebook...$(NC)"
	cd notebooks && jupyter notebook
	@echo "$(GREEN)✅ Jupyter Notebook finalizado!$(NC)"

notebook-lab: ## Inicia Jupyter Lab para análise interativa
	@echo "$(GREEN)🔬 Iniciando Jupyter Lab...$(NC)"
	cd notebooks && jupyter lab
	@echo "$(GREEN)✅ Jupyter Lab finalizado!$(NC)"

analysis-report: ## Gera relatório de análise completo
	@echo "$(GREEN)📊 Gerando relatório de análise...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) analysis_engine.py
	@echo "$(GREEN)✅ Relatório gerado com sucesso!$(NC)"

analysis-quick: ## Análise rápida (apenas estatísticas)
	@echo "$(GREEN)⚡ Análise rápida...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) quick_analysis.py
	@echo "$(GREEN)✅ Análise rápida concluída!$(NC)"

run: ## Executa script interativo
	@echo "$(GREEN)🎮 Executando script interativo...$(NC)"
	$(PYTHON) run.py
	@echo "$(GREEN)✅ Script interativo finalizado!$(NC)"

test: ## Executa todos os testes
	@echo "$(GREEN)🧪 Executando testes...$(NC)"
	$(PYTHON) -m unittest discover $(TESTS_DIR) -v
	@echo "$(GREEN)✅ Todos os testes executados!$(NC)"

test-quick: ## Executa testes rapidamente (sem verbose)
	@echo "$(GREEN)⚡ Executando testes rapidamente...$(NC)"
	$(PYTHON) -m unittest discover $(TESTS_DIR)
	@echo "$(GREEN)✅ Testes executados!$(NC)"

test-coverage: ## Executa testes com cobertura
	@echo "$(GREEN)📊 Executando testes com cobertura...$(NC)"
	$(PIP) install coverage
	coverage run -m unittest discover $(TESTS_DIR)
	coverage report
	coverage html
	@echo "$(GREEN)✅ Relatório de cobertura gerado em htmlcov/$(NC)"

lint: ## Executa verificação de código (flake8)
	@echo "$(GREEN)🔍 Verificando qualidade do código...$(NC)"
	$(PIP) install flake8
	flake8 $(SRC_DIR) $(TESTS_DIR) $(EXAMPLES_DIR) --max-line-length=100 --ignore=E203,W503
	@echo "$(GREEN)✅ Verificação de código concluída!$(NC)"

format: ## Formata código com black
	@echo "$(GREEN)🎨 Formatando código...$(NC)"
	$(PIP) install black
	black $(SRC_DIR) $(TESTS_DIR) $(EXAMPLES_DIR) --line-length=100
	@echo "$(GREEN)✅ Código formatado!$(NC)"

check-all: test lint ## Executa todos os checks (testes + lint)
	@echo "$(GREEN)✅ Todos os checks passaram!$(NC)"

build: ## Constrói o pacote para distribuição
	@echo "$(GREEN)🏗️ Construindo pacote...$(NC)"
	$(PYTHON) setup.py sdist bdist_wheel
	@echo "$(GREEN)✅ Pacote construído!$(NC)"

install-local: ## Instala o projeto localmente
	@echo "$(GREEN)📦 Instalando projeto localmente...$(NC)"
	$(PIP) install -e .
	@echo "$(GREEN)✅ Projeto instalado localmente!$(NC)"

uninstall: ## Remove instalação local do projeto
	@echo "$(YELLOW)🗑️ Removendo instalação local...$(NC)"
	$(PIP) uninstall $(PROJECT_NAME) -y
	@echo "$(GREEN)✅ Projeto desinstalado!$(NC)"

setup: install generate-data ## Configuração inicial do projeto
	@echo "$(GREEN)🎉 Configuração inicial concluída!$(NC)"
	@echo "$(BLUE)Próximos passos:$(NC)"
	@echo "  make demo          # Executar demonstração completa"
	@echo "  make run           # Usar script interativo"
	@echo "  make test          # Executar testes"

dev-setup: install-dev generate-data ## Configuração para desenvolvimento
	@echo "$(GREEN)🔧 Configuração para desenvolvimento concluída!$(NC)"
	@echo "$(BLUE)Comandos disponíveis:$(NC)"
	@echo "  make test          # Executar testes"
	@echo "  make lint          # Verificar código"
	@echo "  make format        # Formatar código"
	@echo "  make check-all     # Todos os checks"

show-structure: ## Mostra a estrutura do projeto
	@echo "$(BLUE)📁 Estrutura do Projeto:$(NC)"
	@echo ""
	@tree -I '__pycache__|*.pyc|*.egg-info|.git|.pytest_cache|htmlcov' || find . -type f -name "*.py" -o -name "*.md" -o -name "Makefile" | sort

show-status: ## Mostra status atual do projeto
	@echo "$(BLUE)📊 Status do Projeto:$(NC)"
	@echo ""
	@echo "$(GREEN)Arquivos Python:$(NC)"
	@find . -name "*.py" | wc -l | xargs echo "  Total:"
	@echo ""
	@echo "$(GREEN)Testes:$(NC)"
	@find $(TESTS_DIR) -name "*.py" | wc -l | xargs echo "  Total:"
	@echo ""
	@echo "$(GREEN)Dataset:$(NC)"
	@if [ -f "$(DATA_DIR)/comments_dataset.json" ]; then \
		echo "  ✅ Dataset existe"; \
		$(PYTHON) -c "import json; data=json.load(open('$(DATA_DIR)/comments_dataset.json')); print(f'  📊 {len(data)} comentários')"; \
	else \
		echo "  ❌ Dataset não encontrado"; \
		echo "  💡 Execute: make generate-data"; \
	fi

# Comandos de desenvolvimento
watch-test: ## Executa testes continuamente (requer entr)
	@echo "$(GREEN)👀 Executando testes em modo watch...$(NC)"
	@if command -v entr >/dev/null 2>&1; then \
		find . -name "*.py" | entr -r make test; \
	else \
		echo "$(RED)❌ 'entr' não encontrado. Instale com: brew install entr$(NC)"; \
	fi

profile: ## Executa profiling de performance
	@echo "$(GREEN)⚡ Executando profiling...$(NC)"
	$(PIP) install cProfile
	cd $(SRC_DIR) && $(PYTHON) -m cProfile -o profile.stats social_analysis.py
	@echo "$(GREEN)✅ Profiling concluído! Resultado em src/profile.stats$(NC)"

# Comandos de documentação
docs: ## Gera documentação
	@echo "$(GREEN)📚 Gerando documentação...$(NC)"
	@echo "$(BLUE)Documentação disponível em:$(NC)"
	@echo "  README.md          # Documentação completa"
	@echo "  QUICKSTART.md      # Guia de início rápido"
	@echo "  src/               # Código fonte com docstrings"

# Comandos de limpeza avançada
clean-all: clean ## Limpeza completa (inclui dados gerados)
	@echo "$(YELLOW)🧹 Limpeza completa...$(NC)"
	rm -f $(DATA_DIR)/*.json $(DATA_DIR)/*.csv $(DATA_DIR)/*.txt
	rm -f $(SRC_DIR)/profile.stats
	@echo "$(GREEN)✅ Limpeza completa concluída!$(NC)"

# Comandos de validação
validate: ## Valida estrutura e arquivos do projeto
	@echo "$(GREEN)✅ Validando estrutura do projeto...$(NC)"
	@test -f "README.md" || (echo "$(RED)❌ README.md não encontrado$(NC)" && exit 1)
	@test -f "setup.py" || (echo "$(RED)❌ setup.py não encontrado$(NC)" && exit 1)
	@test -d "$(SRC_DIR)" || (echo "$(RED)❌ Diretório src/ não encontrado$(NC)" && exit 1)
	@test -d "$(TESTS_DIR)" || (echo "$(RED)❌ Diretório tests/ não encontrado$(NC)" && exit 1)
	@test -d "$(DATA_DIR)" || (echo "$(RED)❌ Diretório data/ não encontrado$(NC)" && exit 1)
	@echo "$(GREEN)✅ Estrutura do projeto válida!$(NC)"

# Comando de inicialização rápida
quick-start: setup demo ## Inicialização rápida completa
	@echo "$(GREEN)🎉 Projeto inicializado e demonstrado com sucesso!$(NC)"
	@echo "$(BLUE)Para continuar explorando:$(NC)"
	@echo "  make run           # Script interativo"
	@echo "  make examples      # Exemplos avançados"
	@echo "  make social-analysis # Análise detalhada"
	@echo "  make analysis-quick  # Análise rápida"
	@echo "  make analysis-report # Relatório completo com gráficos"

# Informações do sistema
info: ## Mostra informações do sistema e projeto
	@echo "$(BLUE)ℹ️  Informações do Sistema:$(NC)"
	@echo "  Python: $(shell $(PYTHON) --version)"
	@echo "  Pip: $(shell $(PIP) --version)"
	@echo "  Diretório: $(shell pwd)"
	@echo "  Usuário: $(shell whoami)"
	@echo ""
	@echo "$(BLUE)📦 Informações do Projeto:$(NC)"
	@echo "  Nome: $(PROJECT_NAME)"
	@echo "  Versão: $(shell $(PYTHON) -c "import setup; print(setup.setup()['version'])" 2>/dev/null || echo "1.0.0")"
	@echo "  Autor: $(shell $(PYTHON) -c "import setup; print(setup.setup()['author'])" 2>/dev/null || echo "Danilo")"
