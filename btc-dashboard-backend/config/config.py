import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    # API Keys
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET')
    
    COINGLASS_API_KEY = os.getenv('COINGLASS_API_KEY')
    
    GLASSNODE_API_KEY = os.getenv('GLASSNODE_API_KEY')
    
    FRED_API_KEY = os.getenv('FRED_API_KEY')
    
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'btc-dashboard:v1.0 (by /u/your_username)')
    
    # Cloudflare R2 / S3 Compatible Storage
    R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
    R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
    R2_ENDPOINT_URL = os.getenv('R2_ENDPOINT_URL')
    R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
    
    # URLs de APIs
    BINANCE_BASE_URL = 'https://api.binance.com'
    COINGLASS_BASE_URL = 'https://open-api.coinglass.com'
    GLASSNODE_BASE_URL = 'https://api.glassnode.com'
    FRED_BASE_URL = 'https://api.stlouisfed.org/fred'
    
    # Configuración de datos
    DATA_DIR = 'data'
    
    # Configuración de Flask
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configuración de CORS
    CORS_ORIGINS = ['*']  # Permitir todas las origins para desarrollo
    
    @classmethod
    def validate_config(cls):
        """Valida que las configuraciones críticas estén presentes"""
        required_vars = [
            'BINANCE_API_KEY', 'BINANCE_API_SECRET',
            'R2_ACCESS_KEY_ID', 'R2_SECRET_ACCESS_KEY', 
            'R2_ENDPOINT_URL', 'R2_BUCKET_NAME'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Faltan las siguientes variables de entorno: {', '.join(missing_vars)}")
        
        return True

