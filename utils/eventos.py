from datetime import datetime

def procesar_eventos(pausas_reanudaciones):
    """Procesa el array de pausas_reanudaciones y lo convierte en un array de eventos.
    
    Estructura esperada de pausas_reanudaciones:
    - Array de objetos con estructura {"datetime": "...", "type": "pausa|reanudacion"}
    - O array alternado donde índices pares son pausas e impares son reanudaciones
    
    Retorna un array de objetos con estructura {"fecha": "...", "titulo": "pausa|reanudacion"}
    Si no existe o está vacío, retorna []
    """
    if not pausas_reanudaciones:
        return []
    
    eventos = []
    
    for index, evento in enumerate(pausas_reanudaciones):
        if isinstance(evento, dict):
            datetime_str = evento.get("datetime") or evento.get("timestamp") or str(evento)
            
            if "type" in evento:
                tipo = evento["type"]
            else:
                tipo = "pausa" if index % 2 == 0 else "reanudacion"
        else:
            # Si es un string o timestamp directo
            datetime_str = str(evento)
            tipo = "pausa" if index % 2 == 0 else "reanudacion"
        
        eventos.append({
            "fecha": datetime_str,
            "titulo": tipo
        })
    
    return eventos