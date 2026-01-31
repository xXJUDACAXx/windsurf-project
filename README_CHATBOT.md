# Sistema de Monitoreo de Dominios con Chatbot Gemini 2.5 Pro

Este proyecto ahora incluye un chatbot inteligente con Gemini 2.5 Pro para consultas sobre dominios y certificados SSL.

## 🆕 Nuevas Funcionalidades

### 🤖 Chatbot con Gemini 2.5 Pro
- **Asistente inteligente**: Consulta información sobre dominios y certificados SSL
- **Análisis en tiempo real**: Verifica certificados SSL y datos WHOIS al momento
- **Respuestas contextuales**: Utiliza la información de tus dominios para dar respuestas precisas
- **Conversación natural**: Interfaz de chat intuitiva con historial

### 🔍 Verificación de Certificados SSL
- **Análisis completo**: Fechas de expiración, emisores, algoritmos
- **Validación de dominios**: Verifica si el certificado es válido para el dominio
- **Alertas automáticas**: Notifica sobre certificados por expirar
- **Múltiples dominios**: Análisis simultáneo de varios dominios

## 📋 Requisitos Actualizados

Las nuevas dependencias incluyen:
```
google-generativeai>=0.3.0
ssl
socket
```

## 🚀 Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Obtener API Key de Gemini
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Cópiala para configurarla en la aplicación

### 3. Configurar la aplicación
- Ejecuta la aplicación con Streamlit:
```bash
streamlit run app_web.py
```
- En la barra lateral, ingresa tu API key de Gemini
- La aplicación está lista para usar

## 💡 Cómo Usar el Chatbot

### Paso 1: Monitorear Dominios
1. Ingresa los dominios que quieres monitorear
2. Haz clic en "Iniciar Monitoreo"
3. Espera a que se recopile la información

### Paso 2: Hacer Preguntas
1. Ve a la sección "Asistente de Dominios con Gemini 2.5 Pro"
2. Usa las preguntas sugeridas o escribe las tuyas
3. El chatbot analizará tus dominios y responderá

### Ejemplos de Preguntas:
- "¿Cuáles dominios están por vencer en los próximos 30 días?"
- "¿Qué certificados SSL expiran pronto?"
- "Analiza el estado completo del dominio google.com"
- "¿Hay alguna alerta crítica que deba conocer?"
- "¿Cuáles de mis dominios tienen certificados SSL válidos?"

## 🏗️ Arquitectura

### Nuevos Módulos:
- **`ssl_checker.py`**: Módulo para verificar certificados SSL
- **`chatbot_dominios.py`**: Chatbot con integración de Gemini 2.5 Pro

### Flujo de Datos:
1. **Usuario ingresa dominios** → Monitoreo tradicional
2. **Usuario hace pregunta** → Chatbot analiza dominios
3. **Gemini 2.5 Pro procesa** → Respuesta inteligente
4. **Resultados mostrados** → Con historial de conversación

## 🔧 Características Técnicas

### SSL Checker:
- Verificación de certificados SSL/TLS
- Análisis de fechas de expiración
- Validación de dominios (CN y SAN)
- Detección de certificados auto-firmados
- Soporte para puertos personalizados

### Chatbot Gemini:
- Integración con Google Generative AI
- Extracción automática de dominios del texto
- Contexto de conversación
- Análisis de múltiples dominios simultáneamente
- Respuestas en español

## 🛡️ Seguridad

- **API Keys**: Configuración segura de API keys
- **Validación**: Verificación de dominios antes de consultas
- **Timeouts**: Límites de tiempo para consultas SSL
- **Manejo de errores**: Gestión robusta de excepciones

## 📊 Funcionalidades Adicionales

### Análisis Completo:
- Resumen de todos los dominios monitoreados
- Alertas SSL y WHOIS consolidadas
- Estadísticas y métricas
- Exportación de resultados

### Interfaz Mejorada:
- Diseño responsivo y moderno
- Tema claro/oscuro
- Historial de conversación
- Sugerencias de preguntas interactivas

## 🚨 Notas Importantes

1. **API Key requerida**: Necesitas una API key válida de Google Generative AI
2. **Conexión a internet**: Requerida para consultas WHOIS y SSL
3. **Límites de API**: Respeta los límites de la API de Gemini
4. **Dominios válidos**: Asegúrate de ingresar dominios correctos

## 🔄 Actualización desde versión anterior

La aplicación es completamente compatible con la versión anterior. Las nuevas funcionalidades se agregan sin modificar el comportamiento existente:

- ✅ Monitoreo WHOIS tradicional
- ✅ Alertas por correo
- ✅ Exportación de datos
- ✅ Visualizaciones
- 🆕 Chatbot con Gemini 2.5 Pro
- 🆕 Verificación SSL
- 🆕 Análisis inteligente

## 📞 Soporte

Si tienes problemas o preguntas:
1. Verifica tu API key de Gemini
2. Asegúrate de tener conexión a internet
3. Revisa que los dominios sean válidos
4. Consulta los logs en la consola para errores detallados
