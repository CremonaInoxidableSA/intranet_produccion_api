INSERT INTO tareas (id_tarea, id_usuario_logeado, nombre_usuario_logeado, apellido_usuario_logeado, id_operario_seleccionado, nombre_operario_seleccionado, apellido_operario_seleccionado, numero_op, numero_plano, id_producto, id_labor, descripcion, fecha_inicio, fecha_fin, duracion_tarea, pausas_reanudaciones) VALUES
(1, 1, "Leandro", "Jakimiuk", 1, "Juan", "Perez", 101, 201, 1, 1, 'Tarea sin pausas', '2024-01-01 08:00:00', NULL, 0, NULL),
(2, 1, "Leandro", "Jakimiuk", 2, "Carlos", "Garcia", 102, 202, 1, 1, 'Tarea con 1 pausa', '2024-01-01 08:30:00', NULL, 1800, '["2024-01-01 09:00:00"]'),
(3, 1, "Leandro", "Jakimiuk", 3, "Maria", "Lopez", 103, 203, 1, 1, 'Tarea con 2 pausas', '2024-01-01 09:00:00', NULL, 3600, '["2024-01-01 09:30:00","2024-01-01 10:00:00"]'),
(4, 1, "Leandro", "Jakimiuk", 4, "Ana", "Martinez", 104, 204, 1, 2, 'Tarea con 3 pausas', '2024-01-01 09:30:00', NULL, 5400, '["2024-01-01 10:00:00","2024-01-01 10:30:00","2024-01-01 11:00:00"]'),
(5, 1, "Leandro", "Jakimiuk", 5, "Roberto", "Sanchez", 105, 205, 1, 2, 'Tarea con 4 pausas', '2024-01-01 10:00:00', NULL, 7200, '["2024-01-01 10:30:00","2024-01-01 11:00:00","2024-01-01 11:30:00","2024-01-01 12:00:00"]');
