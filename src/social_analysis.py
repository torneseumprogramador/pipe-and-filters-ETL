"""
Análise de comentários em redes sociais usando a arquitetura Pipes and Filters.
"""

import json
import sys
import os
from typing import List, Dict, Any

# Adiciona o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(__file__))

from pipes.social_pipeline import (
    create_basic_social_pipeline,
    create_sentiment_analysis_pipeline,
    create_spam_detection_pipeline,
    create_engagement_analysis_pipeline,
    create_multilingual_pipeline,
    create_geographic_pipeline,
    create_comprehensive_social_pipeline
)


def load_comments_from_json(filename: str) -> List[Dict[str, Any]]:
    """
    Carrega comentários de um arquivo JSON.
    
    Args:
        filename: Nome do arquivo JSON
        
    Returns:
        Lista de comentários
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo {filename} não encontrado!")
        print("💡 Execute primeiro: python data/generator.py")
        return []
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar o arquivo {filename}")
        return []


def print_comment_summary(comments: List[Dict[str, Any]], title: str):
    """Imprime um resumo dos comentários processados."""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    
    if not comments:
        print("❌ Nenhum comentário encontrado.")
        return
    
    print(f"📝 Total de comentários: {len(comments)}")
    
    # Estatísticas básicas
    if comments and 'sentiment' in comments[0]:
        positive_count = sum(1 for c in comments if c.get('sentiment') == 'positive')
        negative_count = sum(1 for c in comments if c.get('sentiment') == 'negative')
        print(f"😊 Positivos: {positive_count}")
        print(f"😞 Negativos: {negative_count}")
    
    # Estatísticas de likes
    if comments and 'likes' in comments[0]:
        likes = [c.get('likes', 0) for c in comments]
        avg_likes = sum(likes) / len(likes)
        max_likes = max(likes)
        print(f"👍 Média de likes: {avg_likes:.1f}")
        print(f"🔥 Máximo de likes: {max_likes}")
    
    # Estatísticas de países
    if comments and 'country' in comments[0]:
        countries = {}
        for comment in comments:
            country = comment.get('country', 'Desconhecido')
            countries[country] = countries.get(country, 0) + 1
        
        print(f"🌍 Países: {len(countries)}")
        top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:3]
        print("   Top 3 países:")
        for country, count in top_countries:
            print(f"     {country}: {count}")
    
    # Mostra alguns exemplos
    print(f"\n📋 Exemplos de comentários:")
    for i, comment in enumerate(comments[:3]):
        print(f"   {i+1}. {comment.get('user', 'N/A')} ({comment.get('country', 'N/A')}):")
        print(f"      \"{comment.get('text', 'N/A')[:80]}{'...' if len(comment.get('text', '')) > 80 else ''}\"")
        print(f"      Likes: {comment.get('likes', 0)}, Sentimento: {comment.get('sentiment', 'N/A')}")


def demonstrate_basic_pipeline(comments: List[Dict[str, Any]]):
    """Demonstra o pipeline básico de limpeza."""
    print("\n🚀 Demonstração: Pipeline Básico de Limpeza")
    print("=" * 60)
    
    pipeline = create_basic_social_pipeline()
    result = pipeline.execute(iter(comments))
    
    print_comment_summary(result, "Pipeline Básico - Limpeza e Normalização")
    
    # Mostra exemplo de comentário processado
    if result:
        print(f"\n🔍 Exemplo de comentário processado:")
        comment = result[0]
        print(f"   Texto original: {comment.get('text', 'N/A')}")
        if 'user_normalized' in comment:
            print(f"   Usuário normalizado: {comment['user_normalized']}")
        if 'text_metrics' in comment:
            metrics = comment['text_metrics']
            print(f"   Métricas: {metrics['word_count']} palavras, {metrics['char_count']} caracteres")


def demonstrate_sentiment_analysis(comments: List[Dict[str, Any]]):
    """Demonstra a análise de sentimentos."""
    print("\n🚀 Demonstração: Análise de Sentimentos")
    print("=" * 60)
    
    # Pipeline para comentários positivos
    positive_pipeline = create_sentiment_analysis_pipeline().add_sentiment_filter("positive")
    positive_comments = positive_pipeline.execute(iter(comments))
    
    # Pipeline para comentários negativos
    negative_pipeline = create_sentiment_analysis_pipeline().add_sentiment_filter("negative")
    negative_comments = negative_pipeline.execute(iter(comments))
    
    print_comment_summary(positive_comments, "Comentários Positivos")
    print_comment_summary(negative_comments, "Comentários Negativos")
    
    # Análise de engajamento por sentimento
    if positive_comments and negative_comments:
        pos_avg_score = sum(c.get('engagement_score', 0) for c in positive_comments) / len(positive_comments)
        neg_avg_score = sum(c.get('engagement_score', 0) for c in negative_comments) / len(negative_comments)
        
        print(f"\n📈 Análise de Engajamento:")
        print(f"   Score médio (positivos): {pos_avg_score:.2f}")
        print(f"   Score médio (negativos): {neg_avg_score:.2f}")
        print(f"   Diferença: {pos_avg_score - neg_avg_score:.2f}")


def demonstrate_spam_detection(comments: List[Dict[str, Any]]):
    """Demonstra a detecção de spam."""
    print("\n🚀 Demonstração: Detecção de Spam")
    print("=" * 60)
    
    pipeline = create_spam_detection_pipeline()
    result = pipeline.execute(iter(comments))
    
    # Separa comentários normais e spam
    normal_comments = [c for c in result if not c.get('is_spam', False)]
    spam_comments = [c for c in result if c.get('is_spam', False)]
    
    print_comment_summary(normal_comments, "Comentários Normais")
    print_comment_summary(spam_comments, "Comentários Detectados como Spam")
    
    # Mostra razões do spam
    if spam_comments:
        print(f"\n🚨 Razões para detecção de spam:")
        spam_reasons = {}
        for comment in spam_comments:
            for reason in comment.get('spam_reason', []):
                spam_reasons[reason] = spam_reasons.get(reason, 0) + 1
        
        for reason, count in spam_reasons.items():
            print(f"   {reason}: {count} comentários")


def demonstrate_engagement_analysis(comments: List[Dict[str, Any]]):
    """Demonstra a análise de engajamento."""
    print("\n🚀 Demonstração: Análise de Engajamento")
    print("=" * 60)
    
    pipeline = create_engagement_analysis_pipeline()
    result = pipeline.execute(iter(comments))
    
    print_comment_summary(result, "Análise de Engajamento (likes >= 10)")
    
    # Top comentários por engajamento
    if result:
        top_engagement = sorted(result, key=lambda x: x.get('engagement_score', 0), reverse=True)[:5]
        
        print(f"\n🏆 Top 5 comentários por engajamento:")
        for i, comment in enumerate(top_engagement):
            score = comment.get('engagement_score', 0)
            likes = comment.get('likes', 0)
            sentiment = comment.get('sentiment', 'N/A')
            print(f"   {i+1}. Score: {score:.2f} | Likes: {likes} | Sentimento: {sentiment}")
            print(f"      \"{comment.get('text', 'N/A')[:60]}{'...' if len(comment.get('text', '')) > 60 else ''}\"")


def demonstrate_multilingual_analysis(comments: List[Dict[str, Any]]):
    """Demonstra a análise multilingue."""
    print("\n🚀 Demonstração: Análise Multilingue")
    print("=" * 60)
    
    languages = ["portuguese", "english", "spanish", "french", "german"]
    
    for language in languages:
        pipeline = create_multilingual_pipeline([language])
        result = pipeline.execute(iter(comments))
        
        if result:
            print(f"\n🌐 {language.capitalize()}: {len(result)} comentários")
            # Mostra exemplo
            example = result[0]
            print(f"   Exemplo: \"{example.get('text', 'N/A')[:50]}{'...' if len(example.get('text', '')) > 50 else ''}\"")


def demonstrate_geographic_analysis(comments: List[Dict[str, Any]]):
    """Demonstra a análise geográfica."""
    print("\n🚀 Demonstração: Análise Geográfica")
    print("=" * 60)
    
    # Análise para países específicos
    target_countries = ["Brasil", "Estados Unidos", "França"]
    
    for country in target_countries:
        pipeline = create_geographic_pipeline([country])
        result = pipeline.execute(iter(comments))
        
        if result:
            print(f"\n🌍 {country}: {len(result)} comentários")
            # Estatísticas do país
            positive_count = sum(1 for c in result if c.get('sentiment') == 'positive')
            avg_likes = sum(c.get('likes', 0) for c in result) / len(result)
            print(f"   Positivos: {positive_count} | Média de likes: {avg_likes:.1f}")


def demonstrate_comprehensive_pipeline(comments: List[Dict[str, Any]]):
    """Demonstra o pipeline abrangente."""
    print("\n🚀 Demonstração: Pipeline Abrangente")
    print("=" * 60)
    
    pipeline = create_comprehensive_social_pipeline()
    result = pipeline.execute(iter(comments))
    
    print_comment_summary(result, "Pipeline Abrangente - Todos os Filtros")
    
    # Estatísticas avançadas
    if result:
        print(f"\n📊 Estatísticas Avançadas:")
        
        # Engajamento por país
        engagement_by_country = {}
        for comment in result:
            country = comment.get('country', 'Desconhecido')
            score = comment.get('engagement_score', 0)
            if country not in engagement_by_country:
                engagement_by_country[country] = []
            engagement_by_country[country].append(score)
        
        print(f"   Engajamento médio por país:")
        for country, scores in sorted(engagement_by_country.items()):
            avg_score = sum(scores) / len(scores)
            print(f"     {country}: {avg_score:.2f}")
        
        # Spam por idioma
        spam_by_language = {}
        for comment in result:
            if comment.get('is_spam', False):
                # Detecta idioma baseado no texto
                text = comment.get('text', '').lower()
                if any(word in text for word in ['não', 'muito', 'bom', 'ruim']):
                    lang = 'portuguese'
                elif any(word in text for word in ['the', 'and', 'very', 'good', 'bad']):
                    lang = 'english'
                elif any(word in text for word in ['el', 'la', 'muy', 'bueno', 'malo']):
                    lang = 'spanish'
                elif any(word in text for word in ['le', 'la', 'très', 'bon', 'mauvais']):
                    lang = 'french'
                elif any(word in text for word in ['der', 'die', 'sehr', 'gut', 'schlecht']):
                    lang = 'german'
                else:
                    lang = 'unknown'
                
                spam_by_language[lang] = spam_by_language.get(lang, 0) + 1
        
        if spam_by_language:
            print(f"   Spam por idioma:")
            for lang, count in spam_by_language.items():
                print(f"     {lang}: {count}")


def main():
    """Função principal de demonstração."""
    print("🚀 Análise de Comentários em Redes Sociais")
    print("📊 Usando Arquitetura Pipes and Filters")
    print("=" * 60)
    
    # Carrega comentários
    data_file = "../data/comments_dataset.json"
    comments = load_comments_from_json(data_file)
    
    if not comments:
        return
    
    print(f"✅ Carregados {len(comments)} comentários de {data_file}")
    
    # Demonstrações
    demonstrate_basic_pipeline(comments)
    demonstrate_sentiment_analysis(comments)
    demonstrate_spam_detection(comments)
    demonstrate_engagement_analysis(comments)
    demonstrate_multilingual_analysis(comments)
    demonstrate_geographic_analysis(comments)
    demonstrate_comprehensive_pipeline(comments)
    
    print(f"\n🎉 Análise completa finalizada!")
    print(f"📊 Total de comentários processados: {len(comments)}")
    print(f"🔍 Pipeline executado com sucesso usando arquitetura Pipes and Filters")


if __name__ == "__main__":
    main()
