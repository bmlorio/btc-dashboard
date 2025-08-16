#!/usr/bin/env python3
"""
Script para subir archivos a Cloudflare R2 (S3 compatible)
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime
from typing import Optional

# Añadir el directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from config.config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class R2Uploader:
    def __init__(self):
        """Inicializar el cliente de S3 para Cloudflare R2"""
        try:
            # Validar configuración
            if not all([Config.R2_ACCESS_KEY_ID, Config.R2_SECRET_ACCESS_KEY, 
                       Config.R2_ENDPOINT_URL, Config.R2_BUCKET_NAME]):
                raise ValueError("Faltan credenciales de R2. Verifica las variables de entorno.")
            
            # Crear cliente S3 para R2
            self.s3_client = boto3.client(
                's3',
                endpoint_url=Config.R2_ENDPOINT_URL,
                aws_access_key_id=Config.R2_ACCESS_KEY_ID,
                aws_secret_access_key=Config.R2_SECRET_ACCESS_KEY,
                region_name='auto'  # R2 usa 'auto' como región
            )
            
            self.bucket_name = Config.R2_BUCKET_NAME
            logger.info(f"Cliente R2 inicializado para bucket: {self.bucket_name}")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente R2: {e}")
            raise

    def upload_file(self, local_file_path: str, remote_key: Optional[str] = None, 
                   content_type: Optional[str] = None) -> bool:
        """
        Subir un archivo a R2
        
        Args:
            local_file_path: Ruta local del archivo
            remote_key: Clave/nombre del archivo en R2 (opcional, usa el nombre del archivo local)
            content_type: Tipo de contenido MIME (opcional, se detecta automáticamente)
        
        Returns:
            True si la subida fue exitosa, False en caso contrario
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(local_file_path):
                logger.error(f"El archivo {local_file_path} no existe")
                return False
            
            # Determinar la clave remota si no se proporciona
            if remote_key is None:
                remote_key = os.path.basename(local_file_path)
            
            # Detectar tipo de contenido si no se proporciona
            if content_type is None:
                if local_file_path.endswith('.json'):
                    content_type = 'application/json'
                elif local_file_path.endswith('.csv'):
                    content_type = 'text/csv'
                elif local_file_path.endswith('.parquet'):
                    content_type = 'application/octet-stream'
                else:
                    content_type = 'application/octet-stream'
            
            logger.info(f"Subiendo {local_file_path} a {remote_key}")
            
            # Preparar metadatos
            metadata = {
                'uploaded_at': datetime.utcnow().isoformat(),
                'source': 'btc-dashboard-backend'
            }
            
            # Subir archivo
            with open(local_file_path, 'rb') as file:
                self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    remote_key,
                    ExtraArgs={
                        'ContentType': content_type,
                        'Metadata': metadata
                    }
                )
            
            logger.info(f"✅ Archivo subido exitosamente: {remote_key}")
            return True
            
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {local_file_path}")
            return False
        except NoCredentialsError:
            logger.error("Credenciales de R2 no válidas")
            return False
        except ClientError as e:
            logger.error(f"Error del cliente S3/R2: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al subir archivo: {e}")
            return False

    def upload_json_data(self, data: dict, remote_key: str) -> bool:
        """
        Subir datos JSON directamente a R2
        
        Args:
            data: Datos a subir en formato dict
            remote_key: Clave/nombre del archivo en R2
        
        Returns:
            True si la subida fue exitosa, False en caso contrario
        """
        try:
            logger.info(f"Subiendo datos JSON a {remote_key}")
            
            # Convertir datos a JSON
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Preparar metadatos
            metadata = {
                'uploaded_at': datetime.utcnow().isoformat(),
                'source': 'btc-dashboard-backend',
                'content_type': 'application/json'
            }
            
            # Subir datos
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=remote_key,
                Body=json_data.encode('utf-8'),
                ContentType='application/json',
                Metadata=metadata
            )
            
            logger.info(f"✅ Datos JSON subidos exitosamente: {remote_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Error del cliente S3/R2: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al subir datos JSON: {e}")
            return False

    def list_files(self, prefix: str = '') -> list:
        """
        Listar archivos en el bucket
        
        Args:
            prefix: Prefijo para filtrar archivos
        
        Returns:
            Lista de archivos
        """
        try:
            logger.info(f"Listando archivos en bucket {self.bucket_name}")
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'etag': obj['ETag']
                    })
            
            logger.info(f"Encontrados {len(files)} archivos")
            return files
            
        except ClientError as e:
            logger.error(f"Error al listar archivos: {e}")
            return []
        except Exception as e:
            logger.error(f"Error inesperado al listar archivos: {e}")
            return []

    def delete_file(self, remote_key: str) -> bool:
        """
        Eliminar un archivo de R2
        
        Args:
            remote_key: Clave del archivo a eliminar
        
        Returns:
            True si la eliminación fue exitosa, False en caso contrario
        """
        try:
            logger.info(f"Eliminando archivo: {remote_key}")
            
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=remote_key
            )
            
            logger.info(f"✅ Archivo eliminado exitosamente: {remote_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Error al eliminar archivo: {e}")
            return False
        except Exception as e:
            logger.error(f"Error inesperado al eliminar archivo: {e}")
            return False

    def upload_all_data_files(self) -> bool:
        """
        Subir todos los archivos de datos del directorio local
        
        Returns:
            True si todas las subidas fueron exitosas, False en caso contrario
        """
        try:
            data_dir = Config.DATA_DIR
            
            if not os.path.exists(data_dir):
                logger.warning(f"Directorio de datos {data_dir} no existe")
                return True
            
            success_count = 0
            total_count = 0
            
            # Buscar archivos JSON en el directorio de datos
            for filename in os.listdir(data_dir):
                if filename.endswith('.json'):
                    total_count += 1
                    local_path = os.path.join(data_dir, filename)
                    
                    if self.upload_file(local_path):
                        success_count += 1
                    else:
                        logger.error(f"Falló la subida de {filename}")
            
            logger.info(f"Subidas completadas: {success_count}/{total_count}")
            return success_count == total_count
            
        except Exception as e:
            logger.error(f"Error al subir archivos de datos: {e}")
            return False

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Subir archivos a Cloudflare R2')
    parser.add_argument('--file', '-f', help='Archivo específico a subir')
    parser.add_argument('--key', '-k', help='Clave remota para el archivo')
    parser.add_argument('--all', '-a', action='store_true', help='Subir todos los archivos de datos')
    parser.add_argument('--list', '-l', action='store_true', help='Listar archivos en el bucket')
    
    args = parser.parse_args()
    
    try:
        # Validar configuración
        Config.validate_config()
        
        # Crear instancia del uploader
        uploader = R2Uploader()
        
        if args.list:
            # Listar archivos
            files = uploader.list_files()
            print(f"\n📁 Archivos en bucket {uploader.bucket_name}:")
            for file_info in files:
                print(f"  - {file_info['key']} ({file_info['size']} bytes, {file_info['last_modified']})")
            
        elif args.all:
            # Subir todos los archivos de datos
            if uploader.upload_all_data_files():
                print("✅ Todos los archivos de datos subidos exitosamente")
            else:
                print("❌ Error al subir algunos archivos de datos")
                sys.exit(1)
                
        elif args.file:
            # Subir archivo específico
            if uploader.upload_file(args.file, args.key):
                print(f"✅ Archivo {args.file} subido exitosamente")
            else:
                print(f"❌ Error al subir archivo {args.file}")
                sys.exit(1)
        else:
            parser.print_help()
        
    except Exception as e:
        logger.error(f"Error en main: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

