from datetime import datetime

def calcular_tiempo_cronometrado(fecha_inicio, fecha_fin, pausas_reanudaciones):
    """
    Calcula el tiempo cronometrado (en segundos) de una tarea, considerando pausas y reanudaciones.
    
    Lógica:
    - Array de pausas_reanudaciones alternado: [pausa, reanudacion, pausa, reanudacion, ...]
    - Posiciones PARES (0, 2, 4, ...) = momentos de PAUSA
    - Posiciones IMPARES (1, 3, 5, ...) = momentos de REANUDACIÓN
    
    Cálculo de tiempo ACTIVO:
    - fecha_inicio -> pausas[0] = ACTIVO
    - pausas[0] -> pausas[1] = PAUSADO
    - pausas[1] -> pausas[2] = ACTIVO
    - pausas[2] -> pausas[3] = PAUSADO
    - pausas[3] -> fecha_fin (si existe) = ACTIVO
    
    Si len(pausas) es PAR (2,4,6...) el último índice es IMPAR (1,3,5...) = última acción fue REANUDACIÓN
    Si len(pausas) es IMPAR (1,3,5...) el último índice es PAR (0,2,4...) = última acción fue PAUSA
    
    Args:
        fecha_inicio (datetime): Momento de inicio de la tarea
        fecha_fin (datetime): Momento de fin de la tarea. Si es None, usa datetime.now()
        pausas_reanudaciones (list): Array con timestamps alternados de pausas y reanudaciones
        
    Returns:
        int: Tiempo en segundos que la tarea estuvo activa
    """
    
    if fecha_fin is None:
        fecha_fin = datetime.now()
    
    # Si no hay pausas, el tiempo activo es la diferencia total
    if not pausas_reanudaciones or len(pausas_reanudaciones) == 0:
        return int((fecha_fin - fecha_inicio).total_seconds())
    
    tiempo_activo = 0
    
    # Convertir strings a datetime si es necesario
    pausas = []
    for pausa_str in pausas_reanudaciones:
        if isinstance(pausa_str, str):
            pausas.append(datetime.fromisoformat(pausa_str))
        else:
            pausas.append(pausa_str)
    
    # Tiempo desde inicio hasta la primera pausa (índice 0)
    tiempo_activo += int((pausas[0] - fecha_inicio).total_seconds())
    
    # Tiempo entre cada reanudación (índices impares) y la siguiente pausa (índices pares)
    # Vamos iterando: 1->2, 3->4, 5->6, etc.
    for i in range(1, len(pausas) - 1, 2):
        # pausas[i] es reanudación, pausas[i+1] es siguiente pausa
        tiempo_activo += int((pausas[i + 1] - pausas[i]).total_seconds())
    
    # Si len(pausas) es PAR, el último índice es IMPAR (reanudación)
    # Hay tiempo activo desde la última reanudación hasta fecha_fin
    if len(pausas) % 2 == 0:
        tiempo_activo += int((fecha_fin - pausas[-1]).total_seconds())
    
    return tiempo_activo


def formato_hhmmss(segundos):
    """
    Convierte segundos a formato HH:MM:SS.
    
    Args:
        segundos (int): Tiempo en segundos
        
    Returns:
        str: Tiempo en formato HH:MM:SS
    """
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    secs = segundos % 60
    return f"{horas:02d}:{minutos:02d}:{secs:02d}"
