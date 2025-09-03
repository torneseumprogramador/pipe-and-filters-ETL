"""
Filtros para análise de comentários em redes sociais.
Cada filtro recebe um iterador e retorna um novo iterador com os dados processados.
"""

from typing import Iterator, Dict, Any, List
import re


def clean_text(data: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Limpa o texto dos comentários removendo caracteres especiais e normalizando.
    
    Args:
        data: Iterador de dicionários de comentários
        
    Yields:
        Comentários com texto limpo
    """
    for comment in data:
        if isinstance(comment, dict) and 'text' in comment:
            # Remove caracteres especiais e normaliza espaços
            text = comment['text']
            # Remove caracteres especiais mantendo acentos
            cleaned_text = re.sub(r'[^\w\sáàâãéèêíìîóòôõúùûçñÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇÑ]', ' ', text)
            # Normaliza espaços múltiplos
            cleaned_text = ' '.join(cleaned_text.split())
            
            # Cria uma cópia do comentário com texto limpo
            cleaned_comment = comment.copy()
            cleaned_comment['text'] = cleaned_text
            yield cleaned_comment
        else:
            yield comment


def filter_by_sentiment(data: Iterator[Dict[str, Any]], sentiment: str = "positive") -> Iterator[Dict[str, Any]]:
    """
    Filtra comentários por sentimento específico.
    
    Args:
        data: Iterador de dicionários de comentários
        sentiment: Sentimento a filtrar ("positive" ou "negative")
        
    Yields:
        Apenas comentários com o sentimento especificado
    """
    for comment in data:
        if isinstance(comment, dict) and comment.get('sentiment') == sentiment:
            yield comment


def filter_by_language(data: Iterator[Dict[str, Any]], language: str = "portuguese") -> Iterator[Dict[str, Any]]:
    """
    Filtra comentários por idioma detectado.
    
    Args:
        data: Iterador de dicionários de comentários
        language: Idioma a filtrar ("portuguese", "english", "spanish", "french", "german")
        
    Yields:
        Apenas comentários no idioma especificado
    """
    # Padrões para detectar idiomas
    language_patterns = {
        "portuguese": r'\b(não|sim|muito|bom|ruim|excelente|péssimo|adorei|gostei|não gostei)\b',
        "english": r'\b(the|and|for|you|are|was|very|good|bad|excellent|terrible|love|like|hate)\b',
        "spanish": r'\b(el|la|de|que|y|es|muy|bueno|malo|excelente|terrible|me encantó|no me gustó)\b',
        "french": r'\b(le|la|de|que|et|est|très|bon|mauvais|excellent|terrible|j\'ai adoré|je n\'ai pas aimé)\b',
        "german": r'\b(der|die|das|und|für|ist|sehr|gut|schlecht|ausgezeichnet|schrecklich|ich liebe|ich hasse)\b'
    }
    
    pattern = language_patterns.get(language.lower(), language_patterns["portuguese"])
    
    for comment in data:
        if isinstance(comment, dict) and 'text' in comment:
            text = comment['text'].lower()
            if re.search(pattern, text, re.IGNORECASE):
                yield comment


def filter_by_country(data: Iterator[Dict[str, Any]], countries: List[str]) -> Iterator[Dict[str, Any]]:
    """
    Filtra comentários por países específicos.
    
    Args:
        data: Iterador de dicionários de comentários
        countries: Lista de países para filtrar
        
    Yields:
        Apenas comentários dos países especificados
    """
    for comment in data:
        if isinstance(comment, dict) and comment.get('country') in countries:
            yield comment


def filter_by_likes_threshold(data: Iterator[Dict[str, Any]], min_likes: int = 0, max_likes: int = None) -> Iterator[Dict[str, Any]]:
    """
    Filtra comentários por faixa de likes.
    
    Args:
        data: Iterador de dicionários de comentários
        min_likes: Número mínimo de likes
        max_likes: Número máximo de likes (None para sem limite)
        
    Yields:
        Apenas comentários dentro da faixa de likes especificada
    """
    for comment in data:
        if isinstance(comment, dict) and 'likes' in comment:
            likes = comment['likes']
            if likes >= min_likes and (max_likes is None or likes <= max_likes):
                yield comment


def add_engagement_score(data: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Adiciona um score de engajamento baseado em likes e sentimento.
    
    Args:
        data: Iterador de dicionários de comentários
        
    Yields:
        Comentários com score de engajamento adicionado
    """
    for comment in data:
        if isinstance(comment, dict):
            # Calcula score baseado em likes e sentimento
            likes = comment.get('likes', 0)
            sentiment = comment.get('sentiment', 'neutral')
            
            # Score base: likes / 10
            base_score = likes / 10
            
            # Multiplicador por sentimento
            sentiment_multiplier = 1.2 if sentiment == 'positive' else 0.8
            
            engagement_score = round(base_score * sentiment_multiplier, 2)
            
            # Adiciona o score ao comentário
            enhanced_comment = comment.copy()
            enhanced_comment['engagement_score'] = engagement_score
            yield enhanced_comment


def detect_spam(data: Iterator[Dict[str, Any]], max_repeated_chars: int = 3) -> Iterator[Dict[str, Any]]:
    """
    Detecta possíveis comentários spam baseado em padrões.
    
    Args:
        data: Iterador de dicionários de comentários
        max_repeated_chars: Número máximo de caracteres repetidos consecutivos
        
    Yields:
        Comentários com flag de spam adicionado
    """
    for comment in data:
        if isinstance(comment, dict) and 'text' in comment:
            text = comment['text']
            
            # Detecta caracteres repetidos excessivamente
            has_repeated_chars = False
            for char in text:
                if text.count(char * (max_repeated_chars + 1)) > 0:
                    has_repeated_chars = True
                    break
            
            # Detecta palavras repetidas
            words = text.split()
            has_repeated_words = len(words) > 3 and len(set(words)) < len(words) * 0.5
            
            # Detecta texto muito curto ou muito longo
            is_suspicious_length = len(text) < 5 or len(text) > 500
            
            # Determina se é spam
            is_spam = has_repeated_chars or has_repeated_words or is_suspicious_length
            
            # Adiciona flag de spam
            enhanced_comment = comment.copy()
            enhanced_comment['is_spam'] = is_spam
            enhanced_comment['spam_reason'] = []
            
            if has_repeated_chars:
                enhanced_comment['spam_reason'].append('repeated_chars')
            if has_repeated_words:
                enhanced_comment['spam_reason'].append('repeated_words')
            if is_suspicious_length:
                enhanced_comment['spam_reason'].append('suspicious_length')
            
            yield enhanced_comment


def normalize_user_names(data: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Normaliza nomes de usuários para consistência.
    
    Args:
        data: Iterador de dicionários de comentários
        
    Yields:
        Comentários com nomes de usuário normalizados
    """
    for comment in data:
        if isinstance(comment, dict) and 'user' in comment:
            user = comment['user']
            
            # Normaliza o nome: primeira letra maiúscula, resto minúscula
            normalized_user = ' '.join(word.capitalize() for word in user.split())
            
            # Adiciona o nome normalizado
            enhanced_comment = comment.copy()
            enhanced_comment['user_normalized'] = normalized_user
            yield enhanced_comment


def add_text_metrics(data: Iterator[Dict[str, Any]]) -> Iterator[Dict[str, Any]]:
    """
    Adiciona métricas de texto aos comentários.
    
    Args:
        data: Iterador de dicionários de comentários
        
    Yields:
        Comentários com métricas de texto adicionadas
    """
    for comment in data:
        if isinstance(comment, dict) and 'text' in comment:
            text = comment['text']
            
            # Calcula métricas
            char_count = len(text)
            word_count = len(text.split())
            avg_word_length = round(char_count / word_count, 2) if word_count > 0 else 0
            
            # Conta pontuação
            punctuation_count = sum(1 for char in text if char in '.,!?;:')
            
            # Conta maiúsculas
            uppercase_count = sum(1 for char in text if char.isupper())
            
            # Adiciona métricas ao comentário
            enhanced_comment = comment.copy()
            enhanced_comment['text_metrics'] = {
                'char_count': char_count,
                'word_count': word_count,
                'avg_word_length': avg_word_length,
                'punctuation_count': punctuation_count,
                'uppercase_count': uppercase_count
            }
            yield enhanced_comment
