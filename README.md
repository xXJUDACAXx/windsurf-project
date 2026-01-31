# Sistema de Monitoreo de Dominios - Doble Agente

Sistema de monitoreo de dominios con arquitectura de doble agente implementado en Python con interfaz en pandas.

## 🏗️ Arquitectura

El sistema consta de tres componentes principales:

### 📖 Agente Lector (`agente_lector.py`)
- **Responsabilidad**: Leer y obtener información de dominios
- **Funciones**:
  - Consultar información de vencimiento de dominios usando WHOIS
  - Calcular días hasta el vencimiento
  - Filtrar dominios por vencimiento
  - Exportar datos a CSV

### 🧠 Agente Decisor (`agente_decisor.py`)
- **Responsabilidad**: Tomar decisiones sobre notificaciones
- **Funciones**:
  - Evaluar dominios según criterios de tiempo
  - Decidir si enviar correos o generar logs
  - Generar contenido de notificaciones
  - Enviar correos electrónicos
  - Crear archivos de log

### 🎯 Agente Principal (`agente_principal.py`)
- **Responsabilidad**: Coordinar a los otros dos agentes
- **Funciones**:
  - Orquestar el flujo completo de monitoreo
  - Integrar resultados de los otros agentes
  - Proporcionar interfaz unificada
  - Ejecutar modo interactivo

## 📊 Interfaz Pandas (`interfaz_pandas.py`)

Interfaz visual para el análisis y presentación de datos:
- Tablero resumen con métricas clave
- Tabla detallada con información formateada
- Análisis temporal por rangos
- Exportación a Excel con múltiples hojas
- Alertas visuales

## 🚀 Instalación

1. Clonar o descargar los archivos
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración de Correo

Edita el archivo `config_email.py` con tus datos:

```python
# Para Gmail (recomendado usar Contraseñas de aplicaciones)
CONFIG_EMAIL_GMAIL = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'remite': 'tu_correo@gmail.com',
    'usuario': 'tu_correo@gmail.com',
    'contraseña': 'tu_contraseña_app'  # No tu contraseña normal
}
```

## 📋 Uso

### Modo Interactivo

```bash
python main.py --interactivo
```

### Línea de Comandos

```bash
# Monitorear dominios específicos
python main.py --dominios google.com github.com microsoft.com

# Con notificaciones por correo
python main.py --dominios google.com github.com --correos admin@tuempresa.com

# Con interfaz pandas completa
python main.py --dominios google.com github.com --interfaz

# Exportar a Excel
python main.py --dominios google.com github.com --exportar reporte.xlsx

# Usar diferente proveedor de correo
python main.py --dominios google.com --proveedor outlook --correos admin@tuempresa.com
```

### Ejemplos de Código

```python
from agente_principal import AgentePrincipal
from interfaz_pandas import InterfazPandas
from config_email import obtener_config_email

# Inicializar sistema
config_email = obtener_config_email('gmail')
agente = AgentePrincipal(config_email)
interfaz = InterfazPandas(agente)

# Monitorear dominios
dominios = ['google.com', 'github.com', 'microsoft.com']
resultados = agente.monitorear_dominios(dominios, ['admin@tuempresa.com'])

# Mostrar interfaz
interfaz.mostrar_interfaz_completa(dominios)

# Exportar reporte
interfaz.exportar_reporte_completo(dominios, 'reporte_dominios.xlsx')
```

## 📈 Criterios de Alerta

- **🚨 Crítico**: Dominios que vencen en 30 días o menos
  - Se envía correo electrónico
  - Se genera entrada en log
  
- **⚠️ Advertencia**: Dominios que vencen entre 31-50 días
  - Solo se registra en el reporte
  - No se envía correo

- **✅ Normal**: Dominios que vencen en más de 50 días
  - Monitoreo continuo sin alertas

## 📁 Archivos Generados

- `sistema_dominios.log`: Log general del sistema
- `dominios_log.txt`: Log de alertas específicas
- `reporte_dominios.csv`: Reporte en formato CSV
- `reporte_dominios_completo.xlsx`: Reporte completo en Excel (si se exporta)

## 🔧 Requisitos

- Python 3.7+
- Conexión a internet para consultas WHOIS
- Configuración de correo para notificaciones (opcional)

## 📝 Notas Importantes

1. **Gmail**: Usa "Contraseñas de aplicaciones" en lugar de tu contraseña normal
2. **Rate Limiting**: Algunos servicios WHOIS tienen límites de consulta
3. **Privacidad**: Las contraseñas se almacenan en texto plano, considera usar variables de entorno en producción
4. **Logs**: El sistema genera logs automáticamente cuando detecta dominios críticos

## 🎯 Características Principales

- ✅ Monitoreo multi-dominio
- ✅ Alertas por correo electrónico
- ✅ Sistema de logs
- ✅ Interfaz visual con pandas
- ✅ Exportación a Excel
- ✅ Modo interactivo
- ✅ Línea de comandos
- ✅ Configuración múltiple de proveedores de correo
- ✅ Análisis temporal avanzado

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - Puedes usar este código libremente.
