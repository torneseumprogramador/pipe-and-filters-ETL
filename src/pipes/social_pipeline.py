"""
Pipeline específico para análise de comentários em redes sociais.
"""

from typing import Iterator, Dict, Any, List
from .pipeline import Pipeline
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


class SocialCommentPipeline(Pipeline):
    """
    Pipeline especializado para análise de comentários em redes sociais.
    """
    
    def __init__(self):
        """Inicializa o pipeline de comentários sociais."""
        super().__init__()
    
    def add_text_cleaning(self) -> 'SocialCommentPipeline':
        """Adiciona filtros de limpeza de texto."""
        self.add_filter(clean_text)
        return self
    
    def add_sentiment_filter(self, sentiment: str = "positive") -> 'SocialCommentPipeline':
        """Adiciona filtro por sentimento."""
        def filter_sentiment(data):
            return filter_by_sentiment(data, sentiment)
        
        self.add_filter(filter_sentiment)
        return self
    
    def add_language_filter(self, language: str = "portuguese") -> 'SocialCommentPipeline':
        """Adiciona filtro por idioma."""
        def filter_language(data):
            return filter_by_language(data, language)
        
        self.add_filter(filter_language)
        return self
    
    def add_country_filter(self, countries: List[str]) -> 'SocialCommentPipeline':
        """Adiciona filtro por países."""
        def filter_country(data):
            return filter_by_country(data, countries)
        
        self.add_filter(filter_country)
        return self
    
    def add_likes_filter(self, min_likes: int = 0, max_likes: int = None) -> 'SocialCommentPipeline':
        """Adiciona filtro por faixa de likes."""
        def filter_likes(data):
            return filter_by_likes_threshold(data, min_likes, max_likes)
        
        self.add_filter(filter_likes)
        return self
    
    def add_engagement_analysis(self) -> 'SocialCommentPipeline':
        """Adiciona análise de engajamento."""
        self.add_filter(add_engagement_score)
        return self
    
    def add_spam_detection(self, max_repeated_chars: int = 3) -> 'SocialCommentPipeline':
        """Adiciona detecção de spam."""
        def detect_spam_filter(data):
            return detect_spam(data, max_repeated_chars)
        
        self.add_filter(detect_spam_filter)
        return self
    
    def add_user_normalization(self) -> 'SocialCommentPipeline':
        """Adiciona normalização de nomes de usuário."""
        self.add_filter(normalize_user_names)
        return self
    
    def add_text_metrics(self) -> 'SocialCommentPipeline':
        """Adiciona métricas de texto."""
        self.add_filter(add_text_metrics)
        return self


def create_basic_social_pipeline() -> SocialCommentPipeline:
    """
    Cria um pipeline básico para análise de comentários sociais.
    
    Returns:
        Pipeline configurado com filtros básicos
    """
    return (SocialCommentPipeline()
            .add_text_cleaning()
            .add_user_normalization()
            .add_text_metrics())


def create_sentiment_analysis_pipeline() -> SocialCommentPipeline:
    """
    Cria um pipeline para análise de sentimentos.
    
    Returns:
        Pipeline configurado para análise de sentimentos
    """
    return (SocialCommentPipeline()
            .add_text_cleaning()
            .add_engagement_analysis()
            .add_text_metrics())


def create_spam_detection_pipeline() -> SocialCommentPipeline:
    """
    Cria um pipeline para detecção de spam.
    
    Returns:
        Pipeline configurado para detecção de spam
    """
    return (SocialCommentPipeline()
            .add_text_cleaning()
            .add_spam_detection()
            .add_text_metrics())


def create_engagement_analysis_pipeline() -> SocialCommentPipeline:
    """
    Cria um pipeline para análise de engajamento.
    
    Returns:
        Pipeline configurado para análise de engajamento
    """
    return (SocialCommentPipeline()
            .add_text_cleaning()
            .add_engagement_analysis()
            .add_likes_filter(min_likes=10)
            .add_text_metrics())


def create_multilingual_pipeline(languages: List[str]) -> SocialCommentPipeline:
    """
    Cria um pipeline para análise multilingue.
    
    Args:
        languages: Lista de idiomas para incluir
        
    Returns:
        Pipeline configurado para análise multilingue
    """
    pipeline = SocialCommentPipeline().add_text_cleaning()
    
    # Adiciona filtros para cada idioma
    for language in languages:
        pipeline.add_language_filter(language)
    
    return pipeline.add_text_metrics()


def create_geographic_pipeline(countries: List[str]) -> SocialCommentPipeline:
    """
    Cria um pipeline para análise geográfica.
    
    Args:
        countries: Lista de países para incluir
        
    Returns:
        Pipeline configurado para análise geográfica
    """
    return (SocialCommentPipeline()
            .add_text_cleaning()
            .add_country_filter(countries)
            .add_user_normalization()
            .add_text_metrics())


def create_comprehensive_social_pipeline() -> SocialCommentPipeline:
    """
    Cria um pipeline abrangente para análise de comentários sociais.
    
    Returns:
        Pipeline configurado com todos os filtros principais
    """
    return (SocialCommentPipeline()
            .add_text_cleaning()
            .add_user_normalization()
            .add_engagement_analysis()
            .add_spam_detection()
            .add_text_metrics())
