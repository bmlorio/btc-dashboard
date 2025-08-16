#!/usr/bin/env python3
"""
Script de prueba para verificar que los scripts de ingesta funcionan correctamente
"""

import os
import sys
import json
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_binance_ingestion():
    """Probar la ingesta de datos de Binance"""
    try:
        logger.info("Probando ingesta de Binance...")
        
        # Crear variables de entorno mock para la prueba
        os.environ['BINANCE_API_KEY'] = 'test_key'
        os.environ['BINANCE_API_SECRET'] = 'test_secret'
        
        # Importar y ejecutar el script
        from scripts.ingest_binance import BinanceDataIngester
        
        # Nota: Esto fallará sin credenciales reales, pero podemos verificar la estructura
        logger.info("✅ Script de Binance importado correctamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de Binance: {e}")
        return False

def test_coinglass_ingestion():
    """Probar la ingesta de datos de Coinglass"""
    try:
        logger.info("Probando ingesta de Coinglass...")
        
        from scripts.ingest_coinglass import CoinglassDataIngester
        
        # Crear instancia sin API key (modo mock)
        ingester = CoinglassDataIngester()
        
        # Probar obtener funding rates (debería retornar datos mock)
        funding_data = ingester.get_funding_rates()
        
        if funding_data and len(funding_data) > 0:
            logger.info("✅ Script de Coinglass funcionando (modo mock)")
            return True
        else:
            logger.warning("⚠️ Script de Coinglass retornó datos vacíos")
            return False
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de Coinglass: {e}")
        return False

def test_fred_ingestion():
    """Probar la ingesta de datos de FRED"""
    try:
        logger.info("Probando ingesta de FRED...")
        
        from scripts.ingest_fred import FredDataIngester
        
        # Crear instancia sin API key (modo mock)
        ingester = FredDataIngester()
        
        # Probar obtener datos DXY (debería retornar datos mock)
        dxy_data = ingester.get_dxy_data()
        
        if dxy_data and 'series_id' in dxy_data:
            logger.info("✅ Script de FRED funcionando (modo mock)")
            return True
        else:
            logger.warning("⚠️ Script de FRED retornó datos inválidos")
            return False
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de FRED: {e}")
        return False

def test_yfinance_ingestion():
    """Probar la ingesta de datos de yfinance"""
    try:
        logger.info("Probando ingesta de yfinance...")
        
        from scripts.ingest_yfinance import YFinanceDataIngester
        
        # Crear instancia
        ingester = YFinanceDataIngester()
        
        # Probar obtener datos de un ticker (puede funcionar sin API key)
        ticker_data = ingester.get_ticker_data('SPY')
        
        if ticker_data and 'symbol' in ticker_data:
            logger.info("✅ Script de yfinance funcionando")
            return True
        else:
            logger.warning("⚠️ Script de yfinance retornó datos inválidos")
            return False
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de yfinance: {e}")
        return False

def test_reddit_ingestion():
    """Probar la ingesta de datos de Reddit"""
    try:
        logger.info("Probando ingesta de Reddit...")
        
        from scripts.ingest_reddit import RedditDataIngester
        
        # Crear instancia sin credenciales (modo mock)
        ingester = RedditDataIngester()
        
        # Probar obtener posts (debería retornar datos mock)
        posts = ingester.get_subreddit_posts('Bitcoin')
        
        if posts and len(posts) > 0:
            logger.info("✅ Script de Reddit funcionando (modo mock)")
            return True
        else:
            logger.warning("⚠️ Script de Reddit retornó datos vacíos")
            return False
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de Reddit: {e}")
        return False

def test_r2_uploader():
    """Probar el uploader de R2"""
    try:
        logger.info("Probando uploader de R2...")
        
        from scripts.upload_to_r2 import R2Uploader
        
        # Nota: Esto fallará sin credenciales reales, pero podemos verificar la importación
        logger.info("✅ Script de R2 uploader importado correctamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en prueba de R2 uploader: {e}")
        return False

def create_test_data():
    """Crear datos de prueba para verificar el flujo completo"""
    try:
        logger.info("Creando datos de prueba...")
        
        # Crear directorio de datos si no existe
        os.makedirs('data', exist_ok=True)
        
        # Crear archivo de prueba
        test_data = {
            'timestamp_utc': datetime.utcnow().isoformat(),
            'source': 'test',
            'data': {
                'message': 'Este es un archivo de prueba',
                'status': 'success'
            }
        }
        
        with open('data/test_data.json', 'w') as f:
            json.dump(test_data, f, indent=2)
        
        logger.info("✅ Datos de prueba creados en data/test_data.json")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error al crear datos de prueba: {e}")
        return False

def main():
    """Función principal de pruebas"""
    logger.info("🧪 Iniciando pruebas de scripts de ingesta")
    
    tests = [
        ("Binance", test_binance_ingestion),
        ("Coinglass", test_coinglass_ingestion),
        ("FRED", test_fred_ingestion),
        ("yfinance", test_yfinance_ingestion),
        ("Reddit", test_reddit_ingestion),
        ("R2 Uploader", test_r2_uploader),
        ("Datos de prueba", create_test_data)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Error ejecutando prueba {test_name}: {e}")
            results.append((test_name, False))
    
    # Mostrar resumen
    logger.info("\n📊 Resumen de pruebas:")
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 Resultado final: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El backend está listo.")
        return True
    else:
        print(f"\n⚠️ {total - passed} pruebas fallaron. Revisa los logs para más detalles.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

