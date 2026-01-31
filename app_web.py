#!/usr/bin/env python3
"""
Aplicación Web del Sistema de Monitoreo de Dominios
Interfaz web con pandas para visualización en navegador
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agente_principal import AgentePrincipal
from interfaz_pandas import InterfazPandas
from config_email import obtener_config_email
from traducciones import Traducciones

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Monitoreo de Dominios",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Configuración de tema
def set_custom_theme():
    """
    Define estilos personalizados modernos y revolucionarios
    """
    
    # Tema oscuro revolucionario
    dark_theme = """
    <style>
    /* Estilos base */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%);
        color: #ffffff;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem 1rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        letter-spacing: -0.01em;
    }
    
    .main-header p {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 16px 16px 0 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    /* Alertas modernas */
    .alert-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 12px;
        color: white;
        backdrop-filter: blur(10px);
        font-size: 0.9rem;
        padding: 0.5rem;
    }
    
    /* Tablas */
    .dataframe {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
        font-size: 0.9rem;
    }
    
    .dataframe th {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem;
        font-weight: 600;
    }
    
    .dataframe td {
        padding: 0.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem 1rem;
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.8) 0%, rgba(22, 33, 62, 0.8) 100%);
        border-radius: 20px;
        margin-top: 1.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        font-size: 0.9rem;
    }
    
    .footer h3 {
        font-size: 1.2rem;
        margin-bottom: 0.5rem;
    }
    
    .footer p {
        font-size: 0.85rem;
        margin: 0.25rem 0;
    }
    
    /* Chat interface */
    .chat-message {
        background: rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        font-size: 0.9rem;
    }
    
    .chat-message p {
        margin: 0.25rem 0;
    }
    
    /* Charts */
    .js-plotly-plot {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Animaciones */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .element {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
    }
    </style>
    """
    
    return "", dark_theme

# Inicializar sistema de traducciones
traducciones = Traducciones()

# Inicializar tema oscuro por defecto
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Obtener el idioma actual de session state
if 'idioma' not in st.session_state:
    st.session_state.idioma = 'es'

# Aplicar tema oscuro revolucionario siempre
light_theme, dark_theme = set_custom_theme()
st.markdown(dark_theme, unsafe_allow_html=True)

# Título principal con estilo personalizado
col1, col2 = st.columns([5, 1])

with col1:
    st.markdown(f"""
    <div class="main-header">
        <h1>{traducciones.obtener_texto('titulo_app', st.session_state.idioma)}</h1>
        <p>{traducciones.obtener_texto('subtitulo_app', st.session_state.idioma)}</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para configuración
st.sidebar.markdown(f"""
## ⚙️ {traducciones.obtener_texto('configuracion', st.session_state.idioma)}
""")

# Sección de apariencia
st.sidebar.markdown(f"""
### 🎨 {traducciones.obtener_texto('config_apariencia', st.session_state.idioma)}
""")

# Selector de idioma
idiomas_disponibles = traducciones.obtener_idiomas_disponibles()
idioma_seleccionado = st.sidebar.selectbox(
    traducciones.obtener_texto('idioma', st.session_state.idioma),
    options=list(idiomas_disponibles.keys()),
    format_func=lambda x: idiomas_disponibles[x],
    index=list(idiomas_disponibles.keys()).index(st.session_state.idioma)
)

if idioma_seleccionado != st.session_state.idioma:
    st.session_state.idioma = idioma_seleccionado
    st.rerun()

st.sidebar.markdown("---")

# Input de dominios
dominios_input = st.sidebar.text_area(
    traducciones.obtener_texto('ingresar_dominios', st.session_state.idioma),
    value="google.com\ngithub.com\nmicrosoft.com\npython.org\nsite.xyz",
    height=150
)

# Convertir input a lista
dominios = [d.strip() for d in dominios_input.split('\n') if d.strip()]

# Configuración de correo
st.sidebar.markdown(f"""
### 📧 {traducciones.obtener_texto('config_correo', st.session_state.idioma)}
""")
enviar_correo = st.sidebar.checkbox(traducciones.obtener_texto('enviar_notificaciones', st.session_state.idioma))
destinatario = st.sidebar.text_input(traducciones.obtener_texto('correo_destinatario', st.session_state.idioma), value="")

# Botón principal
st.sidebar.markdown("---")
if st.sidebar.button(traducciones.obtener_texto('btn_iniciar_monitoreo', st.session_state.idioma), type="primary"):
    # Inicializar agentes
    config_email = obtener_config_email('gmail') if enviar_correo else None
    agente_principal = AgentePrincipal(config_email)
    interfaz = InterfazPandas(agente_principal)
    
    # Mostrar spinner durante el monitoreo
    with st.spinner(traducciones.obtener_texto('monitoreando_dominios', st.session_state.idioma)):
        # Ejecutar monitoreo
        destinatarios = [destinatario] if enviar_correo and destinatario else []
        resultados = agente_principal.monitorear_dominios(dominios, destinatarios, forzar_envio_correo=enviar_correo)
        
        # Guardar resultados en session state
        st.session_state.resultados = resultados
        st.session_state.interfaz = interfaz
        st.session_state.dominios = dominios

# Mostrar resultados si existen
if 'resultados' in st.session_state:
    resultados = st.session_state.resultados
    interfaz = st.session_state.interfaz
    dominios = st.session_state.dominios
    
    # Sección de resumen con tarjetas personalizadas
    st.markdown(f"""
    <div class="main-header">
        <h2>{traducciones.obtener_texto('resumen_monitoreo', st.session_state.idioma)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principales con estilo personalizado
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>{traducciones.obtener_texto('total_dominios', st.session_state.idioma)}</h3>
            <h2>{resultados['dominios_procesados']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        criticos = resultados['decisiones']['criticos_count'] if resultados['decisiones'] else 0
        alert_text = f"⚠️ {criticos} alertas" if criticos > 0 else traducciones.obtener_texto('sin_alertas', st.session_state.idioma)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{traducciones.obtener_texto('dominios_criticos', st.session_state.idioma)}</h3>
            <h2>{criticos}</h2>
            <p>{alert_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        advertencias = resultados['decisiones']['advertencia_count'] if resultados['decisiones'] else 0
        alert_text = f"📋 {advertencias} advertencias" if advertencias > 0 else traducciones.obtener_texto('sin_advertencias', st.session_state.idioma)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{traducciones.obtener_texto('dominios_advertencia', st.session_state.idioma)}</h3>
            <h2>{advertencias}</h2>
            <p>{alert_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        log_status = "📝 Archivo creado" if resultados['log_generado'] else "📄 Sin log"
        st.markdown(f"""
        <div class="metric-card">
            <h3>{traducciones.obtener_texto('log_generado', st.session_state.idioma)}</h3>
            <h2>{'Sí' if resultados['log_generado'] else 'No'}</h2>
            <p>{log_status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Obtener DataFrame actualizado
    df_actual = interfaz.agente.obtener_reporte_pandas(dominios)
    
    if not df_actual.empty:
        # Sección de tabla detallada
        st.header(traducciones.obtener_texto('tabla_detalles', st.session_state.idioma))
        
        # Formatear DataFrame para visualización
        df_visual = df_actual.copy()
        df_visual['fecha_expiracion'] = df_visual['fecha_expiracion'].dt.strftime('%Y-%m-%d')
        df_visual['fecha_consulta'] = df_visual['fecha_consulta'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Agregar estado de alerta
        df_visual['estado_alerta'] = df_visual['dias_hasta_vencimiento'].apply(
            lambda x: traducciones.obtener_texto('critico', st.session_state.idioma) if x <= 30 else (traducciones.obtener_texto('advertencia', st.session_state.idioma) if x <= 50 else traducciones.obtener_texto('normal', st.session_state.idioma))
        )
        
        # Renombrar columnas
        df_visual = df_visual.rename(columns={
            'dominio': traducciones.obtener_texto('dominio', st.session_state.idioma),
            'dias_hasta_vencimiento': traducciones.obtener_texto('dias_vencimiento', st.session_state.idioma),
            'fecha_expiracion': traducciones.obtener_texto('fecha_expiracion', st.session_state.idioma),
            'registrar': traducciones.obtener_texto('registrador', st.session_state.idioma),
            'estado_alerta': traducciones.obtener_texto('estado_alerta', st.session_state.idioma),
            'fecha_consulta': traducciones.obtener_texto('fecha_consulta', st.session_state.idioma)
        })
        
        # Mostrar tabla con formato
        st.dataframe(
            df_visual[[traducciones.obtener_texto('dominio', st.session_state.idioma), traducciones.obtener_texto('dias_vencimiento', st.session_state.idioma), traducciones.obtener_texto('fecha_expiracion', st.session_state.idioma), traducciones.obtener_texto('estado_alerta', st.session_state.idioma), traducciones.obtener_texto('registrador', st.session_state.idioma)]],
            use_container_width=True,
            hide_index=True
        )
        
        # Sección de gráficos
        st.header(traducciones.obtener_texto('visualizacion_datos', st.session_state.idioma))
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras - Días hasta vencimiento
            fig_barras = px.bar(
                df_actual.sort_values('dias_hasta_vencimiento'),
                x='dominio',
                y='dias_hasta_vencimiento',
                title=traducciones.obtener_texto('titulo_barras', st.session_state.idioma),
                labels={'dias_hasta_vencimiento': traducciones.obtener_texto('dias_vencimiento', st.session_state.idioma), 'dominio': traducciones.obtener_texto('dominio', st.session_state.idioma)},
                color='dias_hasta_vencimiento',
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig_barras.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_barras, use_container_width=True)
        
        with col2:
            # Gráfico de pastel - Estados de alerta
            df_actual['estado_categoria'] = df_actual['dias_hasta_vencimiento'].apply(
                lambda x: (traducciones.obtener_texto('critico', st.session_state.idioma) + ' (≤30 días)') if x <= 30 else ((traducciones.obtener_texto('advertencia', st.session_state.idioma) + ' (31-50 días)') if x <= 50 else (traducciones.obtener_texto('normal', st.session_state.idioma) + ' (>50 días)'))
            )
            
            conteo_estados = df_actual['estado_categoria'].value_counts()
            
            fig_pie = px.pie(
                names=conteo_estados.index,
                values=conteo_estados.values,
                title=traducciones.obtener_texto('titulo_pastel', st.session_state.idioma),
                color_discrete_map={
                    traducciones.obtener_texto('critico', st.session_state.idioma) + ' (≤30 días)': 'red',
                    traducciones.obtener_texto('advertencia', st.session_state.idioma) + ' (31-50 días)': 'orange',
                    traducciones.obtener_texto('normal', st.session_state.idioma) + ' (>50 días)': 'green'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Sección de análisis temporal
        st.header(traducciones.obtener_texto('analisis_temporal', st.session_state.idioma))
        
        # Crear análisis temporal
        analisis_temporal = interfaz.crear_analisis_temporal()
        
        if not analisis_temporal.empty:
            # Gráfico de análisis temporal
            fig_timeline = px.bar(
                analisis_temporal,
                x='Rango',
                y='Cantidad',
                title=traducciones.obtener_texto('titulo_timeline', st.session_state.idioma),
                color='Porcentaje',
                text='Cantidad'
            )
            fig_timeline.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Tabla de análisis temporal
            st.dataframe(
                analisis_temporal[['Rango', 'Cantidad', 'Porcentaje']],
                use_container_width=True,
                hide_index=True
            )
        
        # Sección de alertas con estilo personalizado
        if resultados['decisiones'] and (resultados['decisiones']['criticos_count'] > 0 or resultados['decisiones']['advertencia_count'] > 0):
            st.markdown(f"""
            <div class="main-header">
                <h2>{traducciones.obtener_texto('alertas_activas', st.session_state.idioma)}</h2>
            </div>
            """, unsafe_allow_html=True)
            
            alertas = interfaz.generar_alertas_visual()
            
            for alerta in alertas['alertas']:
                if alerta['tipo'] == '🚨 CRÍTICO':
                    st.markdown(f"""
                    <div class="alert-critical">
                        <h3>{alerta['tipo']}</h3>
                        <p>{alerta['mensaje']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-warning">
                        <h3>{alerta['tipo']}</h3>
                        <p>{alerta['mensaje']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Botón de exportación
        st.header(traducciones.obtener_texto('exportar_datos', st.session_state.idioma))
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(traducciones.obtener_texto('btn_exportar_csv', st.session_state.idioma)):
                csv = df_visual.to_csv(index=False)
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name=f"dominios_reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button(traducciones.obtener_texto('btn_exportar_excel', st.session_state.idioma)):
                # Generar Excel en memoria
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    df_visual.to_excel(writer, sheet_name='Reporte', index=False)
                    analisis_temporal.to_excel(writer, sheet_name='Análisis', index=False)
                
                st.download_button(
                    label="Descargar Excel",
                    data=buffer.getvalue(),
                    file_name=f"dominios_reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    else:
        st.warning(traducciones.obtener_texto('alert_sin_dominios', st.session_state.idioma))

# Instrucciones
st.sidebar.markdown("---")
st.sidebar.markdown(f"### {traducciones.obtener_texto('instrucciones', st.session_state.idioma)}:")
st.sidebar.markdown("""
1. **Ingrese dominios** en el área de texto
2. **Ejecute monitoreo** para obtener datos
3. **Exporte** los datos en CSV o Excel
""")

# Footer personalizado
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <h3>{traducciones.obtener_texto('footer_titulo', st.session_state.idioma)}</h3>
    <p>{traducciones.obtener_texto('footer_texto', st.session_state.idioma)} | 
    {traducciones.obtener_texto('footer_actualizacion', st.session_state.idioma)}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>{traducciones.obtener_texto('footer_agentes', st.session_state.idioma)}:</strong> 📖 Lector | 🧠 Decisor | 🎯 Principal | 📊 Interfaz Pandas</p>
</div>
""", unsafe_allow_html=True)
