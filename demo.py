#!/usr/bin/env python3
"""
Demonstração completa do projeto Pipes and Filters para análise de comentários sociais.
"""

import json
import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def main():
    """Demonstração principal do projeto."""
    print("🚀 PROJETO PIPE AND FILTERS - ANÁLISE DE COMENTÁRIOS SOCIAIS")
    print("=" * 80)
    print()
    
    # Verifica se o dataset existe
    dataset_path = Path("data/comments_dataset.json")
    if not dataset_path.exists():
        print("❌ Dataset não encontrado!")
        print("💡 Execute primeiro: python data/generator.py -n 100")
        return
    
    # Carrega comentários
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            comments = json.load(f)
        print(f"✅ Dataset carregado: {len(comments)} comentários")
    except Exception as e:
        print(f"❌ Erro ao carregar dataset: {e}")
        return
    
    print()
    print("🔍 ANÁLISE COMPLETA USANDO PIPES AND FILTERS")
    print("=" * 80)
    
    # Importa os pipelines
    try:
        from pipes.social_pipeline import (
            create_basic_social_pipeline,
            create_sentiment_analysis_pipeline,
            create_spam_detection_pipeline,
            create_engagement_analysis_pipeline,
            create_multilingual_pipeline,
            create_geographic_pipeline,
            create_comprehensive_social_pipeline
        )
        print("✅ Pipelines importados com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar pipelines: {e}")
        return
    
    print()
    
    # 1. Pipeline Básico
    print("1️⃣ PIPELINE BÁSICO - LIMPEZA E NORMALIZAÇÃO")
    print("-" * 50)
    
    basic_pipeline = create_basic_social_pipeline()
    basic_result = basic_pipeline.execute(iter(comments))
    
    print(f"📊 Comentários processados: {len(basic_result)}")
    if basic_result:
        sample = basic_result[0]
        print(f"🔍 Exemplo de comentário processado:")
        print(f"   Usuário: {sample.get('user', 'N/A')}")
        print(f"   Usuário normalizado: {sample.get('user_normalized', 'N/A')}")
        if 'text_metrics' in sample:
            metrics = sample['text_metrics']
            print(f"   Métricas: {metrics['word_count']} palavras, {metrics['char_count']} caracteres")
    
    print()
    
    # 2. Análise de Sentimentos
    print("2️⃣ ANÁLISE DE SENTIMENTOS")
    print("-" * 50)
    
    positive_pipeline = create_sentiment_analysis_pipeline().add_sentiment_filter("positive")
    negative_pipeline = create_sentiment_analysis_pipeline().add_sentiment_filter("negative")
    
    positive_comments = positive_pipeline.execute(iter(comments))
    negative_comments = negative_pipeline.execute(iter(comments))
    
    print(f"😊 Comentários positivos: {len(positive_comments)}")
    print(f"😞 Comentários negativos: {len(negative_comments)}")
    
    if positive_comments and negative_comments:
        pos_avg_score = sum(c.get('engagement_score', 0) for c in positive_comments) / len(positive_comments)
        neg_avg_score = sum(c.get('engagement_score', 0) for c in negative_comments) / len(negative_comments)
        print(f"📈 Score médio (positivos): {pos_avg_score:.2f}")
        print(f"📉 Score médio (negativos): {neg_avg_score:.2f}")
    
    print()
    
    # 3. Detecção de Spam
    print("3️⃣ DETECÇÃO DE SPAM")
    print("-" * 50)
    
    spam_pipeline = create_spam_detection_pipeline()
    spam_result = spam_pipeline.execute(iter(comments))
    
    normal_comments = [c for c in spam_result if not c.get('is_spam', False)]
    spam_comments = [c for c in spam_result if c.get('is_spam', False)]
    
    print(f"✅ Comentários normais: {len(normal_comments)}")
    print(f"🚨 Comentários spam: {len(spam_comments)}")
    
    if spam_comments:
        print("🚨 Razões para detecção de spam:")
        spam_reasons = {}
        for comment in spam_comments:
            for reason in comment.get('spam_reason', []):
                spam_reasons[reason] = spam_reasons.get(reason, 0) + 1
        
        for reason, count in spam_reasons.items():
            print(f"   {reason}: {count} comentários")
    
    print()
    
    # 4. Análise de Engajamento
    print("4️⃣ ANÁLISE DE ENGAJAMENTO")
    print("-" * 50)
    
    engagement_pipeline = create_engagement_analysis_pipeline()
    engagement_result = engagement_pipeline.execute(iter(comments))
    
    print(f"📊 Comentários com engajamento (likes >= 10): {len(engagement_result)}")
    
    if engagement_result:
        top_engagement = sorted(engagement_result, key=lambda x: x.get('engagement_score', 0), reverse=True)[:3]
        print("🏆 Top 3 comentários por engajamento:")
        for i, comment in enumerate(top_engagement):
            score = comment.get('engagement_score', 0)
            likes = comment.get('likes', 0)
            sentiment = comment.get('sentiment', 'N/A')
            print(f"   {i+1}. Score: {score:.2f} | Likes: {likes} | Sentimento: {sentiment}")
    
    print()
    
    # 5. Análise Multilingue
    print("5️⃣ ANÁLISE MULTILINGUE")
    print("-" * 50)
    
    languages = ["portuguese", "english", "spanish", "french", "german"]
    
    for language in languages:
        lang_pipeline = create_multilingual_pipeline([language])
        lang_result = lang_pipeline.execute(iter(comments))
        
        if lang_result:
            print(f"🌐 {language.capitalize()}: {len(lang_result)} comentários")
    
    print()
    
    # 6. Análise Geográfica
    print("6️⃣ ANÁLISE GEOGRÁFICA")
    print("-" * 50)
    
    target_countries = ["Brasil", "Estados Unidos", "França", "Alemanha"]
    
    for country in target_countries:
        geo_pipeline = create_geographic_pipeline([country])
        geo_result = geo_pipeline.execute(iter(comments))
        
        if geo_result:
            positive_count = sum(1 for c in geo_result if c.get('sentiment') == 'positive')
            avg_likes = sum(c.get('likes', 0) for c in geo_result) / len(geo_result)
            print(f"🌍 {country}: {len(geo_result)} comentários | Positivos: {positive_count} | Média likes: {avg_likes:.1f}")
    
    print()
    
    # 7. Pipeline Abrangente
    print("7️⃣ PIPELINE ABRANGENTE - TODOS OS FILTROS")
    print("-" * 50)
    
    comprehensive_pipeline = create_comprehensive_social_pipeline()
    comprehensive_result = comprehensive_pipeline.execute(iter(comments))
    
    print(f"📊 Comentários processados pelo pipeline completo: {len(comprehensive_result)}")
    
    if comprehensive_result:
        # Estatísticas avançadas
        countries = {}
        for comment in comprehensive_result:
            country = comment.get('country', 'Desconhecido')
            countries[country] = countries.get(country, 0) + 1
        
        print(f"🌍 Países representados: {len(countries)}")
        top_countries = sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]
        print("   Top 5 países:")
        for country, count in top_countries:
            print(f"     {country}: {count} comentários")
    
    print()
    print("🎉 DEMONSTRAÇÃO COMPLETA FINALIZADA!")
    print("=" * 80)
    print("✅ Todos os pipelines executados com sucesso")
    print("✅ Arquitetura Pipes and Filters funcionando perfeitamente")
    print("✅ Análise de comentários sociais completa")
    print()
    print("📚 Para mais detalhes, consulte:")
    print("   - README.md: Documentação completa")
    print("   - QUICKSTART.md: Guia de início rápido")
    print("   - src/social_analysis.py: Análise detalhada")
    print("   - run.py: Script interativo")


if __name__ == "__main__":
    main()
