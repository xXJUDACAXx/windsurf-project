#!/usr/bin/env python3
"""
Ejemplo de uso del Sistema de Monitoreo de Dominios
"""

from agente_principal import AgentePrincipal
from interfaz_pandas import InterfazPandas
from config_email import obtener_config_email

def ejemplo_basico():
    """
    Ejemplo básico de uso sin notificaciones por correo
    """
    print("=== EJEMPLO BÁSICO ===")
    
    # Lista de dominios de ejemplo
    dominios = [
        'google.com',
        'github.com', 
        'microsoft.com',
        'python.org'
    ]
    
    # Inicializar agente principal sin configuración de correo
    agente = AgentePrincipal()
    
    # Ejecutar monitoreo
    resultados = agente.monitorear_dominios(dominios)
    
    # Mostrar resumen
    agente.mostrar_resumen(resultados)

def ejemplo_con_interfaz():
    """
    Ejemplo usando la interfaz de pandas
    """
    print("\n=== EJEMPLO CON INTERFAZ PANDAS ===")
    
    dominios = [
        'google.com',
        'github.com',
        'stackoverflow.com'
    ]
    
    # Inicializar agentes
    agente = AgentePrincipal()
    interfaz = InterfazPandas(agente)
    
    # Mostrar interfaz completa
    interfaz.mostrar_interfaz_completa(dominios)
    
    # Generar alertas visuales
    alertas = interfaz.generar_alertas_visual()
    print(f"\n🔔 Total de alertas: {alertas['total']}")

def ejemplo_con_correo():
    """
    Ejemplo con configuración de correo (necesita configuración real)
    """
    print("\n=== EJEMPLO CON CORREO ===")
    
    # NOTA: Debes configurar tus datos reales en config_email.py
    config_email = obtener_config_email('gmail')
    
    dominios = ['google.com', 'github.com']
    destinatarios = ['admin@ejemplo.com']  # Cambiar por correo real
    
    # Inicializar agente con configuración de correo
    agente = AgentePrincipal(config_email)
    
    # Ejecutar monitoreo con notificaciones
    resultados = agente.monitorear_dominios(dominios, destinatarios)
    
    # Mostrar resumen
    agente.mostrar_resumen(resultados)

def ejemplo_exportar_excel():
    """
    Ejemplo de exportación a Excel
    """
    print("\n=== EJEMPLO EXPORTAR A EXCEL ===")
    
    dominios = [
        'google.com',
        'github.com',
        'microsoft.com',
        'python.org',
        'stackoverflow.com'
    ]
    
    # Inicializar agentes
    agente = AgentePrincipal()
    interfaz = InterfazPandas(agente)
    
    # Exportar reporte completo
    interfaz.exportar_reporte_completo(dominios, 'reporte_dominios_ejemplo.xlsx')

if __name__ == "__main__":
    print("🚀 SISTEMA DE MONITOREO DE DOMINIOS - EJEMPLOS DE USO")
    print("=" * 60)
    
    # Ejecutar ejemplos
    ejemplo_basico()
    ejemplo_con_interfaz()
    ejemplo_con_correo()
    ejemplo_exportar_excel()
    
    print("\n✅ Ejemplos completados!")
    print("\n📝 NOTAS IMPORTANTES:")
    print("1. Para usar notificaciones por correo, configura tus datos en config_email.py")
    print("2. Para Gmail, usa 'Contraseñas de aplicaciones' en lugar de tu contraseña normal")
    print("3. El sistema genera logs automáticamente cuando hay dominios críticos")
    print("4. Los correos solo se envían cuando hay dominios por vencer en 30 días o menos")
