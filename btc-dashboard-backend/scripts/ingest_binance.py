#!/usr/bin/env python3
"""
Script de ingesta de datos de Binance
Obtiene datos de klines (velas) y open interest para BTC/USDT
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any

# Añadir el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.client import Client
from binance.exceptions import BinanceAPIException
from config.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BinanceDataIngester:
    def __init__(self):
        """Inicializar el cliente de Binance"""
        try:
            self.client = Client(Config.BINANCE_API_KEY, Config.BINANCE_API_SECRET)
            logger.info("Cliente de Binance inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar cliente de Binance: {e}")
            raise

    def get_klines_data(self, symbol: str = 'BTCUSDT', interval: str = '4h', limit: int = 500) -> List[Dict]:
        """
        Obtener datos de klines (velas) de Binance
        
        Args:
            symbol: Par de trading (default: BTCUSDT)
            interval: Intervalo de tiempo (default: 4h)
            limit: Número de velas a obtener (default: 500)
        
        Returns:
            Lista de diccionarios con datos de klines
        """
        try:
            logger.info(f"Obteniendo klines para {symbol} con intervalo {interval}")
            
            # Obtener klines desde Binance
            klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
            
            # Formatear los datos
            formatted_klines = []
            for kline in klines:
                formatted_kline = {
                    'timestamp': int(kline[0]),
                    'datetime': datetime.fromtimestamp(int(kline[0]) / 1000).isoformat(),
                    'open': float(kline[1]),
                    'high': float(kline[2]),
                    'low': float(kline[3]),
                    'close': float(kline[4]),
                    'volume': float(kline[5]),
                    'close_time': int(kline[6]),
                    'quote_asset_volume': float(kline[7]),
                    'number_of_trades': int(kline[8]),
                    'taker_buy_base_asset_volume': float(kline[9]),
                    'taker_buy_quote_asset_volume': float(kline[10])
                }
                formatted_klines.append(formatted_kline)
            
            logger.info(f"Obtenidos {len(formatted_klines)} klines para {symbol}")
            return formatted_klines
            
        except BinanceAPIException as e:
            logger.error(f"Error de API de Binance: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al obtener klines: {e}")
            raise

    def get_futures_open_interest(self, symbol: str = 'BTCUSDT') -> Dict[str, Any]:
        """
        Obtener datos de open interest de futuros
        
        Args:
            symbol: Par de trading (default: BTCUSDT)
        
        Returns:
            Diccionario con datos de open interest
        """
        try:
            logger.info(f"Obteniendo open interest para {symbol}")
            
            # Obtener open interest actual
            oi_data = self.client.futures_open_interest(symbol=symbol)
            
            # Formatear los datos
            formatted_oi = {
                'symbol': oi_data['symbol'],
                'open_interest': float(oi_data['openInterest']),
                'timestamp': int(oi_data['time']),
                'datetime': datetime.fromtimestamp(int(oi_data['time']) / 1000).isoformat()
            }
            
            logger.info(f"Open interest obtenido para {symbol}: {formatted_oi['open_interest']}")
            return formatted_oi
            
        except BinanceAPIException as e:
            logger.error(f"Error de API de Binance al obtener open interest: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al obtener open interest: {e}")
            raise

    def get_24hr_ticker_stats(self, symbol: str = 'BTCUSDT') -> Dict[str, Any]:
        """
        Obtener estadísticas de 24 horas
        
        Args:
            symbol: Par de trading (default: BTCUSDT)
        
        Returns:
            Diccionario con estadísticas de 24h
        """
        try:
            logger.info(f"Obteniendo estadísticas 24h para {symbol}")
            
            ticker = self.client.get_ticker(symbol=symbol)
            
            formatted_ticker = {
                'symbol': ticker['symbol'],
                'price_change': float(ticker['priceChange']),
                'price_change_percent': float(ticker['priceChangePercent']),
                'weighted_avg_price': float(ticker['weightedAvgPrice']),
                'prev_close_price': float(ticker['prevClosePrice']),
                'last_price': float(ticker['lastPrice']),
                'bid_price': float(ticker['bidPrice']),
                'ask_price': float(ticker['askPrice']),
                'open_price': float(ticker['openPrice']),
                'high_price': float(ticker['highPrice']),
                'low_price': float(ticker['lowPrice']),
                'volume': float(ticker['volume']),
                'quote_volume': float(ticker['quoteVolume']),
                'open_time': int(ticker['openTime']),
                'close_time': int(ticker['closeTime']),
                'count': int(ticker['count']),
                'datetime': datetime.fromtimestamp(int(ticker['closeTime']) / 1000).isoformat()
            }
            
            logger.info(f"Estadísticas 24h obtenidas para {symbol}: precio actual {formatted_ticker['last_price']}")
            return formatted_ticker
            
        except BinanceAPIException as e:
            logger.error(f"Error de API de Binance al obtener ticker: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al obtener ticker: {e}")
            raise

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
            logger.info("Iniciando ingesta de datos de Binance")
            
            # Obtener datos de klines
            klines_data = self.get_klines_data()
            
            # Obtener open interest
            oi_data = self.get_futures_open_interest()
            
            # Obtener estadísticas 24h
            ticker_data = self.get_24hr_ticker_stats()
            
            # Crear estructura de datos completa
            binance_data = {
                'timestamp_utc': datetime.utcnow().isoformat(),
                'source': 'binance',
                'data': {
                    'klines': klines_data,
                    'open_interest': oi_data,
                    'ticker_24h': ticker_data
                }
            }
            
            # Guardar datos
            self.save_data_to_file(binance_data, 'binance_data.json')
            
            logger.info("Ingesta de datos de Binance completada exitosamente")
            
        except Exception as e:
            logger.error(f"Error en la ingesta de datos de Binance: {e}")
            raise

def main():
    """Función principal"""
    try:
        # Validar configuración
        Config.validate_config()
        
        # Crear instancia del ingester
        ingester = BinanceDataIngester()
        
        # Ejecutar ingesta
        ingester.run_ingestion()
        
        print("✅ Ingesta de datos de Binance completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"❌ Error en la ingesta de datos de Binance: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

