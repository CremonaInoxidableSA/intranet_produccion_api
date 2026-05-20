INSERT INTO usuarios (id, usuario, nombre, apellido, email, rol, password_hash, habilitado, fecha_creacion) VALUES
(1, 'admin', 'Administrador', 'Sistema', 'admin@cremona.com', 'admin', NULL, 1, NOW()),
(2, 'operador1', 'Juan', 'Pérez', 'jperez@cremona.com', 'operador', NULL, 1, NOW());

INSERT INTO tareas (id_tarea, titulo, descripcion, estado, prioridad, completada, fecha_creacion, fecha_vencimiento, id_usuario) VALUES
(1, 'Configurar entorno', 'Configurar el entorno de producción inicial', 'pendiente', 'alta', 0, NOW(), NULL, 1),
(2, 'Revisión diaria', 'Revisar logs del sistema diariamente', 'pendiente', 'normal', 0, NOW(), NULL, 2);
