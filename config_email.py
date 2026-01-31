"""
Configuración de correo electrónico para el sistema de monitoreo
"""

# Configuración del servidor SMTP
CONFIG_EMAIL_GMAIL = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'remite': 'juandavidvc801@gmail.com', 
    'usuario': 'juandavidvc801@gmail.com',  
    'contraseña': 'rnpi cacg elht qbgy'  
}


# Configuración por defecto (puedes cambiarla)
CONFIG_DEFAULT = CONFIG_EMAIL_GMAIL

def obtener_config_email(proveedor: str = 'gmail') -> dict:
    """
    Obtiene la configuración de correo según el proveedor
    
    Args:
        proveedor: 'gmail', 'outlook', 'yahoo'
        
    Returns:
        Diccionario con configuración del proveedor
    """
    proveedores = {
        'gmail': CONFIG_EMAIL_GMAIL,
    }
    
    return proveedores.get(proveedor.lower(), CONFIG_DEFAULT)

def configurar_correo_manual(smtp_server: str, smtp_port: int, 
                           remite: str, usuario: str, contraseña: str) -> dict:
    """
    Crea una configuración de correo manual
    
    Args:
        smtp_server: Servidor SMTP
        smtp_port: Puerto SMTP
        remite: Correo remitente
        usuario: Usuario de autenticación
        contraseña: Contraseña
        
    Returns:
        Diccionario con configuración personalizada
    """
    return {
        'smtp_server': smtp_server,
        'smtp_port': smtp_port,
        'remite': remite,
        'usuario': usuario,
        'contraseña': contraseña
    }
