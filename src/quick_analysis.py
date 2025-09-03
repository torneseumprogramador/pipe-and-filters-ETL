#!/usr/bin/env python3
"""
Análise rápida dos comentários sociais.
Script leve para estatísticas básicas sem dependências pesadas.
"""

import json
import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.dirname(__file__))


def load_data(data_path: str = "data/comments_dataset.json"):
    """Carrega os dados dos comentários."""
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {data_path}")
        print("💡 Execute 'make generate-data' primeiro")
        return None


def quick_analysis(comments):
    """Executa análise rápida dos comentários."""
    if not comments:
        return
    
    total = len(comments)
    positive = sum(1 for c in comments if c['sentiment'] == 'positive')
    negative = total - positive
    
    # Estatísticas de likes
    likes = [c['likes'] for c in comments]
    avg_likes = sum(likes) / len(likes)
    max_likes = max(likes)
    min_likes = min(likes)
    
    # Países únicos
    countries = set(c['country'] for c in comments)
    users = set(c['user'] for c in comments)
    
    # Comprimento médio do texto
    text_lengths = [len(c['text']) for c in comments]
    avg_text_length = sum(text_lengths) / len(text_lengths)
    
    print("\n" + "="*60)
    print("📊 ANÁLISE RÁPIDA - COMENTÁRIOS SOCIAIS")
    print("="*60)
    print(f"📝 Total de comentários: {total:,}")
    print(f"😊 Comentários positivos: {positive:,} ({positive/total*100:.1f}%)")
    print(f"😞 Comentários negativos: {negative:,} ({negative/total*100:.1f}%)")
    print(f"👍 Média de likes: {avg_likes:.1f}")
    print(f"🔥 Máximo de likes: {max_likes:,}")
    print(f"🌍 Países únicos: {len(countries)}")
    print(f"👥 Usuários únicos: {len(users)}")
    print(f"📏 Comprimento médio do texto: {avg_text_length:.1f} caracteres")
    
    # Top 5 países
    country_counts = {}
    for c in comments:
        country = c['country']
        country_counts[country] = country_counts.get(country, 0) + 1
    
    top_countries = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\n🌍 Top 5 países:")
    for i, (country, count) in enumerate(top_countries, 1):
        print(f"   {i}. {country}: {count:,} comentários")
    
    # Distribuição de likes por faixa
    like_ranges = {
        "0-10": 0,
        "11-50": 0,
        "51-100": 0,
        "100+": 0
    }
    
    for like in likes:
        if like <= 10:
            like_ranges["0-10"] += 1
        elif like <= 50:
            like_ranges["11-50"] += 1
        elif like <= 100:
            like_ranges["51-100"] += 1
        else:
            like_ranges["100+"] += 1
    
    print(f"\n👍 Distribuição de likes:")
    for range_name, count in like_ranges.items():
        percentage = (count / total) * 100
        print(f"   {range_name}: {count:,} ({percentage:.1f}%)")
    
    print("="*60)


def main():
    """Função principal."""
    print("⚡ Análise Rápida - Comentários Sociais")
    print("=" * 40)
    
    # Carrega dados
    comments = load_data()
    if comments:
        quick_analysis(comments)
        print("\n💡 Para análise completa com gráficos:")
        print("   make analysis-report")


if __name__ == "__main__":
    main()
