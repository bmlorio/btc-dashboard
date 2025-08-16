#!/usr/bin/env python3
"""
Script de ingesta de datos de St. Louis FRED
Obtiene datos macroeconómicos como DXY, tasas de interés, etc.
"""

import os
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Añadir el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fredapi import Fred
from config.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FredDataIngester:
    def __init__(self):
        """Inicializar el cliente de FRED"""
        try:
            if Config.FRED_API_KEY:
                self.fred = Fred(api_key=Config.FRED_API_KEY)
                logger.info("Cliente de FRED inicializado con API key")
            else:
                logger.warning("No se encontró API key de FRED, usando datos mock")
                self.fred = None
        except Exception as e:
            logger.error(f"Error al inicializar cliente de FRED: {e}")
            self.fred = None

    def get_series_data(self, series_id: str, series_name: str, limit: int = 30) -> Dict[str, Any]:
        """
        Obtener datos de una serie específica de FRED
        
        Args:
            series_id: ID de la serie en FRED
            series_name: Nombre descriptivo de la serie
            limit: Número de observaciones a obtener
        
        Returns:
            Diccionario con datos de la serie
        """
        try:
            if not self.fred:
                # Retornar datos mock si no hay cliente FRED
                return {
                    'series_id': series_id,
                    'series_name': series_name,
                    'latest_value': 100.0,
                    'latest_date': datetime.now().strftime('%Y-%m-%d'),
                    'data': [],
                    'error': 'No FRED API key available'
                }
            
            logger.info(f"Obteniendo datos de serie {series_id} ({series_name})")
            
            # Obtener datos de la serie
            data = self.fred.get_series(series_id, limit=limit)
            
            # Convertir a formato JSON serializable
            series_data = []
            for date, value in data.items():
                if not pd.isna(value):  # Filtrar valores NaN
                    series_data.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'value': float(value)
                    })
            
            # Obtener el valor más reciente
            latest_value = float(data.dropna().iloc[-1]) if not data.dropna().empty else None
            latest_date = data.dropna().index[-1].strftime('%Y-%m-%d') if not data.dropna().empty else None
            
            result = {
                'series_id': series_id,
                'series_name': series_name,
                'latest_value': latest_value,
                'latest_date': latest_date,
                'data': series_data,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Datos obtenidos para {series_name}: último valor {latest_value} en {latest_date}")
            return result
            
        except Exception as e:
            logger.error(f"Error al obtener datos de serie {series_id}: {e}")
            # Retornar datos mock en caso de error
            return {
                'series_id': series_id,
                'series_name': series_name,
                'latest_value': 100.0,
                'latest_date': datetime.now().strftime('%Y-%m-%d'),
                'data': [],
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

    def get_dxy_data(self) -> Dict[str, Any]:
        """
        Obtener datos del índice del dólar (DXY)
        
        Returns:
            Datos del DXY
        """
        return self.get_series_data('DTWEXBGS', 'US Dollar Index (DXY)')

    def get_interest_rates_data(self) -> Dict[str, Any]:
        """
        Obtener datos de tasas de interés
        
        Returns:
            Datos de tasas de interés
        """
        return self.get_series_data('FEDFUNDS', 'Federal Funds Rate')

    def get_treasury_yield_data(self) -> Dict[str, Any]:
        """
        Obtener datos de rendimiento del tesoro a 10 años
        
        Returns:
            Datos de rendimiento del tesoro
        """
        return self.get_series_data('GS10', '10-Year Treasury Constant Maturity Rate')

    def get_inflation_data(self) -> Dict[str, Any]:
        """
        Obtener datos de inflación (CPI)
        
        Returns:
            Datos de inflación
        """
        return self.get_series_data('CPIAUCSL', 'Consumer Price Index for All Urban Consumers')

    def get_unemployment_data(self) -> Dict[str, Any]:
        """
        Obtener datos de desempleo
        
        Returns:
            Datos de desempleo
        """
        return self.get_series_data('UNRATE', 'Unemployment Rate')

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
            logger.info("Iniciando ingesta de datos de FRED")
            
            # Obtener diferentes series de datos macroeconómicos
            dxy_data = self.get_dxy_data()
            interest_rates_data = self.get_interest_rates_data()
            treasury_yield_data = self.get_treasury_yield_data()
            inflation_data = self.get_inflation_data()
            unemployment_data = self.get_unemployment_data()
            
            # Crear estructura de datos completa
            fred_data = {
                'timestamp_utc': datetime.utcnow().isoformat(),
                'source': 'fred',
                'data': {
                    'dxy': dxy_data,
                    'federal_funds_rate': interest_rates_data,
                    'treasury_10y': treasury_yield_data,
                    'cpi': inflation_data,
                    'unemployment_rate': unemployment_data
                }
            }
            
            # Guardar datos
            self.save_data_to_file(fred_data, 'fred_data.json')
            
            logger.info("Ingesta de datos de FRED completada exitosamente")
            
        except Exception as e:
            logger.error(f"Error en la ingesta de datos de FRED: {e}")
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
        ingester = FredDataIngester()
        
        # Ejecutar ingesta
        ingester.run_ingestion()
        
        print("✅ Ingesta de datos de FRED completada exitosamente")
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"❌ Error en la ingesta de datos de FRED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

