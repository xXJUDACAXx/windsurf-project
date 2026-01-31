import smtplib
import pandas as pd
from datetime import datetime
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Optional

class AgenteDecisor:
    """
    Agente Decisor: Encargado de tomar decisiones sobre notificaciones
    """
    
    def __init__(self, config_email: Optional[Dict] = None):
        self.logger = logging.getLogger('AgenteDecisor')
        self.logger.setLevel(logging.INFO)
        self.config_email = config_email or {}
        
    def evaluar_dominios(self, df: pd.DataFrame, forzar_envio: bool = False) -> Dict:
        """
        Evalúa los dominios y decide qué acción tomar
        
        Args:
            df: DataFrame con información de dominios
            forzar_envio: Si True, envía correo siempre que haya configuración
            
        Returns:
            Diccionario con decisiones tomadas
        """
        if df.empty:
            return {
                'enviar_correo': False,
                'generar_log': False,
                'dominios_criticos': [],
                'dominios_advertencia': [],
                'mensaje': 'No hay dominios para evaluar'
            }
        
        # Filtrar dominios por vencer en 30 días o menos (críticos)
        criticos = df[df['dias_hasta_vencimiento'] <= 30].copy()
        
        # Filtrar dominios por vencer en 50 días o menos (advertencia)
        advertencia = df[(df['dias_hasta_vencimiento'] > 30) & 
                        (df['dias_hasta_vencimiento'] <= 50)].copy()
        
        decisiones = {
            'enviar_correo': len(criticos) > 0 or forzar_envio,  # Forzar envío si se solicita
            'generar_log': len(criticos) > 0,
            'dominios_criticos': criticos.to_dict('records'),
            'dominios_advertencia': advertencia.to_dict('records'),
            'total_evaluados': len(df),
            'criticos_count': len(criticos),
            'advertencia_count': len(advertencia)
        }
        
        self.logger.info(f"Evaluación completada: {len(criticos)} críticos, {len(advertencia)} advertencia")
        return decisiones
    
    def generar_mensaje_correo(self, decisiones: Dict) -> str:
        """
        Genera el contenido del correo electrónico
        
        Args:
            decisiones: Diccionario con decisiones del agente
            
        Returns:
            String con el contenido del correo
        """
        mensaje = f"""
REPORTE DE DOMINIOS POR VENCER
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

=== DOMINIOS CRÍTICOS (Vencen en 30 días o menos) ===
"""
        
        if decisiones['dominios_criticos']:
            for dominio in decisiones['dominios_criticos']:
                mensaje += f"""
Dominio: {dominio['dominio']}
Días hasta vencimiento: {dominio['dias_hasta_vencimiento']}
Fecha de expiración: {dominio['fecha_expiracion']}
Registrar: {dominio.get('registrar', 'N/A')}
----------------------------------------
"""
        else:
            mensaje += "\nNo hay dominios críticos.\n"
        
        mensaje += f"""
=== DOMINIOS EN ADVERTENCIA (Vencen entre 31-50 días) ===
"""
        
        if decisiones['dominios_advertencia']:
            for dominio in decisiones['dominios_advertencia']:
                mensaje += f"""
Dominio: {dominio['dominio']}
Días hasta vencimiento: {dominio['dias_hasta_vencimiento']}
Fecha de expiración: {dominio['fecha_expiracion']}
----------------------------------------
"""
        else:
            mensaje += "\nNo hay dominios en advertencia.\n"
        
        mensaje += f"""
=== RESUMEN ===
Total dominios evaluados: {decisiones['total_evaluados']}
Dominios críticos: {decisiones['criticos_count']}
Dominios en advertencia: {decisiones['advertencia_count']}

Acción recomendada: {'RENOVAR URGENTEMENTE' if decisiones['criticos_count'] > 0 else 'Monitoreo continuo'}
"""
        
        return mensaje
    
    def enviar_correo(self, decisiones: Dict, destinatarios: List[str]) -> bool:
        """
        Envía correo electrónico con las alertas
        
        Args:
            decisiones: Diccionario con decisiones
            destinatarios: Lista de correos destinatarios
            
        Returns:
            True si se envió correctamente, False en caso contrario
        """
        if not self.config_email:
            self.logger.error("No hay configuración de correo")
            return False
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config_email.get('remite', 'sistema@dominio.com')
            msg['To'] = ', '.join(destinatarios)
            
            # Asunto dinámico según contenido
            if decisiones['criticos_count'] > 0:
                msg['Subject'] = f"ALERTA: {decisiones['criticos_count']} dominios por vencer críticamente"
            else:
                msg['Subject'] = f"Reporte de Monitoreo de Dominios - {decisiones['total_evaluados']} dominios revisados"
            
            msg.attach(MIMEText(self.generar_mensaje_correo(decisiones), 'plain'))
            
            self.logger.info(f"Conectando a servidor SMTP: {self.config_email['smtp_server']}:{self.config_email['smtp_port']}")
            server = smtplib.SMTP(self.config_email['smtp_server'], self.config_email['smtp_port'])
            server.starttls()
            self.logger.info(f"Iniciando sesión como: {self.config_email['usuario']}")
            server.login(self.config_email['usuario'], self.config_email['contraseña'])
            
            text = msg.as_string()
            server.sendmail(msg['From'], destinatarios, text)
            server.quit()
            
            self.logger.info(f"Correo enviado exitosamente a {len(destinatarios)} destinatarios")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al enviar correo: {str(e)}")
            return False
    
    def generar_log(self, decisiones: Dict, archivo_log: str = 'dominios_log.txt') -> bool:
        """
        Genera archivo de log con las alertas
        
        Args:
            decisiones: Diccionario con decisiones
            archivo_log: Nombre del archivo de log
            
        Returns:
            True si se generó correctamente, False en caso contrario
        """
        if not decisiones['generar_log']:
            self.logger.info("No se requiere generar log")
            return True
            
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(archivo_log, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*60}\n")
                f.write(f"LOG DE ALERTAS - {timestamp}\n")
                f.write(f"{'='*60}\n")
                
                if decisiones['dominios_criticos']:
                    f.write("\nDOMINIOS CRÍTICOS:\n")
                    for dominio in decisiones['dominios_criticos']:
                        f.write(f"- {dominio['dominio']}: {dominio['dias_hasta_vencimiento']} días\n")
                
                if decisiones['dominios_advertencia']:
                    f.write("\nDOMINIOS EN ADVERTENCIA:\n")
                    for dominio in decisiones['dominios_advertencia']:
                        f.write(f"- {dominio['dominio']}: {dominio['dias_hasta_vencimiento']} días\n")
                
                f.write(f"\nResumen: {decisiones['criticos_count']} críticos, {decisiones['advertencia_count']} advertencia\n")
                f.write(f"{'='*60}\n")
            
            self.logger.info(f"Log generado en {archivo_log}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al generar log: {str(e)}")
            return False
