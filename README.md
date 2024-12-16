El proyecto se encuentra desarrollado con **Fastapi**, utilizado dentro de un ambiente de desarrollo con **Docker**, y utilizando la imagen de **Python 3.13**.



## Index

- [Index](#index)
- [1. Setup - Primer uso](#1-setup---primer-uso)
  - [1.1 Prerrequisitos](#11-prerrequisitos)
  - [1.2 Clona el repositorio](#12-clona-el-repositorio)
  - [1.3 Variables de entorno](#13-variables-de-entorno)
  - [1.4 Instalación de dependencias (Opcional)](#14-instalación-de-dependencias-opcional)
- [2. Levantar contenedor](#2-levantar-contenedor)
  - [2.1 Comandos dentro del contenedor](#21-comandos-dentro-del-contenedor)
- [3. Descripción de servicios basicos](#3-descripción-de-servicios-basicos)
- [4. Explicación de Decisiones de Diseño](#4-explicación-de-decisiones-de-diseño)
  - [4.1 Modularidad](#41-modularidad)
  - [4.2 Uso de Plantillas](#42-uso-de-plantillas)
  - [4.3 Validación y Extensibilidad](#43-validación-y-extensibilidad)
  - [4.4 Tipado de Entradas y Salidas](#44-tipado-de-entradas-y-salidas)
  - [4.5 Documentación con Docstrings](#45-documentacion-con-docstrings)
  - [4.6 Despliegue con Docker](#46-despliegue-con-docker)
  - [4.7 Base de Datos MongoDB](#47-base-de-datos-mongoDB)
  - [4.8 Generación de Assertions](#48-generacion-de-assertions)

<br />

## 1. Setup - Primer uso

### 1.1 Prerrequisitos

- [Docker](https://docs.docker.com/engine/install/)
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
- [Python 3.13](https://www.python.org/)



### 1.2 Clona el repositorio

Empezar clonando el repo y usando la branch **DEV**:

```bash
git clone git@github.com:amartilotta/event-tester.git
```

### 1.3 Variables de entorno

Para este paso es necesario ejecutar los dos siguientes scripts:

```bash
cp example.env .env

```

Dentro de los mismos se hara lo siguiente:

- Cargar **variables de entorno** para el proyecto.


### 1.4 Instalación de dependencias (Opcional)

Para instalar las dependencias del proyecto es necesario **ejecutar** el siguiente comando en la **raíz** del proyecto:

```bash
poetry env use 3.13
poetry install
```

Ahora para utilizar el entorno de desarrollo es necesario **activar** el **entorno** virtual con el siguiente comando:

```bash
poetry shell
```


Ahora en el **IDE** seleccionar el **entorno** virtual que se encuentra en la **raíz** del proyecto.


- Presionar: `Ctrl + Shift + P`
- Busca: `> Python: Select Interpreter`
- Seleccionar el entorno virtual `defaultInterpreterPath` o en su defecto `./venv`


Esto solo nos beneficiara para el desarrollo del proyecto, ya que nos permitirá utilizar las **dependencias** instaladas dentro de **docker**.



## 2. Levantar contenedor

Para utilizar el contenedor es necesario **ejecutar** el siguiente comando en la **raíz** del proyecto:

```bash
docker compose up
```
o en su defecto para dejarlo corriendo en segundo plano
```bash
docker compose up -d
```

Si se siguieron los pasos hasta este punto, ya puedes entrar al proyecto desde el puerto 8450:

[**http://localhost:8450/docs**](http://localhost:8450/docs)


> 💡 **Tip:** En caso de necesitar una instalación **limpia**. Es posible utilizar make fresh-install antes de ejecutar el contenedor para que se instalen las dependencias desde cero.


### 2.1 Comandos dentro del contenedor

Para utilizar **comandos** específicos en el **contenedor** de docker, se hara de la siguiente forma:

```bash
sh scripts/shell.sh <tu-comando>
```

> 📌 **Info:** No es necesario remplazar \<tu-comando> . Si se deja vacío, se mostrara la terminal del contenedor teniendo libertad dentro del mismo


## 3. Descripción de servicios basicos

Toda la parte de **documentación** de la **API** se encuentra en [**`docs`**](http://localhost:8450/docs)

Los servicios más utilizados son:

| Resumen de servicio               | Método | URL                |
| --------------------------------- | ------ | ------------------ |
| Obtener historias de usuario      |   GET  | /stories           |
| Generar pruebas                   |   GET  | /test              |
| Obtener eventos agrupados         |   GET  | /grouped-events    |
| Obtener patrones                  |   GET  | /patterns          |



## 4. Explicación de Decisiones de Diseño

Arquitectura del Proyecto

### 4.1 Modularidad:

Se implementó un **EventService** para manejar el almacenamiento y la validación de eventos.

Un **UserStoryService** para la agrupación de eventos y la identificación de patrones.

Un **PlaywrightTestGenerator** dedicado a la generación de tests automatizados basados en las historias de usuario.

### 4.2 Uso de Plantillas:

Se utilizó **Jinja2** para crear un sistema flexible de generación de código en los tests de Playwright.

### 4.3 Validación y Extensibilidad:

El sistema admite fácilmente nuevos tipos de acciones gracias a su diseño orientado a plantillas y lógica centralizada.

### 4.4 Tipado de Entradas y Salidas:

Se definieron tipos explícitos en los controladores, lo cual garantiza que los datos que ingresan y salen de los endpoints sean los esperados.

Esto también facilita la generación automática de documentación con **Swagger**.

### 4.5 Documentación con Docstrings:

Todas las funciones principales están documentadas con **docstrings** para mayor claridad y mantenibilidad.

### 4.6 Despliegue con Docker:

La aplicación está configurada para ejecutarse dentro de contenedores **Docker**, lo que facilita su despliegue y portabilidad.

### 4.7 Base de Datos MongoDB:

Se eligió **MongoDB** como base de datos para manejar grandes volúmenes de eventos de manera eficiente y flexible.

### 4.8 Generación de Assertions

Se incluyeron assertions relevantes en los tests:

Acciones de **clic**: Se verifica que la navegación sea correcta si se espera un cambio de URL.

**Entradas (input)**: Se valida que los valores ingresados coincidan con los esperados.

**Navegación**: Se asegura que la URL sea la correcta después de una acción de goto.

## 5. Trade-offs Considerados

**Almacenamiento de Eventos**

Base de datos (MongoDB):

Ofrece persistencia y mejor manejo de grandes volúmenes de datos.

Requiere configuración adicional, pero mejora la escalabilidad.

**Generación Dinámica de Tests**

Jinja2 (actual):

Flexible y simple para generación de código.

Menos estricta en validación de sintaxis del código generado.

Builders específicos (opción futura):

Permitirían generar código con estructuras más robustas.

Serían más complejos de implementar.

**Complejidad de Assertions**

Assertions actuales:

Cubre los casos más comunes de navegación y validación de entradas.

Assertions avanzadas (futuro):

Podrían incluir verificaciones de cambios en el DOM o validaciones visuales (capturas de pantalla).

## 6. Áreas de Mejora Identificadas

**Testing y Validación:**

Automatizar tests para validar que los tests generados se ejecutan correctamente.

**Interfaz de Usuario:**

Crear una interfaz gráfica para visualizar y editar las historias de usuario antes de generar los tests.

**Optimización de Assertions:**

Introducir validaciones más avanzadas como comprobaciones de estado del DOM o capturas de pantalla.