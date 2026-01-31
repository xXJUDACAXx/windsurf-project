import whois
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Optional

class AgenteLector:
    """
    Agente Lector: Encargado de leer y obtener información sobre dominios
    """
    
    def __init__(self):
        self.logger = logging.getLogger('AgenteLector')
        self.logger.setLevel(logging.INFO)
        
    def obtener_info_dominio(self, dominio: str) -> Optional[Dict]:
        """
        Obtiene información completa de un dominio
        
        Args:
            dominio: Nombre del dominio a consultar
            
        Returns:
            Diccionario con información del dominio o None si hay error
        """
        try:
            w = whois.whois(dominio)
            
            # Manejar casos donde expiration_date puede ser lista o fecha única
            expiration_date = w.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
                
            # Calcular días hasta vencimiento
            if expiration_date:
                # Asegurar que ambas fechas sean timezone-aware o naive
                now = datetime.now()
                if expiration_date.tzinfo is not None:
                    now = datetime.now(expiration_date.tzinfo)
                dias_hasta_vencimiento = (expiration_date - now).days
            else:
                dias_hasta_vencimiento = None
                
            info = {
                'dominio': dominio,
                'fecha_expiracion': expiration_date,
                'dias_hasta_vencimiento': dias_hasta_vencimiento,
                'registrar': w.registrar,
                'estado': w.status,
                'fecha_consulta': datetime.now()
            }
            
            self.logger.info(f"Información obtenida para {dominio}: {dias_hasta_vencimiento} días hasta vencimiento")
            return info
            
        except Exception as e:
            self.logger.error(f"Error al obtener información del dominio {dominio}: {str(e)}")
            return None
    
    def leer_dominios(self, lista_dominios: List[str]) -> pd.DataFrame:
        """
        Lee información de múltiples dominios y devuelve un DataFrame
        
        Args:
            lista_dominios: Lista de dominios a consultar
            
        Returns:
            DataFrame con información de todos los dominios
        """
        resultados = []
        
        for dominio in lista_dominios:
            info = self.obtener_info_dominio(dominio)
            if info:
                resultados.append(info)
                
        df = pd.DataFrame(resultados)
        self.logger.info(f"Se procesaron {len(resultados)} dominios exitosamente")
        
        return df
    
    def dominios_por_vencer(self, df: pd.DataFrame, dias: int = 50) -> pd.DataFrame:
        """
        Filtra dominios que vencerán en X días o menos
        
        Args:
            df: DataFrame con información de dominios
            dias: Número de días para filtrar
            
        Returns:
            DataFrame filtrado con dominios por vencer
        """
        if df.empty:
            return df
            
        filtrado = df[df['dias_hasta_vencimiento'] <= dias].copy()
        filtrado = filtrado.sort_values('dias_hasta_vencimiento')
        
        self.logger.info(f"Se encontraron {len(filtrado)} dominios por vencer en {dias} días o menos")
        return filtrado
    
    def exportar_dataframe(self, df: pd.DataFrame, archivo: str = 'reporte_dominios.csv'):
        """
        Exporta el DataFrame a un archivo CSV
        
        Args:
            df: DataFrame a exportar
            archivo: Nombre del archivo de salida
        """
        try:
            df.to_csv(archivo, index=False, date_format='%Y-%m-%d %H:%M:%S')
            self.logger.info(f"DataFrame exportado a {archivo}")
        except Exception as e:
            self.logger.error(f"Error al exportar DataFrame: {str(e)}")
