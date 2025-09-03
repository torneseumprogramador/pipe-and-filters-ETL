# 🤝 Guia de Contribuição

Obrigado por se interessar em contribuir para o projeto **Pipes and Filters - Análise de Comentários Sociais**!

## 🚀 Como Contribuir

### 1. Fork e Clone
```bash
# Faça um fork do repositório
# Clone o seu fork
git clone https://github.com/SEU_USUARIO/pipe-and-filters-ETL.git
cd pipe-and-filters-ETL

# Adicione o repositório original como upstream
git remote add upstream https://github.com/torneseumprogramador/pipe-and-filters-ETL.git
```

### 2. Configuração do Ambiente
```bash
# Instale as dependências básicas
make install-faker

# Para desenvolvimento completo
make install-dev

# Para análise completa
make install-full
```

### 3. Desenvolvimento
```bash
# Crie uma branch para sua feature
git checkout -b feature/nova-funcionalidade

# Faça suas alterações
# Execute os testes
make test

# Verifique a qualidade do código
make check-all
```

### 4. Commit e Push
```bash
# Adicione suas alterações
git add .

# Faça o commit com mensagem descritiva
git commit -m "feat: adiciona nova funcionalidade X"

# Faça o push para sua branch
git push origin feature/nova-funcionalidade
```

### 5. Pull Request
- Crie um Pull Request no GitHub
- Descreva suas alterações
- Inclua testes se aplicável
- Aguarde a revisão

## 📋 Padrões de Código

### Python
- Use **Python 3.7+**
- Siga **PEP 8** para estilo
- Use **type hints** quando possível
- Documente funções e classes com **docstrings**

### Estrutura do Projeto
```
src/
├── filters/          # Filtros de processamento
├── pipes/           # Implementações de pipeline
├── main.py          # Ponto de entrada principal
└── analysis_engine.py # Motor de análise

tests/               # Testes unitários
examples/            # Exemplos de uso
notebooks/           # Notebooks Jupyter
data/                # Dados simulados
```

### Testes
- Escreva testes para novas funcionalidades
- Mantenha cobertura de testes alta
- Execute `make test` antes de commitar

### Documentação
- Atualize o README.md se necessário
- Documente novas funcionalidades
- Mantenha exemplos atualizados

## 🎯 Áreas para Contribuição

### Filtros
- Novos filtros de processamento
- Melhorias nos filtros existentes
- Otimizações de performance

### Pipelines
- Novos tipos de pipeline
- Melhorias na arquitetura
- Integração com outras bibliotecas

### Análise
- Novos tipos de visualização
- Algoritmos de análise
- Relatórios personalizados

### Dados
- Novos tipos de dados simulados
- Formatos de saída adicionais
- Validação de dados

### Documentação
- Melhorias no README
- Novos exemplos
- Tutoriais interativos

## 🐛 Reportando Bugs

### Antes de Reportar
1. Verifique se o bug já foi reportado
2. Teste com a versão mais recente
3. Reproduza o problema

### Template de Bug Report
```markdown
**Descrição do Bug**
Descrição clara e concisa do problema.

**Passos para Reproduzir**
1. Execute 'make generate-data'
2. Execute 'make analysis-report'
3. Veja o erro...

**Comportamento Esperado**
O que deveria acontecer.

**Comportamento Atual**
O que está acontecendo.

**Ambiente**
- OS: [ex: macOS 14.0]
- Python: [ex: 3.11.0]
- Versão do projeto: [ex: 1.0.0]

**Informações Adicionais**
Screenshots, logs, etc.
```

## 💡 Sugestões de Features

### Como Sugerir
1. Abra uma **Issue** no GitHub
2. Use o label **enhancement**
3. Descreva a funcionalidade desejada
4. Explique o benefício

### Exemplos de Features
- Novos tipos de filtros
- Integração com APIs externas
- Interface web
- Dashboard interativo
- Exportação para outros formatos

## 📚 Recursos Úteis

### Comandos Make
```bash
make help              # Ajuda
make install-faker     # Instala Faker
make generate-data     # Gera dados
make test             # Executa testes
make analysis-report   # Gera relatório
make notebook         # Inicia Jupyter
```

### Estrutura de Testes
```bash
# Testes básicos
make test-quick

# Testes com cobertura
make test-coverage

# Verificação de código
make check-all
```

## 🏷️ Labels para Issues

- **bug**: Problemas no código
- **enhancement**: Novas funcionalidades
- **documentation**: Melhorias na documentação
- **good first issue**: Ideal para iniciantes
- **help wanted**: Precisa de ajuda
- **question**: Dúvidas sobre o projeto

## 📞 Contato

- **Issues**: [GitHub Issues](https://github.com/torneseumprogramador/pipe-and-filters-ETL/issues)
- **Discussions**: [GitHub Discussions](https://github.com/torneseumprogramador/pipe-and-filters-ETL/discussions)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Obrigado por contribuir! 🎉**

Cada contribuição, por menor que seja, ajuda a tornar este projeto melhor para todos.
