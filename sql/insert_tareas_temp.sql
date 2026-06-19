INSERT INTO tareas (id_tarea, nombre_usuario_logeado, id_operario, numero_op, numero_plano, id_producto, id_labor, descripcion, fecha_inicio, fecha_fin, pausas_reanudaciones) VALUES
(1, "Leandro Emanuel Jakimiuk", 1, 101, 201, 1, 1, 'Tarea temporal 1', '2024-01-01 08:00:00', NULL, NULL),
(2, "Leandro Emanuel Jakimiuk", 2, 102, 202, 1, 1, 'Tarea temporal 2', '2024-01-01 08:30:00', NULL, NULL),
(3, "Leandro Emanuel Jakimiuk", 3, 103, 203, 1, 1, 'Tarea temporal 3', '2024-01-01 09:00:00', NULL, NULL),
(4, "Leandro Emanuel Jakimiuk", 4, 104, 204, 1, 1, 'Tarea temporal 4', '2024-01-01 09:30:00', NULL, NULL),
(5, "Leandro Emanuel Jakimiuk", 5, 105, 205, 1, 1, 'Tarea temporal 5', '2024-01-01 10:00:00', NULL, NULL),
(6, "Leandro Emanuel Jakimiuk", 6, 106, 206, 1, 1, 'Tarea temporal 6', '2024-01-01 10:30:00', '2024-01-01 11:00:00', NULL),
(7, "Leandro Emanuel Jakimiuk", 7, 107, 207, 1, 2, 'Tarea temporal 7', '2024-01-01 10:30:00', NULL, NULL),
(8, "Leandro Emanuel Jakimiuk", 8, 108, 208, 1, 2, 'Tarea temporal 8', '2024-01-01 10:30:00', NULL, NULL),
(9, "Leandro Emanuel Jakimiuk", 9, 109, 209, 1, 2, 'Tarea temporal 9', '2024-01-01 10:30:00', NULL, '["2024-01-01 11:00:00"]'),
(10, "Leandro Emanuel Jakimiuk", 9, 110, 210, 1, 2, 'Tarea temporal 10', '2024-01-01 10:30:00', NULL, NULL),
(11, "Leandro Emanuel Jakimiuk", 10, 109, 209, 1, 2, 'Tarea temporal 9', '2024-01-01 10:30:00', NULL, '["2024-01-01 11:00:00"]'),
(12, "Leandro Emanuel Jakimiuk", 10, 110, 210, 1, 2, 'Tarea temporal 10', '2024-01-01 10:30:00', NULL, NULL),
(13, "Leandro Emanuel Jakimiuk", 10, 110, 210, 1, 2, 'Tarea temporal 10', '2024-01-01 10:30:00', NULL, '["2024-01-01 11:00:00","2024-01-01 11:30:00","2024-01-01 11:50:00"]');