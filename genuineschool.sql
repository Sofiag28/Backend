-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 15-10-2025 a las 17:15:58
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `genuineschool`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `grado` int(11) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`id`, `nombre`, `grado`, `descripcion`) VALUES
(1, 'Curso 1', 1, 'Primer grado'),
(2, 'Curso 2', 2, 'Segundo grado'),
(3, 'Curso 3', 3, 'Tercer grado'),
(4, 'Curso 4', 4, 'Cuarto grado'),
(5, 'Curso 5', 5, 'Quinto grado'),
(6, 'Curso 6', 6, 'Sexto grado'),
(7, 'Curso 7', 7, 'Séptimo grado'),
(8, 'Curso 8', 8, 'Octavo grado'),
(9, 'Curso 9', 9, 'Noveno grado'),
(10, 'Curso 10', 10, 'Décimo grado'),
(11, 'Curso 11', 11, 'Once grado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `genero` varchar(10) DEFAULT NULL,
  `fecha_inscripcion` datetime DEFAULT current_timestamp(),
  `password` varchar(255) NOT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'estudiante',
  `id_curso` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`id`, `nombre`, `apellido`, `email`, `genero`, `fecha_inscripcion`, `password`, `rol`, `id_curso`) VALUES
(3, 'matias', 'perez', 'danip@gmail.com', NULL, '2025-10-10 00:00:00', '', 'estudiante', 7),
(4, 'moni', 'patiño', 'monipatio@ho.co', 'Femenino', '2025-10-10 00:00:00', 'scrypt:32768:8:1$HYGPpzX3QwJvi7f6$4bf22816919588782b48a8eb849e28385b2b5c537a587053429eead15bb2c9659472a02bec6061959c0c765b9e3a72f546d25f766b6c2425d09df460ac2364e1', 'estudiante', 9),
(6, 'pep', 'a', 'pep@p.co', 'Masculino', '2025-10-10 00:00:00', 'scrypt:32768:8:1$sSmT5KiJgHYUELmB$612d4008daa9bdc8447bcfe122c4d5ee053674ee2495d1cbe0aaeecfb22f430043223c16266774e09227ff177f16b13b90ee2dc13273bb53c062df6f558ddc6a', 'estudiante', NULL),
(7, 'MARCO', 'PINILLA', 'MARPIN@GMA.CO', 'Otro', '2025-10-11 00:00:00', 'scrypt:32768:8:1$TSiUJ2sXNxsAOeEd$46601af8b429039aef8b3f02cea62e1919e5684090cfe0ee07a84dafabf758c4266dae7b0659d44d7a6d883d01721c140e7dc80c1cfb0c1eafcc63ee6a5a747b', 'estudiante', NULL),
(8, 'sofa', 'umbrella', 'sofaumbre@gmai.co', 'Femenino', '2025-10-11 00:00:00', 'scrypt:32768:8:1$bhmEGzJkTh0imzxg$6ee288f407a4514f91f93282d09c14ecebad9c23dd4d8c1701b426150b0943eb0af2e211a19cc54ae201464a052f34ed9301e9c63e25d831311b9e77b4564fc7', 'estudiante', NULL),
(9, 'edna', 'moda', 'ednamoda@gmail.com', 'Otro', '2025-10-11 00:00:00', 'scrypt:32768:8:1$8V62zUUVsm74dsig$46ff5ee756a7ca835a8dc8cf49a967cf5df19e3474e183f3829126949018916631729f4709e9a97ada932b5b0dab2781e9a5dd70730c488bd5097f6b939a5a71', 'estudiante', NULL),
(10, 'PEDRO', 'PEREZ', 'PEDROPE@GMAIL.COM', 'Otro', '2025-10-11 00:00:00', 'scrypt:32768:8:1$vfVpTZB6MlMNekys$00ebdd08c651ec05a454e629f1c7137046ae40683189df86235e244e4a090bd7821f7ced974d4428e40b293c915ff7a175b50e0e441966d68d688b373f5c0b31', 'estudiante', 9),
(11, 'isabe', 'garcia', 'garciaisabellaia@gmail.com', 'Femenino', '2025-10-11 00:00:00', 'scrypt:32768:8:1$n1E9dvu8i7qZgcFO$633bb1c16951772668425ac22547e59a9c9ce94e7bb580c80b1a8ddbda4a50a71941f88e89411bc9664b2a7d3f519114f2bef26b3a8dce09efef909d79d4c9d3', 'estudiante', 9),
(12, 'piroberta', 'piro', 'pro@ho.coo', 'Otro', NULL, 'scrypt:32768:8:1$Q2i8ziml79McWbHb$fe7077fc7d10a10aa80b1aa564b3ed89e3560f73b16f3ae30854c75a0553f59607b2653200c208cc554f199a7f778905102c7fb5cc31415ec6838f8537e81c3c', 'estudiante', 9),
(13, 'yo', 'yo', 'yoyo@gmail.com', 'Femenino', NULL, 'scrypt:32768:8:1$iRlTzIk8hKZPO9yN$a47bf49b930c3370e86bd947d870e9483daf6cfb163463834052129fa20b1288459092533814d1909b666d549b3383f47cc7a67ec5fa6407e814df7a96c2763a', 'estudiante', 9),
(14, 'jazmin', 'sierra', 'jazminsierra@gmail.co', 'Femenino', '2025-10-12 06:31:14', 'scrypt:32768:8:1$dh4Y9KeYsVebBXC6$18b0dadbcbec904869935fb48f79f6ea2d8613d6eba7a6d41dce67496201c672e25582d8ccefa5de7f9f0fe5aea6a47cc306875bb95dd34aa83442fadac6d794', 'estudiante', 9),
(15, 'yamile', 'porras', 'yamilepo@gmail.co', 'Femenino', '2025-10-12 07:09:14', 'scrypt:32768:8:1$JMIQtN6AjaLraNhD$ceca36ed35ce2563749a551884a12db378df1fff0deb481021ae037c4e1239b1bfd3f617a0a8ef7130f8dd8447b58f31b4d7352150dcd1e73d470a3aa187b516', 'estudiante', 9),
(16, 'daniela', 'manrrique', 'daniman@gmail.co', 'Femenino', '2025-10-12 07:39:58', 'scrypt:32768:8:1$6XZU0Ys0ejVPwCI0$8a2cd30d553107f473fec553e77032a331239a70accfa692af3b861808eb1b74f79e4bdffa41f4b0c455370725af50cbea41756c933c77c69e96c3bcc33b5489', 'estudiante', 9),
(17, 'ursula', 'h', 'ursula@gmail.com', 'Femenino', '2025-10-12 19:07:34', 'scrypt:32768:8:1$XKn6FxGwHc8qKWbp$650b94500914dec94c4103ea44c722c9c508607a63d0de0f02622036fecf01faba0ddd99adbc08fd0b84a8c4befd477dabd821e7fdb07ebcbbe5b12e8a0c4565', 'estudiante', 9),
(18, 'p', 'a', 'paris@gmail.com', 'Masculino', '2025-10-12 20:02:12', 'scrypt:32768:8:1$3VahpRYp97rqg9NV$cb8bff7be907cc67a338abe5a48cef84187619cba2077a1b45d202d02d328aec3aa7187e9ebe3148c3bac507b0a559b515fe96ac5cfa2acb97537f39c60dfb52', 'estudiante', 1),
(19, 'camila', 'patiño', 'camilapa@gmail.com', 'Femenino', '2025-10-13 07:44:53', 'scrypt:32768:8:1$c2bGqB7GSabpQ7ky$053eb1baff842200796473a6b39312e32b9c67d9728e8f1063fe635771caccafbeb0cfbd51e524ca4197a2a3d5244ca920082bf7c647ee63305b1c6a32e2e1ef', 'estudiante', 1),
(20, 'quiero', 'comer', 'quierocomer@gmail', 'Masculino', '2025-10-13 11:25:12', 'scrypt:32768:8:1$MCqDO0z2S0x96yVw$9d1d6efeb99f4967972612a4a5d8ea91c43ecabc712f1808017bdfeb8c8c96c29116ea1474e759bd03464e0158689f90605aa3964759cbd79d13bbab0d030fc6', 'estudiante', 9),
(21, 'care', 'mono ', 'caremono@gmail.com', 'Otro', '2025-10-13 15:58:00', 'scrypt:32768:8:1$iejyZvNE0YkC7P37$6cc8870c8025f4d4e8f2c4622abbba3a8d17be9761c76466b5a71dbe50764b765d705e02645e9d049aaa5155bb985ea7db65118f893130a5f9751f49e74766d2', 'estudiante', 1),
(27, 'maria', 'potillo', 'maria@gmail.com', 'Femenino', '2025-10-14 12:45:53', 'scrypt:32768:8:1$KjTrWCq92qDsVU3b$1d6e77a183cc6f7f3c322c0e02e7dccaa46973cdf3dc907e6293e502579b932e61ce83187e0bcc043839a4de2293e74adc2670d275893ca20c917f6ffee9971d', 'estudiante', 9),
(33, 'laura', 'lauren', 'lauren@gmail.com', 'Femenino', '2025-10-14 13:13:07', 'scrypt:32768:8:1$fELQzafgrj4G4C2m$e63306dd367e90159f5e88e696f2553ff7019eecb24a0a995109f2d6730c86098e736c04cfc78c474dd1eb151b9bb8ef597f7c818035e74cfed619e558b3f69d', 'estudiante', 9),
(42, 'guitarra', 'tambora', 'guitarratambora@gmail.co', 'Masculino', '2025-10-14 20:27:35', 'scrypt:32768:8:1$batVAmMvOn55518d$830aeafc9e30c8f29a39d405677a28447710cc47ed25c0718af10d0f9b4170ac69953e6e97669cbd9e88441426585938f2fb611a57728bb111642b7791717936', 'estudiante', 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `personal`
--

CREATE TABLE `personal` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `rol` enum('profesor','comercial','marketing','admin') NOT NULL,
  `genero` varchar(10) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `personal`
--

INSERT INTO `personal` (`id`, `nombre`, `apellido`, `email`, `rol`, `genero`, `password`) VALUES
(11, 'Laura', 'González', 'laura.gonzalez@edu.com', 'profesor', 'Femenino', '$2b$12$k05.HcezIkrL1w6ThKyV5OCIZWeqU4biZFEQvHbSF85NwMbdTOpMy'),
(12, 'Andrés', 'Mejía', 'andres.mejia@edu.com', 'profesor', 'Masculino', '$2b$12$R0bltkI5jtX4RcXHTJwbDuVyMG5l9M1uSKx.oPx6/NUMGkBXaP/iG'),
(13, 'Valeria', 'Ríos', 'valeria.rios@edu.com', 'profesor', 'Femenino', '$2b$12$SMWSWi/SJmBlEIff2THr6eLFXkiS9CjcACreT6lhzvUrI0xQyC6Pi'),
(14, 'Sebastián', 'Duarte', 'sebastian.duarte@edu.com', 'profesor', 'Masculino', '$2b$12$e42POy50iyqRR1SrcquabuVIrp7/2lkluuDgTdDoq7smF6Tax66o6'),
(15, 'Camila', 'Torres', 'camila.torres@empresa.com', 'comercial', 'Femenino', '$2b$12$OysGvCmCSPZQHq5r/gA.Tewjskvb3uRwBAVzLmwQuCdaOgxa1Y3ZS'),
(16, 'Nicolás', 'Herrera', 'nicolas.herrera@empresa.com', 'comercial', 'Masculino', '$2b$12$eshh/amTsA8sQeZYAnKDXuBxVBKD62JH4ylsJSG.2KimJkp28qo36'),
(17, 'Juliana', 'Peña', 'juliana.pena@empresa.com', 'comercial', 'Femenino', '$2b$12$j4D4Qsnwdr5sP7JDs.S4lemnAFrXNW1skOeiWVlis.3JlHZo7ZaB2'),
(18, 'Daniela', 'Ramírez', 'daniela.ramirez@empresa.com', 'marketing', 'Femenino', '$2b$12$vPUga6ECow5CAJc8fp6zC.fZc22D43HoxGVU46cYPLHd9wofNu1G2'),
(19, 'Samuel', 'Rodríguez', 'samuel.rodriguez@empresa.com', 'marketing', 'Masculino', '$2b$12$qJR14kpXJZIEaxD6fY.RyeY6mT6zifotNdnk7D.F83y.s2Q8Z4ov2'),
(20, 'Natalia', 'Gómez', 'natalia.gomez@empresa.com', 'marketing', 'Femenino', '$2b$12$0xkHKjhgmuzvArhjmuw72uNrqZVx6CyUE0Pg.HygssNHc/1BvDUtW'),
(23, 'Sofía', 'Martínez', 'sofia.martinez@admin.com', 'admin', 'Femenino', '$2b$12$LunWYMyDRjW/Xx95VaepF.5NTgFg1bnEnksDVESt4oj2sltjZQnmO'),
(24, 'Carlos', 'Jiménez', 'carlos.jimenez@admin.com', 'admin', 'Masculino', '$2b$12$97Ok51La.9tKN.OgiU/svuJIfxTHzUKsR43HbKX.g9Tq4NBETlqdK'),
(25, 'Lucía', 'Pérez', 'lucia.perez@admin.com', 'admin', 'Femenino', '$2b$12$FEbZ1GpBt.tpuAqge5lpx.624fteYLtSB5b0BTewoZGUa7ocoOiCO'),
(26, 'Julián', 'Vargas', 'julian.vargas@admin.com', '', 'Masculino', '$2b$12$MyEYW.fRp8v68tFAyVfyuOHfnb20hYa2jPKVGwNjHpjhmrLmRHO2K'),
(27, 'Mariana', 'López', 'mariana.lopez@admin.com', '', 'Femenino', '$2b$12$DwUqi/ije4CiFGEgExFkPuOt3vR9pDvyb1cZ1avm2cJsBOryypV4m'),
(29, 'Mariana', 'Suárez', 'mariana.suarez@admin.com', '', 'Femenino', '$2b$12$a0lYxLazarHdlQOEc9mgI.lI.Xnzgjs3YWbk/8DGraGf2dx0P.e9u'),
(30, 'Andrés', 'Castillo', 'andres.castillo@admin.com', '', 'Masculino', '$2b$12$YGZQcWfuvw.Fja06lZAtkeuGzExB/lucouiqJEYWVwsyo9keOLwMG'),
(31, 'Valentina', 'Moreno', 'valentina.moreno@admin.com', '', 'Femenino', '$2b$12$Hb5j7uvy8wxRVvc8ZVUKTeSnb.F9K87WiroqVs36P/CWyr5UHOdwu'),
(32, 'Felipe', 'García', 'felipe.garcia@admin.com', '', 'Masculino', '$2b$12$uT2Sj//1l/xVzLteXJSqGeHHegZmHnFki8QrfaqUGatr0Apf1Q5fm'),
(33, 'Laura', 'Benítez', 'laura.benitez@admin.com', '', 'Femenino', '$2b$12$Oe2MjGUwiWYgrfCxJWJSgOtw2wIoYrUw65xrv0CUt.9C3qqQ0es.C'),
(34, 'Sara', 'patiño', 'saara.suarezp@admin.com', 'admin', 'Femenino', '$2b$12$EwD4y4vGSWUqVeQBH4llS.s2G8U3NfwGH59pEuJDqCpgTkVXsJz8G'),
(35, 'cami', 'Cas', 'andresca.lo@admin.com', 'admin', 'Masculino', '$2b$12$7ex5AaHKkHwtjWXeZM47nuAtytRHJT0Nralj6PSCjFaOlQs7YkRvC'),
(36, 'yamile', 'jajaja', 'ya@ga.co', '', NULL, '12345');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `estado` enum('pendiente','en_progreso','completada') DEFAULT 'pendiente',
  `fecha_entrega` date DEFAULT NULL,
  `id_curso` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id`, `titulo`, `descripcion`, `estado`, `fecha_entrega`, `id_curso`) VALUES
(8, 'lectura de fotosintesis', 'Leer el capítulo 4 del libro', 'en_progreso', '2025-10-31', 1),
(9, 'papear', 'Prepno', NULL, '2025-11-01', 1),
(21, 'correr', 'toda la cancha', 'pendiente', '2025-10-31', 1),
(22, 'correr', 'toda la cancha', 'completada', '2025-10-31', 1),
(23, 'correr', 'toda la cancha', 'pendiente', '2025-10-31', 1),
(24, 'correr', 'toda la cancha', 'pendiente', '2025-10-31', 1),
(26, 'Tarea 199999999', 'Descripción de prueba', 'completada', '2025-10-20', 1),
(27, 'po', 'q', 'completada', '2025-10-24', 1),
(28, 'correr', 'una cuadra', 'pendiente', '2025-10-24', 4),
(30, 'caminar ', 'caminar una cuadra', 'pendiente', '2025-10-23', 4),
(38, 'CORRER', 'no', 'pendiente', '2025-10-25', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas_estudiantes`
--

CREATE TABLE `tareas_estudiantes` (
  `id` int(11) NOT NULL,
  `id_tarea` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `estado` enum('pendiente','completada') DEFAULT 'pendiente',
  `fecha_actualizacion` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tareas_estudiantes`
--

INSERT INTO `tareas_estudiantes` (`id`, `id_tarea`, `id_estudiante`, `estado`, `fecha_actualizacion`) VALUES
(1, 38, 3, 'pendiente', '2025-10-14 14:58:24');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `contraseña` varchar(255) DEFAULT NULL,
  `rol` enum('admin','personal','estudiante') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `username`, `contraseña`, `rol`) VALUES
(5, 'Maria', 'scrypt:32768:8:1$EMRlAkV9QwbxP0SF$cbdf83c5722fa69ad369549138646bc9b90a3795f223067f127bb48985f179895508a620b30a8cf0e5cfb4cc3310b5fffa27ff36a50c416c114a1042586f3625', 'admin');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `fk_estudiante_curso` (`id_curso`);

--
-- Indices de la tabla `personal`
--
ALTER TABLE `personal`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_tarea_curso` (`id_curso`);

--
-- Indices de la tabla `tareas_estudiantes`
--
ALTER TABLE `tareas_estudiantes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_tarea` (`id_tarea`,`id_estudiante`),
  ADD KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT de la tabla `personal`
--
ALTER TABLE `personal`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `tareas_estudiantes`
--
ALTER TABLE `tareas_estudiantes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `fk_estudiante_curso` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id`);

--
-- Filtros para la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD CONSTRAINT `fk_tarea_curso` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id`);

--
-- Filtros para la tabla `tareas_estudiantes`
--
ALTER TABLE `tareas_estudiantes`
  ADD CONSTRAINT `tareas_estudiantes_ibfk_1` FOREIGN KEY (`id_tarea`) REFERENCES `tareas` (`id`),
  ADD CONSTRAINT `tareas_estudiantes_ibfk_2` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
