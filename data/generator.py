#!/usr/bin/env python3
"""
Gerador de dados simulados de comentários em redes sociais.
Gera comentários realistas para serem processados em uma arquitetura Pipes and Filters.
"""

import json
import csv
import random
import argparse
from typing import List, Dict, Any
from pathlib import Path
from faker import Faker


class SocialCommentGenerator:
    """Gerador de comentários simulados para redes sociais."""
    
    def __init__(self):
        """Inicializa o gerador com dados pré-definidos."""
        self.faker = Faker(['pt_BR', 'en_US', 'es_ES', 'fr_FR', 'de_DE'])
        
        self.countries = [
            "Brasil", "Estados Unidos", "México", "Argentina", "Canadá",
            "Reino Unido", "França", "Alemanha", "Espanha", "Itália",
            "Portugal", "Japão", "Coreia do Sul", "China", "Índia",
            "Austrália", "Nova Zelândia", "África do Sul", "Egito", "Nigéria"
        ]
        
        self.states = {
            "Brasil": ["São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná"],
            "Estados Unidos": ["Califórnia", "Texas", "Nova York", "Flórida", "Illinois"],
            "México": ["Jalisco", "Veracruz", "Puebla", "Guanajuato", "Chihuahua"],
            "Argentina": ["Buenos Aires", "Córdoba", "Santa Fe", "Mendoza", "Tucumán"],
            "Canadá": ["Ontário", "Quebec", "Colúmbia Britânica", "Alberta", "Manitoba"],
            "Reino Unido": ["Inglaterra", "Escócia", "País de Gales", "Irlanda do Norte"],
            "França": ["Île-de-France", "Auvergne-Rhône-Alpes", "Nova Aquitânia", "Occitânia"],
            "Alemanha": ["Baviera", "Renânia do Norte-Vestfália", "Baden-Württemberg", "Baixa Saxônia"],
            "Espanha": ["Madrid", "Catalunha", "Andaluzia", "Valência", "Galiza"],
            "Itália": ["Lombardia", "Lácio", "Campânia", "Sicília", "Piemonte"],
            "Portugal": ["Lisboa", "Porto", "Braga", "Coimbra", "Faro"],
            "Japão": ["Tóquio", "Osaka", "Quioto", "Yokohama", "Nagoya"],
            "Coreia do Sul": ["Seul", "Busan", "Incheon", "Daegu", "Daejeon"],
            "China": ["Pequim", "Xangai", "Guangzhou", "Shenzhen", "Tianjin"],
            "Índia": ["Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Karnataka", "Gujarat"],
            "Austrália": ["Nova Gales do Sul", "Victoria", "Queensland", "Austrália Ocidental"],
            "Nova Zelândia": ["Auckland", "Wellington", "Canterbury", "Waikato", "Otago"],
            "África do Sul": ["Gauteng", "KwaZulu-Natal", "Cabo Ocidental", "Cabo Oriental"],
            "Egito": ["Cairo", "Alexandria", "Giza", "Shubra El Kheima", "Port Said"],
            "Nigéria": ["Lagos", "Kano", "Ibadan", "Kaduna", "Port Harcourt"]
        }
    
    def generate_comment(self, post_id: str) -> Dict[str, Any]:
        """Gera um comentário individual."""
        # Escolhe país e estado
        country = random.choice(self.countries)
        state = random.choice(self.states.get(country, ["Capital"]))
        
        # Gera nome usando Faker
        user = self.faker.name()
        
        # Determina sentimento (70% positivo, 30% negativo)
        is_positive = random.random() < 0.7
        
        # Gera texto do comentário
        text = self.faker.paragraph()
        sentiment = "positive" if is_positive else "negative"
        
        # Gera likes (0-200)
        likes = random.randint(0, 200)
        
        return {
            "post_id": post_id,
            "user": user,
            "country": country,
            "state": state,
            "likes": likes,
            "text": text,
            "sentiment": sentiment
        }
    
    def generate_dataset(self, num_comments: int = 100) -> List[Dict[str, Any]]:
        """Gera o dataset completo de comentários."""
        comments = []
        
        for i in range(num_comments):
            post_id = f"post_{i+1:04d}"
            comment = self.generate_comment(post_id)
            comments.append(comment)
        
        return comments
    
    def save_json(self, comments: List[Dict[str, Any]], filename: str):
        """Salva os comentários em formato JSON."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)
        print(f"✅ Dataset salvo em JSON: {filename}")
    
    def save_csv(self, comments: List[Dict[str, Any]], filename: str):
        """Salva os comentários em formato CSV."""
        if not comments:
            return
        
        fieldnames = comments[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(comments)
        print(f"✅ Dataset salvo em CSV: {filename}")
    
    def save_txt(self, comments: List[Dict[str, Any]], filename: str):
        """Salva os comentários em formato TXT (um por linha)."""
        with open(filename, 'w', encoding='utf-8') as f:
            for comment in comments:
                f.write(f"{comment['post_id']} | {comment['user']} | {comment['country']} | {comment['text']}\n")
        print(f"✅ Dataset salvo em TXT: {filename}")


def main():
    """Função principal do gerador."""
    parser = argparse.ArgumentParser(description="Gerador de comentários simulados para redes sociais")
    parser.add_argument("-n", "--num-comments", type=int, default=100, 
                       help="Número de comentários a gerar (padrão: 100)")
    parser.add_argument("-f", "--format", choices=["json", "csv", "txt"], default="json",
                       help="Formato de saída (padrão: json)")
    parser.add_argument("-o", "--output", type=str, default="comments_dataset",
                       help="Nome base do arquivo de saída (sem extensão)")
    
    args = parser.parse_args()
    
    print("🚀 Gerador de Comentários Simulados para Redes Sociais")
    print("=" * 60)
    print(f"📊 Gerando {args.num_comments} comentários...")
    print(f"📁 Formato: {args.format.upper()}")
    print(f"💾 Arquivo: {args.output}.{args.format}")
    print()
    
    # Cria o gerador
    generator = SocialCommentGenerator()
    
    # Gera o dataset
    comments = generator.generate_dataset(args.num_comments)
    
    # Estatísticas
    positive_count = sum(1 for c in comments if c['sentiment'] == 'positive')
    negative_count = len(comments) - positive_count
    
    print("📈 Estatísticas do Dataset:")
    print(f"   Total de comentários: {len(comments)}")
    print(f"   Comentários positivos: {positive_count} ({positive_count/len(comments)*100:.1f}%)")
    print(f"   Comentários negativos: {negative_count} ({negative_count/len(comments)*100:.1f}%)")
    print()
    
    # Salva no formato escolhido
    filename = f"{args.output}.{args.format}"
    
    if args.format == "json":
        generator.save_json(comments, filename)
    elif args.format == "csv":
        generator.save_csv(comments, filename)
    elif args.format == "txt":
        generator.save_txt(comments, filename)
    
    print(f"\n🎉 Dataset gerado com sucesso!")
    print(f"📁 Arquivo: {filename}")
    print(f"📊 Total de comentários: {len(comments)}")


if __name__ == "__main__":
    main()
