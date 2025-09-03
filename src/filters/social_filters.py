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


def get_top_users_by_comments(data: Iterator[Dict[str, Any]], top_n: int = 10) -> Iterator[Dict[str, Any]]:
    """
    Extrai os X usuários que mais comentaram.
    
    Args:
        data: Iterador de dicionários de comentários
        top_n: Número de usuários top a retornar
        
    Yields:
        Dicionários com nome do usuário e quantidade de comentários
    """
    # Coleta todos os comentários para análise
    comments_list = list(data)
    
    # Conta comentários por usuário
    user_comment_counts = {}
    for comment in comments_list:
        if isinstance(comment, dict):
            # Tenta diferentes campos possíveis para o nome do usuário
            user_name = comment.get('user_name') or comment.get('user') or comment.get('username') or 'Usuário Desconhecido'
            
            if user_name in user_comment_counts:
                user_comment_counts[user_name] += 1
            else:
                user_comment_counts[user_name] = 1
    
    # Ordena usuários por quantidade de comentários (decrescente)
    sorted_users = sorted(user_comment_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Retorna os top N usuários com formato simplificado
    for user_name, comment_count in sorted_users[:top_n]:
        yield {
            'nome': user_name,
            'quantidade_comentario': comment_count
        }


def get_user_engagement_summary(data: Iterator[Dict[str, Any]], top_n: int = 10) -> Iterator[Dict[str, Any]]:
    """
    Cria um resumo completo de engajamento dos usuários top.
    
    Args:
        data: Iterador de dicionários de comentários
        top_n: Número de usuários top a analisar
        
    Yields:
        Dicionários com resumo completo de cada usuário top
    """
    # Coleta todos os comentários para análise
    comments_list = list(data)
    
    # Agrupa comentários por usuário
    user_comments = {}
    for comment in comments_list:
        if isinstance(comment, dict):
            user_name = comment.get('user_name') or comment.get('user') or comment.get('username') or 'Usuário Desconhecido'
            
            if user_name not in user_comments:
                user_comments[user_name] = []
            user_comments[user_name].append(comment)
    
    # Calcula estatísticas para cada usuário
    user_stats = []
    for user_name, user_comment_list in user_comments.items():
        total_likes = sum(comment.get('likes', 0) for comment in user_comment_list)
        avg_likes = total_likes / len(user_comment_list) if user_comment_list else 0
        
        # Conta sentimentos
        sentiments = [comment.get('sentiment', 'neutral') for comment in user_comment_list]
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        # Calcula score de engajamento médio
        engagement_scores = [comment.get('engagement_score', 0) for comment in user_comment_list]
        avg_engagement = sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0
        
        user_stats.append({
            'user_name': user_name,
            'comment_count': len(user_comment_list),
            'total_likes': total_likes,
            'avg_likes': round(avg_likes, 2),
            'positive_comments': positive_count,
            'negative_comments': negative_count,
            'neutral_comments': neutral_count,
            'avg_engagement_score': round(avg_engagement, 2)
        })
    
    # Ordena por quantidade de comentários
    sorted_stats = sorted(user_stats, key=lambda x: x['comment_count'], reverse=True)
    
    # Retorna os top N usuários com estatísticas completas
    for i, stats in enumerate(sorted_stats[:top_n], 1):
        stats['rank'] = i
        stats['percentage'] = round((stats['comment_count'] / len(comments_list)) * 100, 2)
        yield stats
