"""
Testes unitários para os filtros de análise de comentários sociais.
"""

import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from filters.social_filters import (
    clean_text,
    filter_by_sentiment,
    filter_by_language,
    filter_by_country,
    filter_by_likes_threshold,
    add_engagement_score,
    detect_spam,
    normalize_user_names,
    add_text_metrics
)


class TestSocialFilters(unittest.TestCase):
    """Testa os filtros de análise de comentários sociais."""
    
    def setUp(self):
        """Configura dados de teste."""
        self.sample_comments = [
            {
                "post_id": "post_0001",
                "user": "João Silva",
                "country": "Brasil",
                "state": "São Paulo",
                "likes": 100,
                "text": "Excelente post! Muito informativo e útil.",
                "sentiment": "positive"
            },
            {
                "post_id": "post_0002",
                "user": "John Smith",
                "country": "Estados Unidos",
                "state": "Califórnia",
                "likes": 50,
                "text": "Very good content, thanks for sharing!",
                "sentiment": "positive"
            },
            {
                "post_id": "post_0003",
                "user": "Maria García",
                "country": "Espanha",
                "state": "Madrid",
                "likes": 25,
                "text": "¡Me encantó el contenido!",
                "sentiment": "positive"
            },
            {
                "post_id": "post_0004",
                "user": "Pierre Dubois",
                "country": "França",
                "state": "Paris",
                "likes": 75,
                "text": "Très bon travail, continuez comme ça!",
                "sentiment": "positive"
            },
            {
                "post_id": "post_0005",
                "user": "Hans Müller",
                "country": "Alemanha",
                "state": "Berlim",
                "likes": 30,
                "text": "Sehr gut gemacht!",
                "sentiment": "positive"
            }
        ]
    
    def test_clean_text(self):
        """Testa a limpeza de texto."""
        # Comentário com caracteres especiais
        dirty_comment = {
            "post_id": "post_0001",
            "user": "Test User",
            "text": "Excelente post!!! Muito informativo... e útil."
        }
        
        result = list(clean_text(iter([dirty_comment])))
        
        self.assertEqual(len(result), 1)
        self.assertIn("text", result[0])
        # Verifica se caracteres especiais foram removidos
        self.assertNotIn("!!!", result[0]["text"])
        self.assertNotIn("...", result[0]["text"])
    
    def test_filter_by_sentiment(self):
        """Testa filtro por sentimento."""
        # Filtra comentários positivos
        positive_comments = list(filter_by_sentiment(iter(self.sample_comments), "positive"))
        
        self.assertEqual(len(positive_comments), 5)
        for comment in positive_comments:
            self.assertEqual(comment["sentiment"], "positive")
        
        # Filtra comentários negativos (não deve encontrar nenhum)
        negative_comments = list(filter_by_sentiment(iter(self.sample_comments), "negative"))
        self.assertEqual(len(negative_comments), 0)
    
    def test_filter_by_language(self):
        """Testa filtro por idioma."""
        # Filtra comentários em português
        portuguese_comments = list(filter_by_language(iter(self.sample_comments), "portuguese"))
        
        self.assertEqual(len(portuguese_comments), 1)
        self.assertIn("excelente", portuguese_comments[0]["text"].lower())
        
        # Filtra comentários em inglês
        english_comments = list(filter_by_language(iter(self.sample_comments), "english"))
        
        self.assertEqual(len(english_comments), 1)
        self.assertIn("very", english_comments[0]["text"].lower())
    
    def test_filter_by_country(self):
        """Testa filtro por país."""
        target_countries = ["Brasil", "Estados Unidos"]
        
        result = list(filter_by_country(iter(self.sample_comments), target_countries))
        
        self.assertEqual(len(result), 2)
        for comment in result:
            self.assertIn(comment["country"], target_countries)
    
    def test_filter_by_likes_threshold(self):
        """Testa filtro por faixa de likes."""
        # Filtra comentários com pelo menos 50 likes
        result = list(filter_by_likes_threshold(iter(self.sample_comments), min_likes=50))
        
        self.assertEqual(len(result), 3)  # 100, 75, 50
        for comment in result:
            self.assertGreaterEqual(comment["likes"], 50)
        
        # Filtra comentários entre 20 e 60 likes
        result = list(filter_by_likes_threshold(iter(self.sample_comments), min_likes=20, max_likes=60))
        
        self.assertEqual(len(result), 3)  # 50, 30, 25
        for comment in result:
            self.assertGreaterEqual(comment["likes"], 20)
            self.assertLessEqual(comment["likes"], 60)
    
    def test_add_engagement_score(self):
        """Testa adição de score de engajamento."""
        result = list(add_engagement_score(iter(self.sample_comments)))
        
        self.assertEqual(len(result), 5)
        for comment in result:
            self.assertIn("engagement_score", comment)
            self.assertIsInstance(comment["engagement_score"], (int, float))
            
            # Verifica se o score é calculado corretamente
            expected_score = comment["likes"] / 10 * 1.2  # positivo
            self.assertAlmostEqual(comment["engagement_score"], expected_score, places=1)
    
    def test_detect_spam(self):
        """Testa detecção de spam."""
        # Comentário normal
        normal_comment = {
            "post_id": "post_0001",
            "user": "Test User",
            "text": "Excelente post muito informativo"
        }
        
        # Comentário com caracteres repetidos (spam)
        spam_comment = {
            "post_id": "post_0002",
            "user": "Spam User",
            "text": "Excelente post!!!!! muito informativo!!!!!"
        }
        
        test_data = [normal_comment, spam_comment]
        result = list(detect_spam(iter(test_data)))
        
        self.assertEqual(len(result), 2)
        
        # Verifica se o spam foi detectado
        spam_detected = False
        for comment in result:
            if comment.get("is_spam"):
                spam_detected = True
                self.assertIn("spam_reason", comment)
                self.assertIn("repeated_chars", comment["spam_reason"])
        
        self.assertTrue(spam_detected)
    
    def test_normalize_user_names(self):
        """Testa normalização de nomes de usuário."""
        result = list(normalize_user_names(iter(self.sample_comments)))
        
        self.assertEqual(len(result), 5)
        for comment in result:
            self.assertIn("user_normalized", comment)
            
            # Verifica se o nome foi normalizado corretamente
            original = comment["user"]
            normalized = comment["user_normalized"]
            
            # Primeira letra de cada palavra deve ser maiúscula
            words = normalized.split()
            for word in words:
                self.assertTrue(word[0].isupper())
                self.assertTrue(word[1:].islower())
    
    def test_add_text_metrics(self):
        """Testa adição de métricas de texto."""
        result = list(add_text_metrics(iter(self.sample_comments)))
        
        self.assertEqual(len(result), 5)
        for comment in result:
            self.assertIn("text_metrics", comment)
            metrics = comment["text_metrics"]
            
            # Verifica se todas as métricas estão presentes
            required_metrics = ["char_count", "word_count", "avg_word_length", "punctuation_count", "uppercase_count"]
            for metric in required_metrics:
                self.assertIn(metric, metrics)
                self.assertIsInstance(metrics[metric], (int, float))
            
            # Verifica se as métricas fazem sentido
            text = comment["text"]
            self.assertEqual(metrics["char_count"], len(text))
            self.assertEqual(metrics["word_count"], len(text.split()))
    
    def test_empty_input(self):
        """Testa comportamento com entrada vazia."""
        empty_data = []
        
        # Todos os filtros devem retornar iteradores vazios
        self.assertEqual(list(clean_text(iter(empty_data))), [])
        self.assertEqual(list(filter_by_sentiment(iter(empty_data))), [])
        self.assertEqual(list(filter_by_language(iter(empty_data))), [])
        self.assertEqual(list(filter_by_country(iter(empty_data), [])), [])
        self.assertEqual(list(filter_by_likes_threshold(iter(empty_data))), [])
        self.assertEqual(list(add_engagement_score(iter(empty_data))), [])
        self.assertEqual(list(detect_spam(iter(empty_data))), [])
        self.assertEqual(list(normalize_user_names(iter(empty_data))), [])
        self.assertEqual(list(add_text_metrics(iter(empty_data))), [])
    
    def test_malformed_data(self):
        """Testa comportamento com dados malformados."""
        malformed_data = [
            {"invalid": "data"},
            {"text": "valid text", "likes": "not a number"},
            None,
            "string instead of dict"
        ]
        
        # Filtros devem lidar graciosamente com dados malformados
        result = list(clean_text(iter(malformed_data)))
        self.assertEqual(len(result), 4)  # Todos os itens devem ser retornados
        
        result = list(filter_by_sentiment(iter(malformed_data)))
        self.assertEqual(len(result), 0)  # Nenhum tem sentimento válido


if __name__ == '__main__':
    unittest.main()
