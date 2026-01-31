#!/usr/bin/env python3
"""
Módulo para verificar certificados SSL de dominios
"""

import ssl
import socket
from datetime import datetime
from typing import Dict, Optional, List
import logging

class SSLChecker:
    """
    Clase para verificar certificados SSL de dominios
    """
    
    def __init__(self):
        self.logger = logging.getLogger('SSLChecker')
        self.logger.setLevel(logging.INFO)
        
    def obtener_info_ssl(self, dominio: str, puerto: int = 443, timeout: int = 10) -> Optional[Dict]:
        """
        Obtiene información del certificado SSL de un dominio
        
        Args:
            dominio: Nombre del dominio a verificar
            puerto: Puerto SSL (default 443)
            timeout: Timeout en segundos
            
        Returns:
            Diccionario con información del certificado o None si hay error
        """
        try:
            # Crear contexto SSL
            context = ssl.create_default_context()
            
            # Conectar y obtener certificado
            with socket.create_connection((dominio, puerto), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=dominio) as ssock:
                    cert = ssock.getpeercert()
                    
            # Extraer información del certificado
            info_cert = {
                'dominio': dominio,
                'version': cert.get('version'),
                'serial_number': cert.get('serialNumber'),
                'emisor': dict(cert.get('issuer', [])),
                'sujeto': dict(cert.get('subject', [])),
                'fecha_inicio': self._parse_date(cert.get('notBefore')),
                'fecha_fin': self._parse_date(cert.get('notAfter')),
                'algoritmo': cert.get('signatureAlgorithm'),
                'alternativos': cert.get('subjectAltName', []),
                'fecha_verificacion': datetime.now()
            }
            
            # Calcular días hasta expiración
            if info_cert['fecha_fin']:
                dias_hasta_expiracion = (info_cert['fecha_fin'] - datetime.now()).days
                info_cert['dias_hasta_expiracion'] = dias_hasta_expiracion
            else:
                info_cert['dias_hasta_expiracion'] = None
                
            # Verificar si el certificado es válido para el dominio
            info_cert['dominio_valido'] = self._verificar_dominio(dominio, cert)
            
            self.logger.info(f"SSL verificado para {dominio}: {info_cert['dias_hasta_expiracion']} días hasta expiración")
            return info_cert
            
        except Exception as e:
            self.logger.error(f"Error al verificar SSL para {dominio}: {str(e)}")
            return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Convierte fecha del certificado a datetime
        
        Args:
            date_str: Fecha en formato del certificado
            
        Returns:
            Objeto datetime o None
        """
        if not date_str:
            return None
            
        try:
            # Formatos comunes de fechas en certificados
            formatos = [
                '%b %d %H:%M:%S %Y %Z',  # Jan 1 00:00:00 2023 GMT
                '%Y%m%d%H%M%SZ',         # 20230101000000Z
                '%Y-%m-%d %H:%M:%S',     # 2023-01-01 00:00:00
            ]
            
            for fmt in formatos:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
                    
            return None
            
        except Exception:
            return None
    
    def _verificar_dominio(self, dominio: str, cert: Dict) -> bool:
        """
        Verifica si el certificado es válido para el dominio
        
        Args:
            dominio: Dominio a verificar
            cert: Certificado SSL
            
        Returns:
            True si el dominio es válido, False en caso contrario
        """
        try:
            # Obtener CN del sujeto
            subject = dict(cert.get('subject', []))
            cn = subject.get('commonName', '')
            
            # Verificar dominio principal
            if cn.lower() == dominio.lower():
                return True
                
            # Verificar wildcard
            if cn.startswith('*.'):
                base_domain = cn[2:].lower()
                if dominio.lower().endswith(base_domain):
                    return True
                    
            # Verificar SAN (Subject Alternative Names)
            san = cert.get('subjectAltName', [])
            for entry in san:
                if entry[0] == 'DNS' and entry[1].lower() == dominio.lower():
                    return True
                if entry[0] == 'DNS' and entry[1].startswith('*.'):
                    base_domain = entry[1][2:].lower()
                    if dominio.lower().endswith(base_domain):
                        return True
                        
            return False
            
        except Exception:
            return False
    
    def verificar_multiples_dominios(self, dominios: List[str]) -> List[Dict]:
        """
        Verifica certificados SSL de múltiples dominios
        
        Args:
            dominios: Lista de dominios a verificar
            
        Returns:
            Lista de diccionarios con información de certificados
        """
        resultados = []
        
        for dominio in dominios:
            info = self.obtener_info_ssl(dominio)
            if info:
                resultados.append(info)
                
        self.logger.info(f"Se verificaron {len(resultados)} certificados SSL exitosamente")
        return resultados
    
    def obtener_alertas_ssl(self, info_cert: Dict, dias_critico: int = 30, dias_advertencia: int = 60) -> Dict:
        """
        Genera alertas basadas en la información del certificado SSL
        
        Args:
            info_cert: Información del certificado
            dias_critico: Días para alerta crítica
            dias_advertencia: Días para advertencia
            
        Returns:
            Diccionario con alertas
        """
        alertas = {
            'criticas': [],
            'advertencias': [],
            'informativas': []
        }
        
        if not info_cert:
            return alertas
            
        dias = info_cert.get('dias_hasta_expiracion')
        
        # Alerta de expiración
        if dias is not None:
            if dias <= dias_critico:
                alertas['criticas'].append(f"🚨 El certificado expira en {dias} días")
            elif dias <= dias_advertencia:
                alertas['advertencias'].append(f"⚠️ El certificado expira en {dias} días")
            else:
                alertas['informativas'].append(f"✅ El certificado es válido por {dias} días")
        
        # Alerta de dominio inválido
        if not info_cert.get('dominio_valido', False):
            alertas['criticas'].append("🚨 El certificado no es válido para este dominio")
        
        # Alerta de certificado auto-firmado
        emisor = info_cert.get('emisor', {})
        if emisor.get('organizationName') == emisor.get('commonName'):
            alertas['advertencias'].append("⚠️ Posible certificado auto-firmado")
            
        return alertas
