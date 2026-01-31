import pandas as pd
import logging
from datetime import datetime
from typing import List, Dict, Optional
from agente_lector import AgenteLector
from agente_decisor import AgenteDecisor

class AgentePrincipal:
    """
    Agente Principal: Coordina al Agente Lector y Agente Decisor
    """
    
    def __init__(self, config_email: Optional[Dict] = None):
        self.logger = logging.getLogger('AgentePrincipal')
        self.logger.setLevel(logging.INFO)
        
        # Configurar logging
        self._configurar_logging()
        
        # Inicializar agentes
        self.agente_lector = AgenteLector()
        self.agente_decisor = AgenteDecisor(config_email)
        
        self.logger.info("Agente Principal inicializado")
    
    def _configurar_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sistema_dominios.log'),
                logging.StreamHandler()
            ]
        )
    
    def monitorear_dominios(self, lista_dominios: List[str], 
                          destinatarios_correo: List[str] = None, forzar_envio_correo: bool = False) -> Dict:
        """
        Ejecuta el monitoreo completo de dominios
        
        Args:
            lista_dominios: Lista de dominios a monitorear
            destinatarios_correo: Lista de correos para notificaciones
            forzar_envio_correo: Si True, envía correo siempre que haya configuración
            
        Returns:
            Diccionario con resultados completos del monitoreo
        """
        self.logger.info(f"Iniciando monitoreo de {len(lista_dominios)} dominios")
        
        resultados = {
            'timestamp': datetime.now(),
            'dominios_procesados': 0,
            'dominios_error': 0,
            'decisiones': None,
            'correo_enviado': False,
            'log_generado': False,
            'dataframe_completo': None,
            'errores': []
        }
        
        try:
            # Paso 1: Agente Lector obtiene información
            self.logger.info("Paso 1: Obteniendo información de dominios...")
            df_completo = self.agente_lector.leer_dominios(lista_dominios)
            resultados['dataframe_completo'] = df_completo
            resultados['dominios_procesados'] = len(df_completo)
            resultados['dominios_error'] = len(lista_dominios) - len(df_completo)
            
            if df_completo.empty:
                self.logger.warning("No se pudo obtener información de ningún dominio")
                return resultados
            
            # Paso 2: Agente Decisor evalúa y toma decisiones
            self.logger.info("Paso 2: Evaluando decisiones...")
            decisiones = self.agente_decisor.evaluar_dominios(df_completo, forzar_envio_correo)
            resultados['decisiones'] = decisiones
            
            # Paso 3: Ejecutar acciones según decisiones
            self.logger.info("Paso 3: Ejecutando acciones...")
            
            # Generar log si es necesario
            if decisiones['generar_log']:
                log_resultado = self.agente_decisor.generar_log(decisiones)
                resultados['log_generado'] = log_resultado
            
            # Enviar correo si es necesario y hay destinatarios
            if decisiones['enviar_correo'] and destinatarios_correo:
                correo_resultado = self.agente_decisor.enviar_correo(decisiones, destinatarios_correo)
                resultados['correo_enviado'] = correo_resultado
            elif decisiones['enviar_correo'] and not destinatarios_correo:
                self.logger.warning("Se requiere enviar correo pero no hay destinatarios configurados")
            
            self.logger.info("Monitoreo completado exitosamente")
            
        except Exception as e:
            error_msg = f"Error en monitoreo: {str(e)}"
            self.logger.error(error_msg)
            resultados['errores'].append(error_msg)
        
        return resultados
    
    def obtener_reporte_pandas(self, lista_dominios: List[str]) -> pd.DataFrame:
        """
        Obtiene un reporte visual en pandas de los dominios
        
        Args:
            lista_dominios: Lista de dominios a consultar
            
        Returns:
            DataFrame con información formateada para visualización
        """
        self.logger.info("Generando reporte pandas...")
        
        df = self.agente_lector.leer_dominios(lista_dominios)
        
        if df.empty:
            return df
        
        # Agregar columnas de análisis
        df['estado_alerta'] = df['dias_hasta_vencimiento'].apply(
            lambda x: 'CRÍTICO' if x <= 30 else ('ADVERTENCIA' if x <= 50 else 'NORMAL')
        )
        
        df['prioridad'] = df['dias_hasta_vencimiento'].apply(
            lambda x: 1 if x <= 30 else (2 if x <= 50 else 3)
        )
        
        # Ordenar por prioridad
        df = df.sort_values('prioridad')
        
        return df
    
    def mostrar_resumen(self, resultados: Dict):
        """
        Muestra un resumen de los resultados del monitoreo
        
        Args:
            resultados: Diccionario con resultados del monitoreo
        """
        print("\n" + "="*60)
        print("RESUMEN DE MONITOREO DE DOMINIOS")
        print("="*60)
        print(f"Fecha y hora: {resultados['timestamp']}")
        print(f"Dominios procesados: {resultados['dominios_procesados']}")
        print(f"Dominios con error: {resultados['dominios_error']}")
        
        if resultados['decisiones']:
            dec = resultados['decisiones']
            print(f"Dominios críticos (≤30 días): {dec['criticos_count']}")
            print(f"Dominios en advertencia (31-50 días): {dec['advertencia_count']}")
            print(f"Log generado: {'Sí' if resultados['log_generado'] else 'No'}")
            print(f"Correo enviado: {'Sí' if resultados['correo_enviado'] else 'No'}")
        
        if resultados['errores']:
            print("\nERRORES:")
            for error in resultados['errores']:
                print(f"- {error}")
        
        print("="*60)
    
    def ejecutar_monitoreo_interactivo(self):
        """
        Ejecuta el monitoreo en modo interactivo
        """
        print("=== SISTEMA DE MONITOREO DE DOMINIOS ===")
        
        # Solicitar dominios
        entrada = input("Ingrese los dominios a monitorear (separados por coma): ")
        dominios = [d.strip() for d in entrada.split(',') if d.strip()]
        
        if not dominios:
            print("No se ingresaron dominios válidos")
            return
        
        # Solicitar correos (opcional)
        entrada_correos = input("Ingrese correos para notificaciones (separados por coma, o presione Enter para omitir): ")
        destinatarios = [c.strip() for c in entrada_correos.split(',') if c.strip()] if entrada_correos else []
        
        # Ejecutar monitoreo
        resultados = self.monitorear_dominios(dominios, destinatarios)
        
        # Mostrar resumen
        self.mostrar_resumen(resultados)
        
        # Mostrar reporte pandas si hay datos
        if resultados['dataframe_completo'] is not None and not resultados['dataframe_completo'].empty:
            print("\nREPORTE DETALLADO:")
            print(resultados['dataframe_completo'].to_string())
