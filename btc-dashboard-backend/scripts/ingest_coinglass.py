#!/usr/bin/env python3
"""
Script de ingesta de datos de Coinglass
Obtiene datos de funding rates, liquidaciones y long/short ratios
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Añadir el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoinglassDataIngester:
    def __init__(self):
        """Inicializar el cliente de Coinglass"""
        self.base_url = Config.COINGLASS_BASE_URL
        self.api_key = Config.COINGLASS_API_KEY
        self.session = requests.Session()
        
        # Configurar headers
        self.session.headers.update({
            'User-Agent': 'btc-dashboard/1.0',
            'Accept': 'application/json'
        })
        
        # Añadir API key si está disponible
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
            logger.info("Cliente de Coinglass inicializado con API key")
        else:
            logger.warning("Cliente de Coinglass inicializado sin API key (límites más restrictivos)")

    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Realizar petición HTTP a la API de Coinglass
        
        Args:
            endpoint: Endpoint de la API
            params: Parámetros de la petición
        
        Returns:
            Respuesta JSON de la API
        """
        try:
            url = f"{self.base_url}{endpoint}"
            
            logger.info(f"Realizando petición a: {url}")
            
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('success', True):  # Algunos endpoints no tienen campo 'success'
                return data
            else:
                raise Exception(f"Error en respuesta de API: {data.get('msg', 'Error desconocido')}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de red al acceder a {endpoint}: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON de {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado en petición a {endpoint}: {e}")
            raise

    def get_funding_rates(self, symbol: str = 'BTC') -> List[Dict[str, Any]]:
        """
        Obtener funding rates actuales
        
        Args:
            symbol: Símbolo de la criptomoneda (default: BTC)
        
        Returns:
            Lista de funding rates por exchange
        """
        try:
            logger.info(f"Obteniendo funding rates para {symbol}")
            
            endpoint = f"/api/futures/funding_rates_chart"
            params = {
                'symbol': symbol,
                'type': 'C'  # Current funding rates
            }
            
            response = self.make_request(endpoint, params)
            
            # Procesar datos
            funding_data = []
            if 'data' in response:
                for item in response['data']:
                    funding_info = {
                        'exchange': item.get('exchangeName', 'Unknown'),
                        'symbol': item.get('symbol', symbol),
                        'funding_rate': float(item.get('rate', 0)),
                        'next_funding_time': item.get('nextFundingTime'),
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    funding_data.append(funding_info)
            
            logger.info(f"Obtenidos funding rates de {len(funding_data)} exchanges para {symbol}")
            return funding_data
            
        except Exception as e:
            logger.error(f"Error al obtener funding rates: {e}")
            # Retornar datos mock en caso de error para mantener el pipeline funcionando
            return [{
                'exchange': 'mock',
                'symbol': symbol,
                'funding_rate': 0.01,
                'next_funding_time': None,
                'timestamp': datetime.utcnow().isoformat(),
                'error': str(e)
            }]

    def get_liquidation_data(self, symbol: str = 'BTC') -> Dict[str, Any]:
        """
        Obtener datos de liquidaciones
        
        Args:
            symbol: Símbolo de la criptomoneda (default: BTC)
        
        Returns:
            Datos de liquidaciones
        """
        try:
            logger.info(f"Obteniendo datos de liquidaciones para {symbol}")
            
            endpoint = f"/api/futures/liquidation_chart"
            params = {
                'symbol': symbol,
                'timeType': '1'  # 24h
            }
            
            response = self.make_request(endpoint, params)
            
            # Procesar datos
            liquidation_data = {
                'symbol': symbol,
                'total_liquidations': 0,
                'long_liquidations': 0,
                'short_liquidations': 0,
                'timestamp': datetime.utcnow().isoformat(),
                'data': response.get('data', [])
            }
            
            # Calcular totales si hay datos
            if 'data' in response and response['data']:
                for item in response['data']:
                    liquidation_data['total_liquidations'] += float(item.get('totalLiq', 0))
                    liquidation_data['long_liquidations'] += float(item.get('longLiq', 0))
                    liquidation_data['short_liquidations'] += float(item.get('shortLiq', 0))
            
            logger.info(f"Datos de liquidaciones obtenidos para {symbol}: Total ${liquidation_data['total_liquidations']:,.2f}")
            return liquidation_data
            
        except Exception as e:
            logger.error(f"Error al obtener datos de liquidaciones: {e}")
            # Retornar datos mock en caso de error
            return {
                'symbol': symbol,
                'total_liquidations': 0,
                'long_liquidations': 0,
                'short_liquidations': 0,
                'timestamp': datetime.utcnow().isoformat(),
                'data': [],
                'error': str(e)
            }

    def get_long_short_ratio(self, symbol: str = 'BTC') -> Dict[str, Any]:
        """
        Obtener ratio de long/short
        
        Args:
            symbol: Símbolo de la criptomoneda (default: BTC)
        
        Returns:
            Datos de ratio long/short
        """
        try:
            logger.info(f"Obteniendo ratio long/short para {symbol}")
            
            endpoint = f"/api/futures/longShort_chart"
            params = {
                'symbol': symbol,
                'timeType': '1'  # 24h
            }
            
            response = self.make_request(endpoint, params)
            
            # Procesar datos
            ls_data = {
                'symbol': symbol,
                'long_percentage': 50.0,
                'short_percentage': 50.0,
                'long_short_ratio': 1.0,
                'timestamp': datetime.utcnow().isoformat(),
                'data': response.get('data', [])
            }
            
            # Calcular promedios si hay datos
            if 'data' in response and response['data']:
                total_long = 0
                total_short = 0
                count = 0
                
                for item in response['data']:
                    if 'longRate' in item and 'shortRate' in item:
                        total_long += float(item['longRate'])
                        total_short += float(item['shortRate'])
                        count += 1
                
                if count > 0:
                    ls_data['long_percentage'] = total_long / count
                    ls_data['short_percentage'] = total_short / count
                    ls_data['long_short_ratio'] = ls_data['long_percentage'] / ls_data['short_percentage'] if ls_data['short_percentage'] > 0 else 1.0
            
            logger.info(f"Ratio long/short obtenido para {symbol}: {ls_data['long_percentage']:.1f}% / {ls_data['short_percentage']:.1f}%")
            return ls_data
            
        except Exception as e:
            logger.error(f"Error al obtener ratio long/short: {e}")
            # Retornar datos mock en caso de error
            return {
                'symbol': symbol,
                'long_percentage': 50.0,
                'short_percentage': 50.0,
                'long_short_ratio': 1.0,
                'timestamp': datetime.utcnow().isoformat(),
                'data': [],
                'error': str(e)
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
            logger.info("Iniciando ingesta de datos de Coinglass")
            
            # Obtener funding rates
            funding_data = self.get_funding_rates()
            
            # Obtener datos de liquidaciones
            liquidation_data = self.get_liquidation_data()
            
            # Obtener ratio long/short
            ls_data = self.get_long_short_ratio()
            
            # Crear estructura de datos completa
            coinglass_data = {
                'timestamp_utc': datetime.utcnow().isoformat(),
                'source': 'coinglass',
                'data': {
                    'funding_rates': funding_data,
                    'liquidations': liquidation_data,
                    'long_short_ratio': ls_data
                }
            }
            
            # Guardar datos
            self.save_data_to_file(coinglass_data, 'coinglass_data.json')
            
            logger.info("Ingesta de datos de Coinglass completada exitosamente")
            
        except Exception as e:
            logger.error(f"Error en la ingesta de datos de Coinglass: {e}")
            raise

def main():
    """Función principal"""
    try:
        # Crear instancia del ingester
        ingester = CoinglassDataIngester()
        
        # Ejecutar ingesta
        ingester.run_ingestion()
        
        print("✅ Ingesta de datos de Coinglass completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"❌ Error en la ingesta de datos de Coinglass: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

