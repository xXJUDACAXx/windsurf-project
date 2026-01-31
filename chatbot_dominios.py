#!/usr/bin/env python3
"""
Asistente de Dominios - Sistema simple de consulta de monitoreo
"""

import pandas as pd
from typing import Dict, List, Optional
import logging
from datetime import datetime
import json

from ssl_checker import SSLChecker
from agente_lector import AgenteLector

class AsistenteDominios:
    """
    Asistente simple para consultas sobre resultados de monitoreo de dominios
    """
    
    def __init__(self):
        """
        Inicializar el asistente sin dependencia de APIs externas
        """
        # Configurar logger
        self.logger = logging.getLogger('AsistenteDominios')
        self.logger.setLevel(logging.INFO)
        
        # Herramientas de consulta
        self.ssl_checker = SSLChecker()
        self.agente_lector = AgenteLector()
        
        # Contexto del sistema para el asistente
        self.system_context = """
        Eres un asistente experto en análisis de dominios web y certificados SSL. 
        Tu función es ayudar a interpretar los resultados del monitoreo de dominios.
        
        Puedes:
        - Analizar información de dominios (fechas de expiración, registradores, etc.)
        - Interpretar estado de certificados SSL (fechas de validez, emisores, seguridad)
        - Proporcionar recomendaciones basadas en los datos disponibles
        - Alertar sobre problemas detectados en el monitoreo
        
        Responde en español de manera clara y profesional. Basa tus respuestas
        únicamente en los datos de monitoreo proporcionados.
        """
    
    def generar_respuesta_contexto(self, pregunta: str, contexto_dominios: Optional[Dict] = None) -> str:
        """
        Genera respuesta basada en el contexto de monitoreo disponible
        
        Args:
            pregunta: Pregunta del usuario
            contexto_dominios: Información de dominios relevante
            
        Returns:
            Respuesta basada en el análisis de datos
        """
        try:
            # Analizar la pregunta y generar respuesta basada en contexto
            respuesta = self._analizar_pregunta_contexto(pregunta, contexto_dominios)
            
            self.logger.info(f"Respuesta generada basada en contexto para: {pregunta[:50]}...")
            return respuesta
            
        except Exception as e:
            self.logger.error(f"ERROR: Falló en generar_respuesta_contexto: {str(e)}")
            return f"Lo siento, tuve un error al procesar tu pregunta: {str(e)}"
    
    def _analizar_pregunta_contexto(self, pregunta: str, contexto_dominios: Optional[Dict] = None) -> str:
        """
        Analiza la pregunta y genera respuesta basada en el contexto disponible
        """
        pregunta_lower = pregunta.lower()
        
        # Si no hay contexto de monitoreo
        if not contexto_dominios:
            return self._respuesta_sin_monitoreo(pregunta_lower)
        
        # Analizar según el tipo de pregunta
        if any(palabra in pregunta_lower for palabra in ['vencer', 'expirar', 'caducar']):
            return self._analizar_vencimientos(contexto_dominios)
        
        elif any(palabra in pregunta_lower for palabra in ['ssl', 'certificado', 'seguridad']):
            return self._analizar_certificados_ssl(contexto_dominios)
        
        elif any(palabra in pregunta_lower for palabra in ['crítico', 'alerta', 'peligro']):
            return self._analizar_alertas(contexto_dominios)
        
        elif any(palabra in pregunta_lower for palabra in ['resumen', 'general', 'estado']):
            return self._analizar_resumen_general(contexto_dominios)
        
        else:
            return self._respuesta_general(contexto_dominios, pregunta)
    
    def _respuesta_sin_monitoreo(self, pregunta: str) -> str:
        """
        Respuesta cuando no hay datos de monitoreo
        """
        if any(palabra in pregunta for palabra in ['qué puedes', 'funcionas', 'haces']):
            return ("Soy un asistente de análisis de dominios web. Puedo ayudarte a interpretar los resultados "
                   "del monitoreo de dominios, analizar fechas de vencimiento, estado de certificados SSL "
                   "y proporcionar recomendaciones basadas en los datos disponibles. "
                   "Para comenzar, ejecuta un monitoreo de dominios desde el panel principal.")
        
        return ("Para poder darte información específica, primero necesito que ejecutes un monitoreo "
               "de dominios desde el panel principal. Una vez que tengas datos de monitoreo, "
               "podré analizarlos y responder tus preguntas sobre vencimientos, certificados SSL "
               "y estado general de tus dominios.")
    
    def _analizar_vencimientos(self, contexto: Dict) -> str:
        """
        Analiza fechas de vencimiento de dominios
        """
        if 'dataframe_completo' in contexto:
            df = contexto['dataframe_completo']
            
            if df.empty:
                return "No se encontraron datos de dominios para analizar vencimientos."
            
            # Dominios por vencer en 30 días
            criticos = df[df['dias_hasta_vencimiento'] <= 30]
            # Dominios por vencer en 60 días
            advertencia = df[(df['dias_hasta_vencimiento'] > 30) & (df['dias_hasta_vencimiento'] <= 60)]
            
            respuesta = f"Análisis de vencimientos:\n\n"
            
            if not criticos.empty:
                respuesta += f"🚨 **Dominios por vencer en 30 días ({len(criticos)}):**\n"
                for _, row in criticos.iterrows():
                    respuesta += f"• {row['dominio']}: {row['dias_hasta_vencimiento']} días (vence: {row['fecha_expiracion']})\n"
                respuesta += "\n"
            
            if not advertencia.empty:
                respuesta += f"⚠️ **Dominios por vencer en 60 días ({len(advertencia)}):**\n"
                for _, row in advertencia.iterrows():
                    respuesta += f"• {row['dominio']}: {row['dias_hasta_vencimiento']} días (vence: {row['fecha_expiracion']})\n"
                respuesta += "\n"
            
            if criticos.empty and advertencia.empty:
                respuesta += "✅ **Buenas noticias:** Todos los dominios tienen más de 60 días para vencer.\n"
            
            return respuesta
        
        return "No hay suficientes datos para analizar vencimientos."
    
    def _analizar_certificados_ssl(self, contexto: Dict) -> str:
        """
        Analiza estado de certificados SSL
        """
        if 'dataframe_completo' in contexto:
            df = contexto['dataframe_completo']
            
            if df.empty:
                return "No se encontraron datos de dominios para analizar certificados SSL."
            
            respuesta = f"Análisis de certificados SSL:\n\n"
            
            for _, row in df.iterrows():
                dominio = row['dominio']
                dias_ssl = row.get('dias_hasta_expiracion_ssl', 'N/A')
                
                respuesta += f"🔒 **{dominio}**\n"
                respuesta += f"• Estado SSL: {'Válido' if dias_ssl != 'N/A' else 'No disponible'}\n"
                
                if dias_ssl != 'N/A':
                    if isinstance(dias_ssl, (int, float)) and dias_ssl <= 30:
                        respuesta += f"• ⚠️ Certificado por expirar en {dias_ssl} días\n"
                    else:
                        respuesta += f"• ✅ Certificado vigente (expira en {dias_ssl} días)\n"
                
                respuesta += "\n"
            
            return respuesta
        
        return "No hay suficientes datos para analizar certificados SSL."
    
    def _analizar_alertas(self, contexto: Dict) -> str:
        """
        Analiza alertas críticas
        """
        if 'decisiones' in contexto:
            decisiones = contexto['decisiones']
            
            respuesta = f"Análisis de alertas:\n\n"
            
            if decisiones.get('dominios_criticos'):
                respuesta += f"🚨 **Alertas Críticas ({len(decisiones['dominios_criticos'])}):**\n"
                for dominio in decisiones['dominios_criticos']:
                    respuesta += f"• {dominio['dominio']}: {dominio.get('dias_hasta_vencimiento', 'N/A')} días para vencer\n"
                respuesta += "\n"
            
            if decisiones.get('dominios_advertencia'):
                respuesta += f"⚠️ **Advertencias ({len(decisiones['dominios_advertencia'])}):**\n"
                for dominio in decisiones['dominios_advertencia']:
                    respuesta += f"• {dominio['dominio']}: {dominio.get('dias_hasta_vencimiento', 'N/A')} días para vencer\n"
                respuesta += "\n"
            
            if not decisiones.get('dominios_criticos') and not decisiones.get('dominios_advertencia'):
                respuesta += "✅ **Sin alertas:** No hay dominios que requieran atención inmediata.\n"
            
            return respuesta
        
        return "No hay datos de alertas disponibles."
    
    def _analizar_resumen_general(self, contexto: Dict) -> str:
        """
        Proporciona un resumen general del estado
        """
        if 'decisiones' in contexto:
            decisiones = contexto['decisiones']
            
            total = decisiones.get('total_evaluados', 0)
            criticos = len(decisiones.get('dominios_criticos', []))
            advertencia = len(decisiones.get('dominios_advertencia', []))
            normales = total - criticos - advertencia
            
            respuesta = f"📊 **Resumen General del Monitoreo:**\n\n"
            respuesta += f"• Total dominios evaluados: {total}\n"
            respuesta += f"• Dominios normales: {normales} ✅\n"
            respuesta += f"• Dominios con advertencia: {advertencia} ⚠️\n"
            respuesta += f"• Dominios críticos: {criticos} 🚨\n\n"
            
            if criticos > 0:
                respuesta += "🔴 **Estado:** Se requiere acción inmediata\n"
            elif advertencia > 0:
                respuesta += "🟡 **Estado:** Se recomienda monitoreo cercano\n"
            else:
                respuesta += "🟢 **Estado:** Todos los dominios en buen estado\n"
            
            return respuesta
        
        return "No hay suficientes datos para generar un resumen general."
    
    def _respuesta_general(self, contexto: Dict, pregunta: str) -> str:
        """
        Respuesta general para preguntas no específicas
        """
        if 'dataframe_completo' in contexto:
            df = contexto['dataframe_completo']
            
            if not df.empty:
                respuesta = f"He analizado los datos de monitoreo disponibles para {len(df)} dominios.\n\n"
                respuesta += "Puedo ayudarte con:\n"
                respuesta += "• Análisis de fechas de vencimiento\n"
                respuesta += "• Estado de certificados SSL\n"
                respuesta += "• Identificación de alertas críticas\n"
                respuesta += "• Resumen general del estado\n\n"
                respuesta += "¿Qué aspecto específico te gustaría que analice?"
                return respuesta
        
        return "Para poder analizar los datos, primero ejecuta un monitoreo de dominios desde el panel principal."
    
    def consultar_dominio_completo(self, dominio: str) -> Dict:
        """
        Obtiene información completa de un dominio (WHOIS + SSL)
        
        Args:
            dominio: Nombre del dominio a consultar
            
        Returns:
            Diccionario con información completa
        """
        try:
            # Obtener información WHOIS
            info_whois = self.agente_lector.obtener_info_dominio(dominio)
            
            # Obtener información SSL
            info_ssl = self.ssl_checker.obtener_info_ssl(dominio)
            
            # Combinar información
            resultado = {
                'dominio': dominio,
                'whois': info_whois,
                'ssl': info_ssl,
                'fecha_consulta': datetime.now(),
                'estado': 'completo' if info_whois and info_ssl else 'parcial'
            }
            
            self.logger.info(f"Consulta completa realizada para {dominio}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en consulta completa para {dominio}: {str(e)}")
            return {
                'dominio': dominio,
                'error': str(e),
                'fecha_consulta': datetime.now(),
                'estado': 'error'
            }
    
    def generar_respuesta_chatgpt(self, pregunta: str, contexto_dominios: Optional[Dict] = None) -> str:
        """
        Genera respuesta usando ChatGPT
        
        Args:
            pregunta: Pregunta del usuario
            contexto_dominios: Información de dominios relevante
            
        Returns:
            Respuesta generada por ChatGPT
        """
        try:
            # Verificar si tenemos un modelo disponible
            if not self.model:
                raise Exception("No hay modelo disponible. Verifica tu API key de ChatGPT.")
            
            # Construir prompt con contexto
            prompt = f"{self.system_context}\n\n"
            
            if contexto_dominios:
                prompt += "CONTEXTO DE DOMINIOS DISPONIBLE:\n"
                prompt += f"```json\n{json.dumps(contexto_dominios, default=str, indent=2)}\n```\n\n"
            
            prompt += f"PREGUNTA DEL USUARIO: {pregunta}\n\n"
            prompt += "Proporciona una respuesta detallada y útil basada en la información disponible."
            
            # Generar respuesta usando el modelo de ChatGPT
            self.logger.info(f"API: Usando modelo {self.model}")
            self.logger.info("API: Enviando solicitud a ChatGPT...")
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_context},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            self.logger.info("API: Respuesta recibida exitosamente")
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"ERROR: Falló en generar_respuesta_chatgpt: {str(e)}")
            self.logger.error(f"ERROR: Tipo de error: {type(e).__name__}")
            return f"Lo siento, tuve un error al procesar tu pregunta: {str(e)}"
    
    def procesar_pregunta(self, pregunta: str, contexto_monitoreo: Optional[Dict] = None) -> Dict:
        """
        Procesa una pregunta del usuario y genera respuesta basada en contexto
        
        Args:
            pregunta: Pregunta del usuario
            contexto_monitoreo: Resultados del monitoreo disponibles
            
        Returns:
            Diccionario con respuesta y metadatos
        """
        try:
            # Generar respuesta basada en contexto de monitoreo
            respuesta = self.generar_respuesta_contexto(pregunta, contexto_monitoreo)
            
            resultado = {
                'pregunta': pregunta,
                'respuesta': respuesta,
                'contexto_utilizado': contexto_monitoreo is not None,
                'timestamp': datetime.now()
            }
            
            self.logger.info(f"Pregunta procesada: {pregunta[:50]}...")
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error procesando pregunta: {str(e)}")
            return {
                'pregunta': pregunta,
                'respuesta': f"Lo siento, ocurrió un error al procesar tu pregunta: {str(e)}",
                'contexto_utilizado': False,
                'timestamp': datetime.now(),
                'error': str(e)
            }
    
    def _extraer_dominios(self, texto: str, dominios_disponibles: List[str] = None) -> List[str]:
        """
        Extrae nombres de dominio de un texto
        
        Args:
            texto: Texto donde buscar dominios
            dominios_disponibles: Lista de dominios disponibles para limitar búsqueda
            
        Returns:
            Lista de dominios encontrados
        """
        import re
        
        # Patrones para encontrar dominios
        patrones = [
            r'\b[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+\b',
            r'\b(?:www\.)?[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z]{2,})+\b'
        ]
        
        encontrados = set()
        
        for patron in patrones:
            matches = re.findall(patron, texto, re.IGNORECASE)
            for match in matches:
                dominio = match.lower().strip()
                if dominios_disponibles:
                    if dominio in [d.lower() for d in dominios_disponibles]:
                        encontrados.add(dominio)
                else:
                    encontrados.add(dominio)
        
        return list(encontrados)
    
    def obtener_resumen_dominios(self, dominios: List[str]) -> Dict:
        """
        Obtiene un resumen de múltiples dominios
        
        Args:
            dominios: Lista de dominios a analizar
            
        Returns:
            Resumen con información consolidada
        """
        try:
            resultados = []
            
            for dominio in dominios:
                info = self.consultar_dominio_completo(dominio)
                resultados.append(info)
            
            # Analizar resultados
            total_dominios = len(resultados)
            dominios_con_ssl = sum(1 for r in resultados if r.get('ssl'))
            dominios_con_whois = sum(1 for r in resultados if r.get('whois'))
            
            # Alertas SSL
            alertas_ssl = []
            for r in resultados:
                if r.get('ssl'):
                    dias = r['ssl'].get('dias_hasta_expiracion')
                    if dias is not None and dias <= 30:
                        alertas_ssl.append(f"{r['dominio']}: {dias} días para expirar SSL")
            
            # Alertas WHOIS
            alertas_whois = []
            for r in resultados:
                if r.get('whois'):
                    dias = r['whois'].get('dias_hasta_vencimiento')
                    if dias is not None and dias <= 30:
                        alertas_whois.append(f"{r['dominio']}: {dias} días para vencer dominio")
            
            resumen = {
                'total_dominios': total_dominios,
                'dominios_con_ssl': dominios_con_ssl,
                'dominios_con_whois': dominios_con_whois,
                'alertas_ssl': alertas_ssl,
                'alertas_whois': alertas_whois,
                'detalles': resultados,
                'fecha_analisis': datetime.now()
            }
            
            self.logger.info(f"Resumen generado para {total_dominios} dominios")
            return resumen
            
        except Exception as e:
            self.logger.error(f"Error generando resumen: {str(e)}")
            return {
                'error': str(e),
                'fecha_analisis': datetime.now()
            }
    
    def conversacion_interactiva(self, pregunta: str, historial: List[Dict] = None) -> Dict:
        """
        Modo de conversación con historial
        
        Args:
            pregunta: Nueva pregunta del usuario
            historial: Historial de conversación anterior
            
        Returns:
            Respuesta con contexto de conversación
        """
        try:
            # Construir contexto de conversación
            contexto_conversacion = ""
            if historial:
                contexto_conversacion = "HISTORIAL DE CONVERSACIÓN:\n"
                for msg in historial[-5:]:  # Últimos 5 mensajes
                    contexto_conversacion += f"Usuario: {msg.get('pregunta', '')}\n"
                    contexto_conversacion += f"Asistente: {msg.get('respuesta', '')[:200]}...\n\n"
            
            # Procesar pregunta actual
            resultado = self.procesar_pregunta(pregunta)
            
            # Agregar contexto de conversación
            if contexto_conversacion:
                resultado['contexto_conversacion'] = contexto_conversacion
            
            return resultado
            
        except Exception as e:
            self.logger.error(f"Error en conversación interactiva: {str(e)}")
            return {
                'pregunta': pregunta,
                'respuesta': f"Error en la conversación: {str(e)}",
                'timestamp': datetime.now(),
                'error': str(e)
            }
