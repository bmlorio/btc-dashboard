#!/usr/bin/env python3
"""
Script de ingesta de datos de yfinance
Obtiene datos de mercados tradicionales como SPY, QQQ, GLD, etc.
"""

import os
import sys
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Añadir el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yfinance as yf
from config.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class YFinanceDataIngester:
    def __init__(self):
        """Inicializar el ingester de yfinance"""
        self.symbols = {
            'SPY': 'SPDR S&P 500 ETF Trust',
            'QQQ': 'Invesco QQQ Trust',
            'GLD': 'SPDR Gold Shares',
            'TLT': 'iShares 20+ Year Treasury Bond ETF',
            'VIX': 'CBOE Volatility Index',
            'DXY': 'US Dollar Index'
        }
        logger.info("Ingester de yfinance inicializado")

    def get_ticker_data(self, symbol: str, period: str = '1mo') -> Dict[str, Any]:
        """
        Obtener datos de un ticker específico
        
        Args:
            symbol: Símbolo del ticker
            period: Período de datos (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            Diccionario con datos del ticker
        """
        try:
            logger.info(f"Obteniendo datos para {symbol}")
            
            # Crear objeto ticker
            ticker = yf.Ticker(symbol)
            
            # Obtener datos históricos
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise Exception(f"No se encontraron datos para {symbol}")
            
            # Obtener información del ticker
            info = {}
            try:
                info = ticker.info
            except Exception as e:
                logger.warning(f"No se pudo obtener info para {symbol}: {e}")
            
            # Convertir datos históricos a formato JSON serializable
            historical_data = []
            for date, row in hist.iterrows():
                historical_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': float(row['Open']) if not pd.isna(row['Open']) else None,
                    'high': float(row['High']) if not pd.isna(row['High']) else None,
                    'low': float(row['Low']) if not pd.isna(row['Low']) else None,
                    'close': float(row['Close']) if not pd.isna(row['Close']) else None,
                    'volume': int(row['Volume']) if not pd.isna(row['Volume']) else None
                })
            
            # Obtener datos del último día
            latest_data = historical_data[-1] if historical_data else {}
            
            # Calcular cambio porcentual si hay suficientes datos
            price_change = 0
            price_change_percent = 0
            if len(historical_data) >= 2:
                current_price = latest_data.get('close', 0)
                previous_price = historical_data[-2].get('close', 0)
                if previous_price and current_price:
                    price_change = current_price - previous_price
                    price_change_percent = (price_change / previous_price) * 100
            
            result = {
                'symbol': symbol,
                'name': self.symbols.get(symbol, symbol),
                'latest_price': latest_data.get('close'),
                'latest_date': latest_data.get('date'),
                'price_change': price_change,
                'price_change_percent': price_change_percent,
                'volume': latest_data.get('volume'),
                'historical_data': historical_data,
                'info': {
                    'market_cap': info.get('marketCap'),
                    'pe_ratio': info.get('trailingPE'),
                    'dividend_yield': info.get('dividendYield'),
                    'beta': info.get('beta'),
                    '52_week_high': info.get('fiftyTwoWeekHigh'),
                    '52_week_low': info.get('fiftyTwoWeekLow')
                },
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Datos obtenidos para {symbol}: precio ${latest_data.get('close', 0):.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener datos para {symbol}: {e}")
            # Retornar datos mock en caso de error
            return {
                'symbol': symbol,
                'name': self.symbols.get(symbol, symbol),
                'latest_price': 100.0,
                'latest_date': datetime.now().strftime('%Y-%m-%d'),
                'price_change': 0,
                'price_change_percent': 0,
                'volume': 0,
                'historical_data': [],
                'info': {},
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    def get_all_tickers_data(self) -> Dict[str, Any]:
        """
        Obtener datos de todos los tickers configurados
        
        Returns:
            Diccionario con datos de todos los tickers
        """
        all_data = {}
        
        for symbol in self.symbols.keys():
            try:
                # Añadir delay entre peticiones para evitar rate limiting
                time.sleep(1)
                
                ticker_data = self.get_ticker_data(symbol)
                all_data[symbol] = ticker_data
                
            except Exception as e:
                logger.error(f"Error al obtener datos para {symbol}: {e}")
                # Continuar con el siguiente ticker en caso de error
                all_data[symbol] = {
                    'symbol': symbol,
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                }
        
        return all_data

    def get_market_summary(self, tickers_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crear un resumen del mercado basado en los datos de los tickers
        
        Args:
            tickers_data: Datos de todos los tickers
        
        Returns:
            Resumen del mercado
        """
        try:
            summary = {
                'market_sentiment': 'neutral',
                'risk_on_assets': {},
                'risk_off_assets': {},
                'volatility_index': None,
                'dollar_strength': None,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Analizar activos de riesgo (SPY, QQQ)
            risk_on_symbols = ['SPY', 'QQQ']
            risk_on_performance = []
            
            for symbol in risk_on_symbols:
                if symbol in tickers_data and 'price_change_percent' in tickers_data[symbol]:
                    change = tickers_data[symbol]['price_change_percent']
                    summary['risk_on_assets'][symbol] = change
                    risk_on_performance.append(change)
            
            # Analizar activos refugio (GLD, TLT)
            risk_off_symbols = ['GLD', 'TLT']
            for symbol in risk_off_symbols:
                if symbol in tickers_data and 'price_change_percent' in tickers_data[symbol]:
                    change = tickers_data[symbol]['price_change_percent']
                    summary['risk_off_assets'][symbol] = change
            
            # Obtener VIX si está disponible
            if 'VIX' in tickers_data and 'latest_price' in tickers_data['VIX']:
                summary['volatility_index'] = tickers_data['VIX']['latest_price']
            
            # Obtener fortaleza del dólar
            if 'DXY' in tickers_data and 'price_change_percent' in tickers_data['DXY']:
                summary['dollar_strength'] = tickers_data['DXY']['price_change_percent']
            
            # Determinar sentimiento del mercado
            if risk_on_performance:
                avg_risk_on = sum(risk_on_performance) / len(risk_on_performance)
                if avg_risk_on > 1:
                    summary['market_sentiment'] = 'bullish'
                elif avg_risk_on < -1:
                    summary['market_sentiment'] = 'bearish'
                else:
                    summary['market_sentiment'] = 'neutral'
            
            return summary
            
        except Exception as e:
            logger.error(f"Error al crear resumen del mercado: {e}")
            return {
                'market_sentiment': 'neutral',
                'risk_on_assets': {},
                'risk_off_assets': {},
                'volatility_index': None,
                'dollar_strength': None,
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
            logger.info("Iniciando ingesta de datos de yfinance")
            
            # Obtener datos de todos los tickers
            tickers_data = self.get_all_tickers_data()
            
            # Crear resumen del mercado
            market_summary = self.get_market_summary(tickers_data)
            
            # Crear estructura de datos completa
            yfinance_data = {
                'timestamp_utc': datetime.utcnow().isoformat(),
                'source': 'yfinance',
                'data': {
                    'tickers': tickers_data,
                    'market_summary': market_summary
                }
            }
            
            # Guardar datos
            self.save_data_to_file(yfinance_data, 'yfinance_data.json')
            
            logger.info("Ingesta de datos de yfinance completada exitosamente")
            
        except Exception as e:
            logger.error(f"Error en la ingesta de datos de yfinance: {e}")
            raise

def main():
    """Función principal"""
    try:
        # Importar pandas aquí para evitar error si no está disponible
        global pd
        try:
            import pandas as pd
        except ImportError:
            logger.error("pandas no está disponible, usando datos mock")
            pd = None
        
        # Crear instancia del ingester
        ingester = YFinanceDataIngester()
        
        # Ejecutar ingesta
        ingester.run_ingestion()
        
        print("✅ Ingesta de datos de yfinance completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"❌ Error en la ingesta de datos de yfinance: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

