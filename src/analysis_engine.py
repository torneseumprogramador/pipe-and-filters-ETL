#!/usr/bin/env python3
"""
Motor de análise leve para comentários sociais.
Gera relatórios visuais e estatísticas sem depender de Jupyter.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Any
import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.dirname(__file__))

from filters.social_filters import *
from pipes.social_pipeline import *


class SocialAnalysisEngine:
    """Motor de análise para comentários sociais."""
    
    def __init__(self, data_path: str = "data/comments_dataset.json"):
        """Inicializa o motor de análise."""
        self.data_path = data_path
        self.comments = None
        self.df = None
        self.load_data()
        
        # Configuração para gráficos
        plt.style.use('default')
        sns.set_palette("husl")
        
    def load_data(self):
        """Carrega os dados dos comentários."""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.comments = json.load(f)
            self.df = pd.DataFrame(self.comments)
            print(f"✅ Dados carregados: {len(self.comments)} comentários")
        except FileNotFoundError:
            print(f"❌ Arquivo não encontrado: {self.data_path}")
            print("💡 Execute 'make generate-data' primeiro")
            sys.exit(1)
    
    def basic_statistics(self) -> Dict[str, Any]:
        """Calcula estatísticas básicas dos dados."""
        stats = {
            "total_comments": len(self.df),
            "positive_comments": len(self.df[self.df['sentiment'] == 'positive']),
            "negative_comments": len(self.df[self.df['sentiment'] == 'negative']),
            "avg_likes": self.df['likes'].mean(),
            "max_likes": self.df['likes'].max(),
            "min_likes": self.df['likes'].min(),
            "unique_countries": self.df['country'].nunique(),
            "unique_users": self.df['user'].nunique(),
            "avg_text_length": self.df['text'].str.len().mean()
        }
        
        stats["positive_percentage"] = (stats["positive_comments"] / stats["total_comments"]) * 100
        stats["negative_percentage"] = (stats["negative_comments"] / stats["total_comments"]) * 100
        
        return stats
    
    def print_statistics(self):
        """Imprime estatísticas formatadas."""
        stats = self.basic_statistics()
        
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS DOS COMENTÁRIOS SOCIAIS")
        print("="*60)
        print(f"📝 Total de comentários: {stats['total_comments']:,}")
        print(f"😊 Comentários positivos: {stats['positive_comments']:,} ({stats['positive_percentage']:.1f}%)")
        print(f"😞 Comentários negativos: {stats['negative_comments']:,} ({stats['negative_percentage']:.1f}%)")
        print(f"👍 Média de likes: {stats['avg_likes']:.1f}")
        print(f"🔥 Máximo de likes: {stats['max_likes']:,}")
        print(f"🌍 Países únicos: {stats['unique_countries']}")
        print(f"👥 Usuários únicos: {stats['unique_users']}")
        print(f"📏 Comprimento médio do texto: {stats['avg_text_length']:.1f} caracteres")
        print("="*60)
    
    def create_sentiment_chart(self, save_path: str = "notebooks/reports/sentiment_distribution.png"):
        """Cria gráfico de distribuição de sentimentos."""
        plt.figure(figsize=(10, 6))
        
        sentiment_counts = self.df['sentiment'].value_counts()
        colors = ['#2E8B57', '#DC143C']
        
        plt.pie(sentiment_counts.values, labels=sentiment_counts.index, 
                colors=colors, autopct='%1.1f%%', startangle=90)
        plt.title('Distribuição de Sentimentos dos Comentários', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        # Salva o gráfico
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Gráfico de sentimentos salvo: {save_path}")
    
    def create_likes_distribution(self, save_path: str = "notebooks/reports/likes_distribution.png"):
        """Cria gráfico de distribuição de likes."""
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.hist(self.df['likes'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Distribuição de Likes', fontweight='bold')
        plt.xlabel('Número de Likes')
        plt.ylabel('Frequência')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        self.df.boxplot(column='likes', by='sentiment', ax=plt.gca())
        plt.title('Likes por Sentimento', fontweight='bold')
        plt.suptitle('')  # Remove título automático
        
        plt.tight_layout()
        
        # Salva o gráfico
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Gráfico de likes salvo: {save_path}")
    
    def create_country_analysis(self, save_path: str = "notebooks/reports/country_analysis.png"):
        """Cria análise por país."""
        plt.figure(figsize=(14, 8))
        
        # Top 10 países por número de comentários
        country_counts = self.df['country'].value_counts().head(10)
        
        plt.subplot(2, 2, 1)
        country_counts.plot(kind='bar', color='lightcoral')
        plt.title('Top 10 Países por Comentários', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Número de Comentários')
        
        # Média de likes por país (top 10)
        plt.subplot(2, 2, 2)
        country_likes = self.df.groupby('country')['likes'].mean().sort_values(ascending=False).head(10)
        country_likes.plot(kind='bar', color='lightgreen')
        plt.title('Média de Likes por País (Top 10)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Média de Likes')
        
        # Sentimento por país
        plt.subplot(2, 2, 3)
        sentiment_by_country = pd.crosstab(self.df['country'], self.df['sentiment'])
        sentiment_by_country.head(10).plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Sentimento por País (Top 10)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Número de Comentários')
        plt.legend(title='Sentimento')
        
        # Comprimento do texto por país
        plt.subplot(2, 2, 4)
        text_length_by_country = self.df.groupby('country')['text'].apply(lambda x: x.str.len().mean()).sort_values(ascending=False).head(10)
        text_length_by_country.plot(kind='bar', color='gold')
        plt.title('Comprimento Médio do Texto por País (Top 10)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Caracteres Médios')
        
        plt.tight_layout()
        
        # Salva o gráfico
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Análise por país salva: {save_path}")
    
    def create_text_analysis(self, save_path: str = "notebooks/reports/text_analysis.png"):
        """Cria análise de texto."""
        plt.figure(figsize=(14, 8))
        
        # Comprimento do texto por sentimento
        plt.subplot(2, 2, 1)
        positive_texts = self.df[self.df['sentiment'] == 'positive']['text'].str.len()
        negative_texts = self.df[self.df['sentiment'] == 'negative']['text'].str.len()
        
        plt.hist(positive_texts, bins=20, alpha=0.7, label='Positivo', color='green')
        plt.hist(negative_texts, bins=20, alpha=0.7, label='Negativo', color='red')
        plt.title('Distribuição do Comprimento do Texto por Sentimento', fontweight='bold')
        plt.xlabel('Comprimento do Texto (caracteres)')
        plt.ylabel('Frequência')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Palavras mais comuns (simulação)
        plt.subplot(2, 2, 2)
        # Conta palavras simples (exemplo)
        all_words = ' '.join(self.df['text'].str.lower()).split()
        word_counts = pd.Series(all_words).value_counts().head(10)
        word_counts.plot(kind='bar', color='lightblue')
        plt.title('Palavras Mais Comuns (Top 10)', fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.ylabel('Frequência')
        
        # Relação entre likes e comprimento do texto
        plt.subplot(2, 2, 3)
        plt.scatter(self.df['text'].str.len(), self.df['likes'], alpha=0.6, color='purple')
        plt.title('Relação: Likes vs Comprimento do Texto', fontweight='bold')
        plt.xlabel('Comprimento do Texto (caracteres)')
        plt.ylabel('Número de Likes')
        plt.grid(True, alpha=0.3)
        
        # Distribuição de sentimentos por faixa de likes
        plt.subplot(2, 2, 4)
        self.df['likes_category'] = pd.cut(self.df['likes'], bins=[0, 10, 50, 100, 200], 
                                          labels=['0-10', '11-50', '51-100', '100+'])
        sentiment_likes = pd.crosstab(self.df['likes_category'], self.df['sentiment'])
        sentiment_likes.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Sentimento por Faixa de Likes', fontweight='bold')
        plt.xlabel('Faixa de Likes')
        plt.ylabel('Número de Comentários')
        plt.legend(title='Sentimento')
        plt.xticks(rotation=0)
        
        plt.tight_layout()
        
        # Salva o gráfico
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Análise de texto salva: {save_path}")
    
    def create_pipeline_analysis(self, save_path: str = "notebooks/reports/pipeline_analysis.png"):
        """Cria análise usando os filtros do pipeline."""
        plt.figure(figsize=(16, 10))
        
        # Aplica filtros do pipeline
        pipeline = create_comprehensive_social_pipeline()
        filtered_data = list(pipeline.process(self.comments))
        
        # Estatísticas antes e depois dos filtros
        original_count = len(self.comments)
        filtered_count = len(filtered_data)
        
        # Gráfico de comparação
        plt.subplot(2, 3, 1)
        categories = ['Original', 'Após Filtros']
        counts = [original_count, filtered_count]
        colors = ['lightblue', 'lightgreen']
        plt.bar(categories, counts, color=colors)
        plt.title('Comentários: Antes vs Após Filtros', fontweight='bold')
        plt.ylabel('Número de Comentários')
        for i, v in enumerate(counts):
            plt.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold')
        
        # Análise de sentimentos após filtros
        if filtered_data:
            filtered_df = pd.DataFrame(filtered_data)
            sentiment_after = filtered_df['sentiment'].value_counts()
            
            plt.subplot(2, 3, 2)
            sentiment_after.plot(kind='pie', autopct='%1.1f%%', startangle=90, 
                               colors=['#2E8B57', '#DC143C'])
            plt.title('Sentimentos Após Filtros', fontweight='bold')
            plt.ylabel('')
        
        # Likes após filtros
        if filtered_data:
            plt.subplot(2, 3, 3)
            plt.hist(filtered_df['likes'], bins=20, alpha=0.7, color='orange', edgecolor='black')
            plt.title('Distribuição de Likes Após Filtros', fontweight='bold')
            plt.xlabel('Número de Likes')
            plt.ylabel('Frequência')
            plt.grid(True, alpha=0.3)
        
        # Análise de países após filtros
        if filtered_data:
            plt.subplot(2, 3, 4)
            country_after = filtered_df['country'].value_counts().head(8)
            country_after.plot(kind='bar', color='lightcoral')
            plt.title('Países Após Filtros (Top 8)', fontweight='bold')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Número de Comentários')
        
        # Comprimento do texto após filtros
        if filtered_data:
            plt.subplot(2, 3, 5)
            text_length_after = filtered_df['text'].str.len()
            plt.hist(text_length_after, bins=20, alpha=0.7, color='purple', edgecolor='black')
            plt.title('Comprimento do Texto Após Filtros', fontweight='bold')
            plt.xlabel('Comprimento (caracteres)')
            plt.ylabel('Frequência')
            plt.grid(True, alpha=0.3)
        
        # Resumo estatístico
        plt.subplot(2, 3, 6)
        plt.axis('off')
        summary_text = f"""
        RESUMO DA ANÁLISE:
        
        📊 Comentários originais: {original_count:,}
        🔍 Comentários após filtros: {filtered_count:,}
        📉 Redução: {((original_count - filtered_count) / original_count * 100):.1f}%
        
        ✅ Filtros aplicados:
        • Limpeza de texto
        • Detecção de spam
        • Normalização
        • Análise de engajamento
        """
        plt.text(0.1, 0.5, summary_text, fontsize=10, fontfamily='monospace',
                verticalalignment='center', transform=plt.gca().transAxes)
        
        plt.tight_layout()
        
        # Salva o gráfico
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"📊 Análise do pipeline salva: {save_path}")
    
    def generate_all_reports(self):
        """Gera todos os relatórios visuais."""
        print("🚀 Gerando relatórios visuais...")
        
        # Cria diretório de relatórios
        Path("notebooks/reports").mkdir(parents=True, exist_ok=True)
        
        # Gera estatísticas
        self.print_statistics()
        
        # Gera gráficos
        self.create_sentiment_chart()
        self.create_likes_distribution()
        self.create_country_analysis()
        self.create_text_analysis()
        self.create_pipeline_analysis()
        
        print("\n🎉 Todos os relatórios foram gerados!")
        print("📁 Localização: notebooks/reports/")
        print("💡 Abra as imagens para visualizar os gráficos")
    
    def generate_html_report(self, save_path: str = "notebooks/reports/analysis_report.html"):
        """Gera um relatório HTML completo."""
        stats = self.basic_statistics()
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Relatório de Análise - Comentários Sociais</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 20px; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 30px 0; }}
                .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .stat-value {{ font-size: 2em; font-weight: bold; margin: 10px 0; }}
                .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
                .chart-section {{ margin: 40px 0; text-align: center; }}
                .chart-section img {{ max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                .summary {{ background: #ecf0f1; padding: 20px; border-radius: 8px; margin: 30px 0; }}
                .footer {{ text-align: center; margin-top: 40px; color: #7f8c8d; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Relatório de Análise - Comentários Sociais</h1>
                
                <div class="summary">
                    <h2>📋 Resumo Executivo</h2>
                    <p>Este relatório apresenta uma análise completa dos comentários simulados em redes sociais, 
                    demonstrando o uso da arquitetura Pipes and Filters para processamento e análise de dados.</p>
                </div>
                
                <h2>📈 Estatísticas Principais</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{stats['total_comments']:,}</div>
                        <div class="stat-label">Total de Comentários</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['positive_comments']:,}</div>
                        <div class="stat-label">Comentários Positivos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['negative_comments']:,}</div>
                        <div class="stat-label">Comentários Negativos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['avg_likes']:.1f}</div>
                        <div class="stat-label">Média de Likes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['unique_countries']}</div>
                        <div class="stat-label">Países Únicos</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{stats['unique_users']}</div>
                        <div class="stat-label">Usuários Únicos</div>
                    </div>
                </div>
                
                <h2>📊 Visualizações</h2>
                
                <div class="chart-section">
                    <h3>Distribuição de Sentimentos</h3>
                    <img src="sentiment_distribution.png" alt="Distribuição de Sentimentos">
                </div>
                
                <div class="chart-section">
                    <h3>Análise de Likes</h3>
                    <img src="likes_distribution.png" alt="Distribuição de Likes">
                </div>
                
                <div class="chart-section">
                    <h3>Análise por País</h3>
                    <img src="country_analysis.png" alt="Análise por País">
                </div>
                
                <div class="chart-section">
                    <h3>Análise de Texto</h3>
                    <img src="text_analysis.png" alt="Análise de Texto">
                </div>
                
                <div class="chart-section">
                    <h3>Análise do Pipeline</h3>
                    <img src="pipeline_analysis.png" alt="Análise do Pipeline">
                </div>
                
                <div class="footer">
                    <p>Relatório gerado automaticamente pelo Motor de Análise Social</p>
                    <p>Arquitetura Pipes and Filters - Projeto Educacional</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Salva o relatório HTML
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"🌐 Relatório HTML gerado: {save_path}")
        return save_path


def main():
    """Função principal."""
    print("🚀 Motor de Análise Social - Pipes and Filters")
    print("=" * 50)
    
    # Verifica se os dados existem
    if not os.path.exists("data/comments_dataset.json"):
        print("❌ Dataset não encontrado!")
        print("💡 Execute 'make generate-data' primeiro")
        return
    
    # Cria o motor de análise
    engine = SocialAnalysisEngine()
    
    # Gera todos os relatórios
    engine.generate_all_reports()
    
    # Gera relatório HTML
    html_path = engine.generate_html_report()
    
    print(f"\n🎉 Análise completa finalizada!")
    print(f"📊 Gráficos salvos em: notebooks/reports/")
    print(f"🌐 Relatório HTML: {html_path}")
    print("\n💡 Para visualizar os gráficos:")
    print("   - Abra as imagens PNG na pasta notebooks/reports/")
    print("   - Abra o arquivo HTML no seu navegador")


if __name__ == "__main__":
    main()
