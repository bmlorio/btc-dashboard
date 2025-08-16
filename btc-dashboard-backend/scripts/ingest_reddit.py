#!/usr/bin/env python3
"""
Script de ingesta de datos de Reddit
Obtiene posts populares de subreddits relacionados con Bitcoin y criptomonedas
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Añadir el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import praw
from config.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RedditDataIngester:
    def __init__(self):
        """Inicializar el cliente de Reddit (PRAW)"""
        try:
            if Config.REDDIT_CLIENT_ID and Config.REDDIT_CLIENT_SECRET:
                self.reddit = praw.Reddit(
                    client_id=Config.REDDIT_CLIENT_ID,
                    client_secret=Config.REDDIT_CLIENT_SECRET,
                    user_agent=Config.REDDIT_USER_AGENT
                )
                logger.info("Cliente de Reddit inicializado correctamente")
            else:
                logger.warning("Credenciales de Reddit no disponibles, usando datos mock")
                self.reddit = None
                
            # Subreddits a monitorear
            self.subreddits = [
                'Bitcoin',
                'CryptoCurrency', 
                'btc',
                'BitcoinMarkets',
                'CryptoMarkets'
            ]
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente de Reddit: {e}")
            self.reddit = None

    def get_subreddit_posts(self, subreddit_name: str, limit: int = 10, time_filter: str = 'day') -> List[Dict[str, Any]]:
        """
        Obtener posts populares de un subreddit
        
        Args:
            subreddit_name: Nombre del subreddit
            limit: Número de posts a obtener
            time_filter: Filtro de tiempo ('hour', 'day', 'week', 'month', 'year', 'all')
        
        Returns:
            Lista de posts
        """
        try:
            if not self.reddit:
                # Retornar datos mock si no hay cliente Reddit
                return [{
                    'id': 'mock_post',
                    'title': f'Mock post from r/{subreddit_name}',
                    'score': 100,
                    'num_comments': 50,
                    'created_utc': datetime.utcnow().timestamp(),
                    'author': 'mock_user',
                    'url': f'https://reddit.com/r/{subreddit_name}',
                    'selftext': 'Mock post content',
                    'upvote_ratio': 0.85,
                    'error': 'No Reddit credentials available'
                }]
            
            logger.info(f"Obteniendo posts de r/{subreddit_name}")
            
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = []
            
            # Obtener posts populares del día
            for submission in subreddit.top(time_filter=time_filter, limit=limit):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': submission.created_utc,
                    'created_datetime': datetime.fromtimestamp(submission.created_utc).isoformat(),
                    'author': str(submission.author) if submission.author else '[deleted]',
                    'url': submission.url,
                    'permalink': f"https://reddit.com{submission.permalink}",
                    'selftext': submission.selftext[:500] if submission.selftext else '',  # Limitar texto
                    'upvote_ratio': submission.upvote_ratio,
                    'is_self': submission.is_self,
                    'domain': submission.domain,
                    'subreddit': subreddit_name
                }
                posts.append(post_data)
            
            logger.info(f"Obtenidos {len(posts)} posts de r/{subreddit_name}")
            return posts
            
        except Exception as e:
            logger.error(f"Error al obtener posts de r/{subreddit_name}: {e}")
            # Retornar datos mock en caso de error
            return [{
                'id': 'error_post',
                'title': f'Error fetching from r/{subreddit_name}',
                'score': 0,
                'num_comments': 0,
                'created_utc': datetime.utcnow().timestamp(),
                'created_datetime': datetime.utcnow().isoformat(),
                'author': 'system',
                'url': '',
                'permalink': '',
                'selftext': '',
                'upvote_ratio': 0.5,
                'is_self': True,
                'domain': 'self',
                'subreddit': subreddit_name,
                'error': str(e)
            }]

    def get_all_subreddits_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtener datos de todos los subreddits configurados
        
        Returns:
            Diccionario con posts de todos los subreddits
        """
        all_posts = {}
        
        for subreddit_name in self.subreddits:
            try:
                posts = self.get_subreddit_posts(subreddit_name, limit=5)
                all_posts[subreddit_name] = posts
                
                # Pequeña pausa entre peticiones para respetar rate limits
                import time
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error al obtener datos de r/{subreddit_name}: {e}")
                all_posts[subreddit_name] = []
        
        return all_posts

    def analyze_sentiment(self, posts_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Analizar el sentimiento general basado en los posts
        
        Args:
            posts_data: Datos de posts de todos los subreddits
        
        Returns:
            Análisis de sentimiento
        """
        try:
            total_posts = 0
            total_score = 0
            total_comments = 0
            positive_posts = 0
            negative_posts = 0
            
            # Palabras clave para análisis básico de sentimiento
            positive_keywords = ['bullish', 'moon', 'pump', 'buy', 'hodl', 'up', 'green', 'profit', 'gain']
            negative_keywords = ['bearish', 'dump', 'sell', 'down', 'red', 'loss', 'crash', 'dip']
            
            for subreddit, posts in posts_data.items():
                for post in posts:
                    if 'error' in post:
                        continue
                        
                    total_posts += 1
                    total_score += post.get('score', 0)
                    total_comments += post.get('num_comments', 0)
                    
                    # Análisis básico de sentimiento basado en título
                    title_lower = post.get('title', '').lower()
                    text_lower = post.get('selftext', '').lower()
                    combined_text = f"{title_lower} {text_lower}"
                    
                    positive_count = sum(1 for keyword in positive_keywords if keyword in combined_text)
                    negative_count = sum(1 for keyword in negative_keywords if keyword in combined_text)
                    
                    if positive_count > negative_count:
                        positive_posts += 1
                    elif negative_count > positive_count:
                        negative_posts += 1
            
            # Calcular métricas
            avg_score = total_score / total_posts if total_posts > 0 else 0
            avg_comments = total_comments / total_posts if total_posts > 0 else 0
            
            sentiment_ratio = 0.5  # neutral por defecto
            if positive_posts + negative_posts > 0:
                sentiment_ratio = positive_posts / (positive_posts + negative_posts)
            
            # Determinar sentimiento general
            if sentiment_ratio > 0.6:
                overall_sentiment = 'bullish'
            elif sentiment_ratio < 0.4:
                overall_sentiment = 'bearish'
            else:
                overall_sentiment = 'neutral'
            
            analysis = {
                'overall_sentiment': overall_sentiment,
                'sentiment_ratio': sentiment_ratio,
                'total_posts_analyzed': total_posts,
                'positive_posts': positive_posts,
                'negative_posts': negative_posts,
                'neutral_posts': total_posts - positive_posts - negative_posts,
                'average_score': avg_score,
                'average_comments': avg_comments,
                'total_engagement': total_score + total_comments,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Análisis de sentimiento completado: {overall_sentiment} (ratio: {sentiment_ratio:.2f})")
            return analysis
            
        except Exception as e:
            logger.error(f"Error en análisis de sentimiento: {e}")
            return {
                'overall_sentiment': 'neutral',
                'sentiment_ratio': 0.5,
                'total_posts_analyzed': 0,
                'positive_posts': 0,
                'negative_posts': 0,
                'neutral_posts': 0,
                'average_score': 0,
                'average_comments': 0,
                'total_engagement': 0,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    def get_trending_topics(self, posts_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Identificar temas trending basados en los posts
        
        Args:
            posts_data: Datos de posts de todos los subreddits
        
        Returns:
            Lista de temas trending
        """
        try:
            # Palabras clave comunes a filtrar
            common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'bitcoin', 'btc', 'crypto', 'cryptocurrency'}
            
            word_count = {}
            trending_posts = []
            
            for subreddit, posts in posts_data.items():
                for post in posts:
                    if 'error' in post:
                        continue
                    
                    # Agregar posts con alto engagement a trending
                    if post.get('score', 0) > 100 or post.get('num_comments', 0) > 50:
                        trending_posts.append({
                            'title': post.get('title', ''),
                            'subreddit': subreddit,
                            'score': post.get('score', 0),
                            'comments': post.get('num_comments', 0),
                            'url': post.get('permalink', ''),
                            'engagement': post.get('score', 0) + post.get('num_comments', 0)
                        })
                    
                    # Contar palabras en títulos
                    title = post.get('title', '').lower()
                    words = title.split()
                    for word in words:
                        # Limpiar palabra
                        word = ''.join(c for c in word if c.isalnum())
                        if len(word) > 3 and word not in common_words:
                            word_count[word] = word_count.get(word, 0) + 1
            
            # Ordenar posts trending por engagement
            trending_posts.sort(key=lambda x: x['engagement'], reverse=True)
            
            # Obtener top palabras
            top_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:10]
            
            result = {
                'trending_posts': trending_posts[:5],  # Top 5 posts
                'trending_keywords': [{'word': word, 'count': count} for word, count in top_words],
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Identificados {len(trending_posts)} posts trending y {len(top_words)} palabras clave")
            return result
            
        except Exception as e:
            logger.error(f"Error al identificar temas trending: {e}")
            return {
                'trending_posts': [],
                'trending_keywords': [],
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    def save_data_to_file(self, data: Dict[str, Any], filename: str) -> None:
        """
        Guardar datos en archivo JSON
        
        Args:
            data: Datos a guardar
            filename: Nombre del archivo
        """
        try:
            # Crear directorio de datos si no existe
            os.makedirs(Config.DATA_DIR, exist_ok=True)
            
            filepath = os.path.join(Config.DATA_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Datos guardados en {filepath}")
            
        except Exception as e:
            logger.error(f"Error al guardar datos en {filename}: {e}")
            raise

    def run_ingestion(self) -> None:
        """Ejecutar el proceso completo de ingesta de datos"""
        try:
            logger.info("Iniciando ingesta de datos de Reddit")
            
            # Obtener posts de todos los subreddits
            posts_data = self.get_all_subreddits_data()
            
            # Analizar sentimiento
            sentiment_analysis = self.analyze_sentiment(posts_data)
            
            # Identificar temas trending
            trending_topics = self.get_trending_topics(posts_data)
            
            # Crear estructura de datos completa
            reddit_data = {
                'timestamp_utc': datetime.utcnow().isoformat(),
                'source': 'reddit',
                'data': {
                    'posts_by_subreddit': posts_data,
                    'sentiment_analysis': sentiment_analysis,
                    'trending_topics': trending_topics
                }
            }
            
            # Guardar datos
            self.save_data_to_file(reddit_data, 'reddit_data.json')
            
            logger.info("Ingesta de datos de Reddit completada exitosamente")
            
        except Exception as e:
            logger.error(f"Error en la ingesta de datos de Reddit: {e}")
            raise

def main():
    """Función principal"""
    try:
        # Crear instancia del ingester
        ingester = RedditDataIngester()
        
        # Ejecutar ingesta
        ingester.run_ingestion()
        
        print("✅ Ingesta de datos de Reddit completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"❌ Error en la ingesta de datos de Reddit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

