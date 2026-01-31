#!/usr/bin/env python3
"""
Sistema de Monitoreo de Dominios - Doble Agente
Main principal para ejecutar el sistema completo
"""

import sys
import argparse
from agente_principal import AgentePrincipal
from interfaz_pandas import InterfazPandas
from config_email import obtener_config_email, configurar_correo_manual

def main():
    """
    Función principal del sistema
    """
    parser = argparse.ArgumentParser(description='Sistema de Monitoreo de Dominios - Doble Agente')
    parser.add_argument('--dominios', '-d', nargs='+', help='Lista de dominios a monitorear')
    parser.add_argument('--correos', '-c', nargs='+', help='Correos para notificaciones')
    parser.add_argument('--proveedor', '-p', choices=['gmail', 'outlook', 'yahoo'], 
                       default='gmail', help='Proveedor de correo')
    parser.add_argument('--interfaz', '-i', action='store_true', 
                       help='Mostrar interfaz pandas completa')
    parser.add_argument('--exportar', '-e', help='Exportar reporte a Excel')
    parser.add_argument('--interactivo', action='store_true', 
                       help='Ejecutar en modo interactivo')
    
    args = parser.parse_args()
    
    # Configurar correo
    config_email = obtener_config_email(args.proveedor)
    
    # Inicializar agentes
    agente_principal = AgentePrincipal(config_email)
    interfaz = InterfazPandas(agente_principal)
    
    if args.interactivo:
        # Modo interactivo
        agente_principal.ejecutar_monitoreo_interactivo()
        return
    
    # Modo no interactivo requiere dominios
    if not args.dominios:
        print("Error: Se requiere especificar dominios con --dominios o usar --interactivo")
        sys.exit(1)
    
    print(f"🚀 Iniciando monitoreo de {len(args.dominios)} dominios...")
    print(f"Dominios: {', '.join(args.dominios)}")
    
    # Ejecutar monitoreo
    resultados = agente_principal.monitorear_dominios(args.dominios, args.correos)
    
    # Mostrar resumen
    agente_principal.mostrar_resumen(resultados)
    
    # Mostrar interfaz pandas si se solicita
    if args.interfaz:
        interfaz.mostrar_interfaz_completa(args.dominios)
    
    # Exportar a Excel si se solicita
    if args.exportar:
        interfaz.exportar_reporte_completo(args.dominios, args.exportar)
    
    # Mostrar alertas visuales
    alertas = interfaz.generar_alertas_visual()
    if alertas['total'] > 0:
        print(f"\n🔔 ALERTAS GENERADAS: {alertas['total']}")
        for alerta in alertas['alertas']:
            print(f"  {alerta['tipo']}: {alerta['mensaje']}")
    else:
        print("\n✅ No hay alertas activas")

if __name__ == "__main__":
    main()
