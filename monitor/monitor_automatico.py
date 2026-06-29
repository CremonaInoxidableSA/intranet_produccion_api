import threading
import time
import logging
import json
import os
from datetime import datetime
from config.db import SessionLocal
from models.tareas import Tareas
from sqlalchemy.orm.attributes import flag_modified

logger = logging.getLogger("uvicorn")

class MonitorTareasAutomatico:
    """Monitor que ejecuta pausas y reanudaciones automáticas de tareas"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.ultima_ejecucion_930 = None
        self.ultima_ejecucion_940 = None
        self.ultima_ejecucion_1300 = None
        self.ultima_ejecucion_1330 = None
        self.ultima_ejecucion_1600 = None
        self.archivo_pausadas13hs = "monitor/pausadas13hs.json"
        self.archivo_pausadas930hs = "monitor/pausadas930hs.json"
        
    def iniciar(self):
        """Inicia el monitor en un thread separado"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._ejecutar_monitor, daemon=True)
            self.thread.start()
            logger.info("Monitor automático de tareas iniciado")
    
    def detener(self):
        """Detiene el monitor"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Monitor automático de tareas detenido")
    
    def _ejecutar_monitor(self):
        """Ejecuta continuamente el monitor"""
        while self.running:
            try:
                self._verificar_y_ejecutar()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Error en monitor automático: {str(e)}")
                time.sleep(60)
    
    def _verificar_y_ejecutar(self):
        """Verifica los diferentes rangos de tiempo y ejecuta acciones"""
        ahora = datetime.now()
        
        if ahora.hour == 9 and 29 <= ahora.minute <= 31:
            if not self.ultima_ejecucion_930 or self.ultima_ejecucion_930.date() != ahora.date():
                self.ultima_ejecucion_930 = ahora
                self._pausar_y_guardar_930hs()
        
        elif ahora.hour == 9 and 39 <= ahora.minute <= 41:
            if not self.ultima_ejecucion_940 or self.ultima_ejecucion_940.date() != ahora.date():
                self.ultima_ejecucion_940 = ahora
                self._reanudar_desde_json_940()

        if (ahora.hour == 12 and ahora.minute >= 59) or (ahora.hour == 13 and ahora.minute <= 1):
            if not self.ultima_ejecucion_1300 or self.ultima_ejecucion_1300.date() != ahora.date():
                self.ultima_ejecucion_1300 = ahora
                self._pausar_y_guardar_13hs()
        
        elif (ahora.hour == 13 and 29 <= ahora.minute <= 31):
            if not self.ultima_ejecucion_1330 or self.ultima_ejecucion_1330.date() != ahora.date():
                self.ultima_ejecucion_1330 = ahora
                self._reanudar_desde_json_1330()
        
        if (ahora.hour == 15 and ahora.minute >= 59) or (ahora.hour == 16 and ahora.minute <= 1):
            if not self.ultima_ejecucion_1600 or self.ultima_ejecucion_1600.date() != ahora.date():
                self.ultima_ejecucion_1600 = ahora
                self._pausar_todas_las_tareas_activas(guardar_listado=False)
    
    def _pausar_y_guardar_930hs(self):
        """Pausa todas las tareas activas y guarda sus IDs en JSON"""
        db = SessionLocal()
        try:
            tareas_activas = db.query(Tareas).filter(
                Tareas.estado == "activa",
                Tareas.fecha_fin == None
            ).all()
            
            if not tareas_activas:
                logger.info("No hay tareas activas para pausar en rango 9:29-9:31")
                return
            
            ids_pausadas = []
            timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for tarea in tareas_activas:
                try:
                    pausas = tarea.pausas_reanudaciones if tarea.pausas_reanudaciones else []
                    pausas.append(timestamp_actual)
                    tarea.pausas_reanudaciones = pausas
                    flag_modified(tarea, "pausas_reanudaciones")
                    tarea.estado = "pausada"
                    
                    ids_pausadas.append(tarea.id_tarea)
                    
                except Exception as e:
                    logger.error(f"Error al pausar tarea {tarea.id_tarea}: {str(e)}")
            
            db.commit()
            
            # Guarda el JSON con fecha del día actual
            datos_json = {
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "ids_tareas": ids_pausadas
            }
            
            with open(self.archivo_pausadas930hs, 'w') as f:
                json.dump(datos_json, f, indent=2)
            
            logger.info(f"Pausa automática 09:29-09:31 - {len(ids_pausadas)} tareas pausadas y guardadas en JSON")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en pausa automática 09:29-09:31: {str(e)}")
        finally:
            db.close()

    def _reanudar_desde_json_940(self):
        """Reanuda las tareas que fueron pausadas (desde el JSON)"""
        db = SessionLocal()
        try:
            # Verifica si el archivo existe
            if not os.path.exists(self.archivo_pausadas930hs):
                logger.info("No hay archivo de tareas pausadas a las 09:40")
                return
            
            # Lee el JSON
            with open(self.archivo_pausadas930hs, 'r') as f:
                datos_json = json.load(f)
            
            fecha_guardada = datos_json.get("fecha")
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            if fecha_guardada != fecha_actual:
                logger.info(f"Archivo de pausadas es del {fecha_guardada}, no del día actual. Borrando contenido.")
                with open(self.archivo_pausadas930hs, 'w') as f:
                    json.dump({"fecha": "", "ids_tareas": []}, f)
                return
            
            ids_tareas = datos_json.get("ids_tareas", [])
            
            if not ids_tareas:
                logger.info("No hay tareas para reanudar en el JSON")
                return
            
            cantidad_reanudadas = 0
            timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for id_tarea in ids_tareas:
                try:
                    tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
                    
                    # Si no encuentra la tarea o ya está finalizada, ignora
                    if not tarea or tarea.fecha_fin is not None:
                        logger.warning(f"Tarea {id_tarea} no encontrada o ya finalizada, ignorando")
                        continue
                    
                    # Reanuda la tarea
                    pausas = tarea.pausas_reanudaciones if tarea.pausas_reanudaciones else []
                    pausas.append(timestamp_actual)
                    tarea.pausas_reanudaciones = pausas
                    flag_modified(tarea, "pausas_reanudaciones")
                    tarea.estado = "activa"
                    
                    cantidad_reanudadas += 1
                    
                except Exception as e:
                    logger.error(f"Error al reanudar tarea {id_tarea}: {str(e)}")
            
            db.commit()
            
            # Borra el contenido del JSON
            with open(self.archivo_pausadas930hs, 'w') as f:
                json.dump({"fecha": "", "ids_tareas": []}, f)
            
            logger.info(f"Reanudación automática 09:39-09:41 - {cantidad_reanudadas} tareas reanudadas")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en reanudación automática 09:39-09:41: {str(e)}")
        finally:
            db.close()

    def _pausar_y_guardar_13hs(self):
        """Pausa todas las tareas activas y guarda sus IDs en JSON"""
        db = SessionLocal()
        try:
            tareas_activas = db.query(Tareas).filter(
                Tareas.estado == "activa",
                Tareas.fecha_fin == None
            ).all()
            
            if not tareas_activas:
                logger.info("No hay tareas activas para pausar en rango 12:59-13:01")
                return
            
            ids_pausadas = []
            timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for tarea in tareas_activas:
                try:
                    # Pausa la tarea
                    pausas = tarea.pausas_reanudaciones if tarea.pausas_reanudaciones else []
                    pausas.append(timestamp_actual)
                    tarea.pausas_reanudaciones = pausas
                    flag_modified(tarea, "pausas_reanudaciones")
                    tarea.estado = "pausada"
                    
                    # Guarda el ID
                    ids_pausadas.append(tarea.id_tarea)
                    
                except Exception as e:
                    logger.error(f"Error al pausar tarea {tarea.id_tarea}: {str(e)}")
            
            db.commit()
            
            # Guarda el JSON con fecha del día actual
            datos_json = {
                "fecha": datetime.now().strftime("%Y-%m-%d"),
                "ids_tareas": ids_pausadas
            }
            
            with open(self.archivo_pausadas13hs, 'w') as f:
                json.dump(datos_json, f, indent=2)
            
            logger.info(f"Pausa automática 12:59-13:01 - {len(ids_pausadas)} tareas pausadas y guardadas en JSON")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en pausa automática 12:59-13:01: {str(e)}")
        finally:
            db.close()
    
    def _reanudar_desde_json_1330(self):
        """Reanuda las tareas que fueron pausadas (desde el JSON)"""
        db = SessionLocal()
        try:
            # Verifica si el archivo existe
            if not os.path.exists(self.archivo_pausadas13hs):
                logger.info("No hay archivo de tareas pausadas a las 13:00")
                return
            
            # Lee el JSON
            with open(self.archivo_pausadas13hs, 'r') as f:
                datos_json = json.load(f)
            
            fecha_guardada = datos_json.get("fecha")
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            
            # Verifica que sea del día actual
            if fecha_guardada != fecha_actual:
                logger.info(f"Archivo de pausadas es del {fecha_guardada}, no del día actual. Borrando contenido.")
                # Borra el contenido del JSON
                with open(self.archivo_pausadas13hs, 'w') as f:
                    json.dump({"fecha": "", "ids_tareas": []}, f)
                return
            
            ids_tareas = datos_json.get("ids_tareas", [])
            
            if not ids_tareas:
                logger.info("No hay tareas para reanudar en el JSON")
                return
            
            cantidad_reanudadas = 0
            timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for id_tarea in ids_tareas:
                try:
                    tarea = db.query(Tareas).filter(Tareas.id_tarea == id_tarea).first()
                    
                    # Si no encuentra la tarea o ya está finalizada, ignora
                    if not tarea or tarea.fecha_fin is not None:
                        logger.warning(f"Tarea {id_tarea} no encontrada o ya finalizada, ignorando")
                        continue
                    
                    # Reanuda la tarea
                    pausas = tarea.pausas_reanudaciones if tarea.pausas_reanudaciones else []
                    pausas.append(timestamp_actual)
                    tarea.pausas_reanudaciones = pausas
                    flag_modified(tarea, "pausas_reanudaciones")
                    tarea.estado = "activa"
                    
                    cantidad_reanudadas += 1
                    
                except Exception as e:
                    logger.error(f"Error al reanudar tarea {id_tarea}: {str(e)}")
            
            db.commit()
            
            # Borra el contenido del JSON
            with open(self.archivo_pausadas13hs, 'w') as f:
                json.dump({"fecha": "", "ids_tareas": []}, f)
            
            logger.info(f"Reanudación automática 13:29-13:31 - {cantidad_reanudadas} tareas reanudadas")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en reanudación automática 13:29-13:31: {str(e)}")
        finally:
            db.close()
    
    def _pausar_todas_las_tareas_activas(self, guardar_listado=False):
        """Pausa todas las tareas en estado activa"""
        db = SessionLocal()
        try:
            tareas_activas = db.query(Tareas).filter(
                Tareas.estado == "activa",
                Tareas.fecha_fin == None
            ).all()
            
            if not tareas_activas:
                logger.info("No hay tareas activas para pausar en rango 15:59-16:01")
                return
            
            cantidad_pausadas = 0
            timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for tarea in tareas_activas:
                try:
                    pausas = tarea.pausas_reanudaciones if tarea.pausas_reanudaciones else []
                    pausas.append(timestamp_actual)
                    tarea.pausas_reanudaciones = pausas
                    flag_modified(tarea, "pausas_reanudaciones")
                    tarea.estado = "pausada"
                    
                    cantidad_pausadas += 1
                    
                except Exception as e:
                    logger.error(f"Error al pausar tarea {tarea.id_tarea}: {str(e)}")
            
            db.commit()
            
            logger.info(f"Pausa automática 15:59-16:01 - {cantidad_pausadas} tareas pausadas")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error en pausa automática 15:59-16:01: {str(e)}")
        finally:
            db.close()

monitor_automatico = MonitorTareasAutomatico()

def iniciar_monitor_pausas():
    """Inicia el monitor automático"""
    monitor_automatico.iniciar()


def detener_monitor_pausas():
    """Detiene el monitor automático"""
    monitor_automatico.detener()