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
- [4. Explicación de Decisiones de Diseño](#4-explicación-de-decisiones-de-diseño-✨)
  - [4.1 Modularidad](#🔗-41-modularidad)
  - [4.2 Uso de Plantillas](#📄-42-uso-de-plantillas)
  - [4.3 Validación y Extensibilidad](#✅-43-validación-y-extensibilidad)
  - [4.4 Tipado de Entradas y Salidas](#🎯-44-tipado-de-entradas-y-salidas)
  - [4.5 Documentación con Docstrings](#📚-45-documentación-con-docstrings)
  - [4.6 Despliegue con Docker](#🐋-46-despliegue-con-docker)
  - [4.7 Base de Datos MongoDB](#📦-47-base-de-datos-mongodb)
  - [4.8 Generación de Assertions](#⚙️-48-generación-de-assertions)
- [5. Trade-offs Considerados](#5-trade-offs-considerados-✨)
  - [5.1 Almacenamiento de Eventos](#📂-51-almacenamiento-de-eventos)
  - [5.2 Generación Dinámica de Tests](#🛠️-52-generación-dinámica-de-tests)
  - [5.3 Complejidad de Assertions](#🔍-53-complejidad-de-assertions)
- [6. Áreas de Mejora Identificadas](#6-áreas-de-mejora-identificadas-🚀)
  - [6.1 Testing y Validación](#🔧-61-testing-y-validación)
  - [6.2 Optimización de Assertions](#⚡-62-optimización-de-assertions)
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



## 4. Explicación de Decisiones de Diseño ✨

La arquitectura del proyecto se diseñó teniendo en cuenta principios clave para garantizar su modularidad, extensibilidad y capacidad de mantenimiento.

---

### **🔗 4.1 Modularidad**

Se implementaron los siguientes servicios para organizar las responsabilidades:
- **EventService**: Maneja el almacenamiento y la validación de eventos.
- **UserStoryService**: Agrupa eventos y permite identificar patrones en las historias de usuario.
- **PlaywrightTestGenerator**: Dedicado exclusivamente a la generación automatizada de tests basados en las historias de usuario.

Este diseño asegura una separación clara de responsabilidades, lo que facilita la ampliación y el mantenimiento del sistema.

---

### **📄 4.2 Uso de Plantillas**

Para la generación de código en los tests de Playwright, se utilizó **Jinja2**, una herramienta poderosa que permite crear plantillas dinámicas. Esto aporta:
- **Flexibilidad**: Generación de código adaptable a diferentes escenarios.
- **Reutilización**: Permite mantener un sistema consistente y eficiente para la creación de tests.

---

### **✅ 4.3 Validación y Extensibilidad**

El sistema está diseñado para admitir fácilmente nuevos tipos de acciones gracias a:
- **Plantillas modulares**: Permiten añadir nuevas acciones sin modificar la lógica central.
- **Validación centralizada**: Asegura que todos los datos cumplan con los requisitos establecidos antes de ser procesados.

---

### **🎯 4.4 Tipado de Entradas y Salidas**

Se definieron tipos explícitos en los controladores utilizando **Pydantic**, garantizando que:
- Los datos de entrada y salida sean consistentes.
- Se facilite la generación automática de documentación con **Swagger**, mejorando la experiencia para los desarrolladores.

---

### **📚 4.5 Documentación con Docstrings**

Todas las funciones principales están documentadas utilizando **docstrings**. Esto asegura:
- **Claridad**: Proporciona una guía detallada para entender el propósito y funcionamiento de cada función.
- **Mantenibilidad**: Facilita la colaboración en equipo y el desarrollo a largo plazo.

---

### **🐋 4.6 Despliegue con Docker**

La aplicación se ejecuta dentro de contenedores **Docker**, lo que aporta:
- **Portabilidad**: Permite ejecutar el sistema en cualquier entorno compatible con Docker.
- **Facilidad de despliegue**: Simplifica la configuración inicial y el mantenimiento continuo.

---

### **📦 4.7 Base de Datos MongoDB**

Se eligió **MongoDB** como base de datos debido a:
- **Eficiencia**: Ideal para manejar grandes volúmenes de datos de eventos.
- **Flexibilidad**: Permite trabajar con esquemas dinámicos que se adaptan a las necesidades del proyecto.

---

### **⚙️ 4.8 Generación de Assertions**

En los tests automatizados se incluyeron assertions relevantes que validan:
- **Clics**: Comprueban que la navegación sea correcta si se espera un cambio de URL.
- **Entradas (input)**: Verifican que los valores ingresados coincidan con los esperados.
- **Navegación**: Aseguran que la URL sea la correcta después de una acción de goto.

---

## 5. Trade-offs Considerados ✨

Estas son algunas de las decisiones clave y cómo las abordé, buscando siempre equilibrar funcionalidad actual y opciones futuras:

---

### **📂 5.1 Almacenamiento de Eventos**

**Base de datos MongoDB**  
- ✅ **Ventajas**:  
  - **Escalabilidad**: Perfecta para manejar grandes volúmenes de datos de eventos.  
  - **Flexibilidad**: El esquema dinámico permite adaptarse rápidamente a cambios en los requisitos.  
- ⚠️ **Desventajas**:  
  - Requiere **configuración inicial** adicional y monitoreo constante para mantener el rendimiento óptimo.

> 💡 **Consideración futura**: Evaluar el uso de bases de datos relacionales o híbridas para escenarios donde se requiera una mayor consistencia transaccional.

---

### **🛠️ 5.2 Generación Dinámica de Tests**

**Jinja2 (solución actual)**  
- ✅ **Ventajas**:  
  - **Simplicidad**: Fácil de implementar y personalizar para la generación de código.  
  - **Flexibilidad**: Permite un rápido ajuste en la estructura de los tests.  
- ⚠️ **Desventajas**:  
  - La validación de sintaxis depende de pruebas externas, lo que podría llevar a **errores en tiempo de ejecución**.

**Builders específicos (opción futura)**  
- ✅ **Ventajas**:  
  - **Robustez**: Generan código con estructuras más rígidas y menos propensas a errores.  
  - **Reutilización**: Más fácil de mantener en equipos grandes.  
- ⚠️ **Desventajas**:  
  - **Complejidad adicional**: Requiere mayor inversión inicial en desarrollo y diseño.

---

### **🔍 5.3 Complejidad de Assertions**

**Assertions actuales**  
- 🟢 **Alcance**: Se enfocan en validaciones comunes como:  
  - **Navegación**: Comprobar que las URL sean las esperadas tras acciones específicas.  
  - **Acciones de entrada**: Validar que los valores ingresados en campos sean correctos.  
  - **Clicks**: Verificar redirecciones tras un clic.  
- ⚠️ **Limitaciones**:  
  - Aún no se realizan comprobaciones avanzadas como validación visual o cambios detallados en el DOM.

**Assertions avanzadas (posible mejora)**  
- ✅ **Oportunidades**:  
  - **Verificaciones visuales**: Implementar capturas de pantalla automáticas para comparar cambios en interfaces.  
  - **Estado del DOM**: Validar que el DOM refleje cambios esperados tras eventos clave.  
- ⚠️ **Desafíos**:  
  - Incrementan el tiempo de ejecución de los tests y requieren herramientas específicas.

## 6. Áreas de Mejora Identificadas 🚀

### **🔧 6.1 Testing y Validación:**

- **Automatizar la ejecución de tests** para asegurar que todos los casos generados se validen correctamente y de manera más eficiente. Esto permitirá una validación continua sin intervención manual.

### **⚡ 6.2 Optimización de Assertions:**

- **Incorporar validaciones avanzadas** como comprobaciones del estado del DOM o la captura de pantallas, para incrementar la precisión y robustez de las pruebas, y así ofrecer un control más exhaustivo sobre la calidad de las aplicaciones.