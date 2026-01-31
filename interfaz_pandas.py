import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from agente_principal import AgentePrincipal
from typing import List, Dict

class InterfazPandas:
    """
    Interfaz visual basada en pandas para el sistema de monitoreo
    """
    
    def __init__(self, agente_principal: AgentePrincipal):
        self.agente = agente_principal
        self.df_actual = None
        
    def crear_tablero_resumen(self, lista_dominios: List[str]) -> pd.DataFrame:
        """
        Crea un tablero resumen con información clave
        
        Args:
            lista_dominios: Lista de dominios a analizar
            
        Returns:
            DataFrame con tablero resumen
        """
        # Obtener datos del agente
        self.df_actual = self.agente.obtener_reporte_pandas(lista_dominios)
        
        if self.df_actual.empty:
            return pd.DataFrame()
        
        # Crear tablero resumen
        resumen_data = {
            'Métrica': [
                'Total Dominios',
                'Dominios Críticos (≤30 días)',
                'Dominios Advertencia (31-50 días)',
                'Dominios Normales (>50 días)',
                'Promedio Días hasta Vencimiento',
                'Dominio más crítico',
                'Próximo vencimiento'
            ],
            'Valor': [
                len(self.df_actual),
                len(self.df_actual[self.df_actual['dias_hasta_vencimiento'] <= 30]),
                len(self.df_actual[(self.df_actual['dias_hasta_vencimiento'] > 30) & 
                                 (self.df_actual['dias_hasta_vencimiento'] <= 50)]),
                len(self.df_actual[self.df_actual['dias_hasta_vencimiento'] > 50]),
                f"{self.df_actual['dias_hasta_vencimiento'].mean():.1f} días",
                self.df_actual.loc[self.df_actual['dias_hasta_vencimiento'].idxmin(), 'dominio'] if not self.df_actual.empty else 'N/A',
                self.df_actual.loc[self.df_actual['dias_hasta_vencimiento'].idxmin(), 'fecha_expiracion'].strftime('%Y-%m-%d') if not self.df_actual.empty else 'N/A'
            ]
        }
        
        return pd.DataFrame(resumen_data)
    
    def crear_tabla_detalles(self) -> pd.DataFrame:
        """
        Crea una tabla detallada con formato mejorado
        
        Returns:
            DataFrame formateado con detalles
        """
        if self.df_actual is None or self.df_actual.empty:
            return pd.DataFrame()
        
        # Copiar y formatear el DataFrame
        df_detalles = self.df_actual.copy()
        
        # Formatear fechas
        df_detalles['fecha_expiracion'] = df_detalles['fecha_expiracion'].dt.strftime('%Y-%m-%d')
        df_detalles['fecha_consulta'] = df_detalles['fecha_consulta'].dt.strftime('%Y-%m-%d %H:%M')
        
        # Renombrar columnas para mejor visualización
        df_detalles = df_detalles.rename(columns={
            'dominio': 'Dominio',
            'fecha_expiracion': 'Fecha Expiración',
            'dias_hasta_vencimiento': 'Días hasta Vencimiento',
            'registrar': 'Registrador',
            'estado_alerta': 'Estado Alerta',
            'prioridad': 'Prioridad',
            'fecha_consulta': 'Fecha Consulta'
        })
        
        # Reordenar columnas
        columnas_orden = ['Dominio', 'Días hasta Vencimiento', 'Fecha Expiración', 
                         'Estado Alerta', 'Prioridad', 'Registrador', 'Fecha Consulta']
        
        return df_detalles[columnas_orden]
    
    def crear_analisis_temporal(self) -> pd.DataFrame:
        """
        Crea un análisis temporal de vencimientos
        
        Returns:
            DataFrame con análisis por rangos de tiempo
        """
        if self.df_actual is None or self.df_actual.empty:
            return pd.DataFrame()
        
        # Definir rangos
        rangos = [
            (0, 7, 'Crítico Inminente (0-7 días)'),
            (8, 15, 'Crítico Alto (8-15 días)'),
            (16, 30, 'Crítico Medio (16-30 días)'),
            (31, 50, 'Advertencia (31-50 días)'),
            (51, 90, 'Monitoreo (51-90 días)'),
            (91, 365, 'Seguro (>90 días)')
        ]
        
        analisis_data = []
        
        for min_dias, max_dias, etiqueta in rangos:
            if max_dias == 365:
                filtrados = self.df_actual[self.df_actual['dias_hasta_vencimiento'] > min_dias]
            else:
                filtrados = self.df_actual[(self.df_actual['dias_hasta_vencimiento'] >= min_dias) & 
                                         (self.df_actual['dias_hasta_vencimiento'] <= max_dias)]
            
            analisis_data.append({
                'Rango': etiqueta,
                'Cantidad': len(filtrados),
                'Porcentaje': (len(filtrados) / len(self.df_actual)) * 100 if not self.df_actual.empty else 0,
                'Dominios': ', '.join(filtrados['dominio'].tolist()) if len(filtrados) <= 3 else f"{len(filtrados)} dominios"
            })
        
        return pd.DataFrame(analisis_data)
    
    def exportar_reporte_completo(self, lista_dominios: List[str], 
                                 nombre_archivo: str = 'reporte_dominios_completo.xlsx'):
        """
        Exporta un reporte completo a Excel con múltiples hojas
        
        Args:
            lista_dominios: Lista de dominios a analizar
            nombre_archivo: Nombre del archivo Excel
        """
        try:
            # Actualizar datos
            self.df_actual = self.agente.obtener_reporte_pandas(lista_dominios)
            
            if self.df_actual.empty:
                print("No hay datos para exportar")
                return
            
            # Crear DataFrames para cada hoja
            df_resumen = self.crear_tablero_resumen(lista_dominios)
            df_detalles = self.crear_tabla_detalles()
            df_analisis = self.crear_analisis_temporal()
            
            # Exportar a Excel con múltiples hojas
            with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
                df_detalles.to_excel(writer, sheet_name='Detalles', index=False)
                df_analisis.to_excel(writer, sheet_name='Análisis Temporal', index=False)
                
                # Obtener la hoja de detalles para dar formato
                worksheet = writer.sheets['Detalles']
                
                # Ajustar ancho de columnas
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            print(f"Reporte exportado exitosamente a {nombre_archivo}")
            
        except Exception as e:
            print(f"Error al exportar reporte: {str(e)}")
    
    def mostrar_interfaz_completa(self, lista_dominios: List[str]):
        """
        Muestra la interfaz completa en consola
        
        Args:
            lista_dominios: Lista de dominios a analizar
        """
        print("\n" + "="*80)
        print("INTERFAZ DE MONITOREO DE DOMINIOS - PANDAS")
        print("="*80)
        
        # Actualizar datos
        self.df_actual = self.agente.obtener_reporte_pandas(lista_dominios)
        
        if self.df_actual.empty:
            print("No se pudo obtener información de los dominios")
            return
        
        # Mostrar tablero resumen
        print("\n📊 TABLERO RESUMEN")
        print("-" * 40)
        resumen = self.crear_tablero_resumen(lista_dominios)
        for _, row in resumen.iterrows():
            print(f"{row['Métrica']}: {row['Valor']}")
        
        # Mostrar tabla detalles
        print("\n📋 TABLA DETALLADA")
        print("-" * 40)
        detalles = self.crear_tabla_detalles()
        print(detalles.to_string(index=False))
        
        # Mostrar análisis temporal
        print("\n📈 ANÁLISIS TEMPORAL")
        print("-" * 40)
        analisis = self.crear_analisis_temporal()
        for _, row in analisis.iterrows():
            print(f"{row['Rango']}: {row['Cantidad']} dominios ({row['Porcentaje']:.1f}%)")
        
        print("\n" + "="*80)
    
    def generar_alertas_visual(self) -> Dict:
        """
        Genera alertas en formato visual
        
        Returns:
            Diccionario con alertas formateadas
        """
        if self.df_actual is None or self.df_actual.empty:
            return {'alertas': [], 'total': 0}
        
        alertas = []
        
        # Alertas críticas
        criticos = self.df_actual[self.df_actual['dias_hasta_vencimiento'] <= 30]
        for _, dominio in criticos.iterrows():
            alertas.append({
                'tipo': '🚨 CRÍTICO',
                'dominio': dominio['dominio'],
                'dias': dominio['dias_hasta_vencimiento'],
                'mensaje': f"El dominio {dominio['dominio']} vence en {dominio['dias_hasta_vencimiento']} días"
            })
        
        # Alertas de advertencia
        advertencias = self.df_actual[(self.df_actual['dias_hasta_vencimiento'] > 30) & 
                                     (self.df_actual['dias_hasta_vencimiento'] <= 50)]
        for _, dominio in advertencias.iterrows():
            alertas.append({
                'tipo': '⚠️ ADVERTENCIA',
                'dominio': dominio['dominio'],
                'dias': dominio['dias_hasta_vencimiento'],
                'mensaje': f"El dominio {dominio['dominio']} vence en {dominio['dias_hasta_vencimiento']} días"
            })
        
        return {
            'alertas': alertas,
            'total': len(alertas),
            'criticas': len(criticos),
            'advertencias': len(advertencias)
        }
