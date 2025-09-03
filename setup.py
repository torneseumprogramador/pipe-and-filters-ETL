"""
Configuração de instalação para o projeto Pipes and Filters.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pipes-and-filters-etl",
    version="1.0.0",
    author="Danilo",
    author_email="danilo@example.com",
    description="Projeto educacional demonstrando a arquitetura Pipes and Filters em Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/pipes-and-filters-etl",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Architecture",
        "Topic :: Education",
    ],
    python_requires=">=3.7",
    install_requires=[
        "faker>=18.0.0",  # Para geração de dados simulados
        "pandas>=1.3.0",  # Para manipulação de dados
        "matplotlib>=3.5.0",  # Para visualizações básicas
        "seaborn>=0.11.0",  # Para visualizações estatísticas
        "numpy>=1.21.0",  # Para operações numéricas
        "jupyter>=1.0.0",  # Para notebooks interativos
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "analysis": [
            "scikit-learn>=1.0.0",  # Para análise de sentimentos
            "textblob>=0.15.0",  # Para processamento de texto
            "wordcloud>=1.8.0",  # Para nuvens de palavras
            "nltk>=3.6",  # Para processamento de linguagem natural
        ],
        "full": [
            "jupyter>=1.0.0",  # Para notebooks interativos
            "plotly>=5.0.0",  # Para gráficos interativos
            "scikit-learn>=1.0.0",  # Para análise de sentimentos
            "textblob>=0.15.0",  # Para processamento de texto
            "wordcloud>=1.8.0",  # Para nuvens de palavras
            "nltk>=3.6",  # Para processamento de linguagem natural
        ],
    },
    entry_points={
        "console_scripts": [
            "pipes-filters=run:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
