#!/usr/bin/env python3
"""
Sistema de internacionalización para la aplicación
"""

class Traducciones:
    """
    Clase para manejar traducciones de la aplicación
    """
    
    def __init__(self):
        self.traducciones = {
            'es': {
                # Títulos principales
                'titulo_app': 'Sistema de Monitoreo de Dominios',
                'subtitulo_app': 'Monitoreo inteligente de vencimiento de dominios',
                
                # Sidebar - Configuración
                'configuracion': 'Configuración',
                'ingresar_dominios': 'Ingrese dominios a monitorear',
                'config_correo': 'Configuración de Correo',
                'enviar_notificaciones': 'Enviar notificaciones por correo',
                'correo_destinatario': 'Correo destinatario',
                'config_chatbot': 'Configuración de Asistente',
                'api_key_gemini': 'API Key de Gemini',
                'api_key_help': 'Ingresa tu API key de Google Generative AI (Gemini 2.5 Pro)',
                'config_apariencia': 'Configuración de Apariencia',
                'idioma': 'Idioma',
                'tema': 'Tema',
                
                # Botones
                'btn_iniciar_monitoreo': 'Iniciar Monitoreo',
                'btn_enviar_pregunta': 'Enviar Pregunta',
                'btn_limpiar_chat': 'Limpiar Chat',
                'btn_analisis_completo': 'Análisis Completo',
                'btn_exportar_csv': 'Exportar a CSV',
                'btn_exportar_excel': 'Exportar a Excel',
                
                # Secciones
                'resumen_monitoreo': 'Resumen del Monitoreo',
                'tabla_detalles': 'Tabla Detallada de Dominios',
                'visualizacion_datos': 'Visualización de Datos',
                'analisis_temporal': 'Análisis Temporal',
                'alertas_activas': 'Alertas Activas',
                'exportar_datos': 'Exportar Datos',
                'historial_conversacion': 'Historial de Conversación',
                'haz_pregunta': 'Haz una pregunta',
                'sugerencias_preguntas': 'Sugerencias de preguntas',
                
                # Métricas
                'total_dominios': 'Total Dominios',
                'dominios_criticos': 'Dominios Críticos',
                'dominios_advertencia': 'Dominios Advertencia',
                'log_generado': 'Log Generado',
                'sin_alertas': 'Sin alertas',
                'sin_advertencias': 'Sin advertencias',
                
                # Tablas
                'dominio': 'Dominio',
                'dias_vencimiento': 'Días hasta Vencimiento',
                'fecha_expiracion': 'Fecha Expiración',
                'estado_alerta': 'Estado Alerta',
                'registrador': 'Registrador',
                'fecha_consulta': 'Fecha Consulta',
                
                # Gráficos
                'titulo_barras': 'Días hasta Vencimiento por Dominio',
                'titulo_pastel': 'Distribución de Estados de Dominios',
                'titulo_timeline': 'Análisis Temporal de Vencimientos',
                
                # Estados
                'critico': '🚨 CRÍTICO',
                'advertencia': '⚠️ ADVERTENCIA',
                'normal': '✅ NORMAL',
                
                # Chatbot - Sugerencias
                'sug_dominios_vencer': '🔍 ¿Cuáles dominios están por vencer?',
                'sug_ssl_expirar': '🔒 ¿Qué certificados SSL expiran pronto?',
                'sug_alertas_criticas': '⚠️ ¿Hay alertas críticas?',
                'sug_analisis_google': '📊 Análisis de google.com',
                'sug_dominios_seguros': '🛡️ ¿Dominios seguros?',
                'sug_recomendaciones': '📈 Recomendaciones',
                
                # Mensajes
                'monitoreando_dominios': '🔄 Monitoreando dominios...',
                'procesando_pregunta': '🤖 Procesando tu pregunta con Gemini 2.5 Pro...',
                'analizando_dominios': '🔄 Analizando todos los dominios...',
                'escribe_pregunta': 'Escribe tu pregunta sobre dominios y certificados SSL:',
                'dominios_analizados': 'Dominios analizados',
                
                # Alertas
                'alert_configurar_api': '⚠️ Para usar el asistente de IA, configura tu API key de Gemini en la barra lateral',
                'alert_chatbot_configurado': '✅ Chatbot configurado',
                'alert_chatbot_error': '❌ Error configurando chatbot',
                'alert_api_key_vacia': '⚠️ Configura la API key para activar el chatbot',
                'alert_escribe_pregunta': '⚠️ Por favor, escribe una pregunta',
                'alert_primero_monitoreo': '⚠️ Primero ejecuta un monitoreo de dominios',
                'alert_sin_dominios': '⚠️ No se pudo obtener información de los dominios. Verifique los nombres e intente nuevamente.',
                
                # Instrucciones
                'instrucciones': '📋 Instrucciones:',
                'texto_instrucciones': '''
1. **Configure API Key** de Gemini en la barra lateral
2. **Ingrese dominios** en el área de texto
3. **Ejecute monitoreo** para obtener datos
4. **Haga preguntas** al asistente sobre dominios
5. **Exporte** los datos en CSV o Excel
                ''',
                
                # Sistema
                'sistema': 'ℹ️ Sistema:',
                'texto_sistema': '''
- **Agente Lector**: Consulta WHOIS
- **Agente Decisor**: Evalúa alertas
- **Agente Principal**: Orquesta el sistema
- **Interfaz Pandas**: Visualización web
- **🤖 Chatbot Gemini**: Asistente IA
                ''',
                
                # Footer
                'footer_titulo': '🌐 Sistema de Monitoreo de Dominios - Doble Agente',
                'footer_texto': 'Monitoreo inteligente con arquitectura de doble agente',
                'usuario': 'Usuario',
        'asistente': 'Asistente',
        'copiar': 'Copiar',
        'sin_conversaciones': 'Aún no hay conversaciones. ¡Haz una pregunta para comenzar!',
                'footer_actualizacion': 'Última actualización',
            },
            'en': {
                # Títulos principales
                'titulo_app': 'Domain Monitoring System',
                'subtitulo_app': 'Intelligent domain expiration monitoring',
                
                # Sidebar - Configuración
                'configuracion': 'Configuration',
                'ingresar_dominios': 'Enter domains to monitor',
                'config_correo': 'Email Configuration',
                'enviar_notificaciones': 'Send email notifications',
                'correo_destinatario': 'Recipient email',
                'config_chatbot': 'Assistant Configuration',
                'api_key_gemini': 'Gemini API Key',
                'api_key_help': 'Enter your Google Generative AI API key (Gemini 2.5 Pro)',
                'config_apariencia': 'Appearance Configuration',
                'idioma': 'Language',
                'tema': 'Theme',
                
                # Botones
                'btn_iniciar_monitoreo': 'Start Monitoring',
                'btn_enviar_pregunta': 'Send Question',
                'btn_limpiar_chat': 'Clear Chat',
                'btn_analisis_completo': 'Full Analysis',
                'btn_exportar_csv': 'Export to CSV',
                'btn_exportar_excel': 'Export to Excel',
                
                # Secciones
                'resumen_monitoreo': 'Monitoring Summary',
                'tabla_detalles': 'Detailed Domain Table',
                'visualizacion_datos': 'Data Visualization',
                'analisis_temporal': 'Temporal Analysis',
                'alertas_activas': 'Active Alerts',
                'exportar_datos': 'Export Data',
                'historial_conversacion': 'Conversation History',
                'haz_pregunta': 'Ask a Question',
                'sugerencias_preguntas': 'Suggested Questions',
                
                # Métricas
                'total_dominios': 'Total Domains',
                'dominios_criticos': 'Critical Domains',
                'dominios_advertencia': 'Warning Domains',
                'log_generado': 'Log Generated',
                'sin_alertas': 'No alerts',
                'sin_advertencias': 'No warnings',
                
                # Tablas
                'dominio': 'Domain',
                'dias_vencimiento': 'Days until Expiration',
                'fecha_expiracion': 'Expiration Date',
                'estado_alerta': 'Alert Status',
                'registrador': 'Registrar',
                'fecha_consulta': 'Query Date',
                
                # Gráficos
                'titulo_barras': 'Days until Expiration by Domain',
                'titulo_pastel': 'Domain Status Distribution',
                'titulo_timeline': 'Temporal Expiration Analysis',
                
                # Estados
                'critico': '🚨 CRITICAL',
                'advertencia': '⚠️ WARNING',
                'normal': '✅ NORMAL',
                
                # Chatbot - Sugerencias
                'sug_dominios_vencer': '🔍 Which domains are expiring soon?',
                'sug_ssl_expirar': '🔒 Which SSL certificates are expiring soon?',
                'sug_alertas_criticas': '⚠️ Are there any critical alerts?',
                'sug_analisis_google': '📊 Analysis of google.com',
                'sug_dominios_seguros': '🛡️ Which domains are secure?',
                'sug_recomendaciones': '📈 Recommendations',
                
                # Mensajes
                'monitoreando_dominios': '🔄 Monitoring domains...',
                'procesando_pregunta': '🤖 Processing your question with Gemini 2.5 Pro...',
                'analizando_dominios': '🔄 Analyzing all domains...',
                'escribe_pregunta': 'Write your question about domains and SSL certificates:',
                'dominios_analizados': 'Domains analyzed',
                
                # Alertas
                'alert_configurar_api': '⚠️ To use the AI assistant, configure your Gemini API key in the sidebar',
                'alert_chatbot_configurado': '✅ Chatbot configured',
                'alert_chatbot_error': '❌ Error configuring chatbot',
                'alert_api_key_vacia': '⚠️ Configure the API key to activate the chatbot',
                'alert_escribe_pregunta': '⚠️ Please write a question',
                'alert_primero_monitoreo': '⚠️ First run a domain monitoring',
                'alert_sin_dominios': '⚠️ Could not obtain domain information. Verify the names and try again.',
                
                # Instrucciones
                'instrucciones': '📋 Instructions:',
                'texto_instrucciones': '''
1. **Configure API Key** of Gemini in the sidebar
2. **Enter domains** in the text area
3. **Run monitoring** to get data
4. **Ask questions** to the assistant about domains
5. **Export** data in CSV or Excel
                ''',
                
                # Sistema
                'sistema': 'ℹ️ System:',
                'texto_sistema': '''
- **Reader Agent**: WHOIS queries
- **Decisor Agent**: Alert evaluation
- **Principal Agent**: System orchestration
- **Pandas Interface**: Web visualization
- **🤖 Gemini Chatbot**: AI Assistant
                ''',
                
                # Footer
                'footer_titulo': '🌐 Domain Monitoring System - Dual Agent',
                'footer_texto': 'Intelligent monitoring with dual agent architecture',
                'footer_agentes': 'Agents',
                'usuario': 'User',
                'asistente': 'Assistant',
                'copiar': 'Copy',
                'sin_conversaciones': 'No conversations yet. Ask a question to start!',
                'footer_actualizacion': 'Last update',
            }
        }
    
    def obtener_texto(self, clave: str, idioma: str = 'es') -> str:
        """
        Obtiene el texto traducido para una clave
        
        Args:
            clave: Clave de traducción
            idioma: Idioma ('es' o 'en')
            
        Returns:
            Texto traducido
        """
        try:
            return self.traducciones.get(idioma, {}).get(clave, clave)
        except Exception:
            return clave
    
    def obtener_idiomas_disponibles(self) -> dict:
        """
        Obtiene los idiomas disponibles
        
        Returns:
            Diccionario con códigos y nombres de idiomas
        """
        return {
            'es': 'Español',
            'en': 'English'
        }
