despues de instalar Playwright poner playwright install  en la terminal

╔════════════════════════════════════════════════════════════╗
║ Looks like Playwright was just installed or updated.       ║
║ Please run the following command to download new browsers: ║
║                                                            ║
║     playwright install                                     ║
║                                                            ║
║ <3 Playwright Team                                         ║
╚════════════════════════════════════════════════════════════╝



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
- [3. Linter y Extensiones](#3-linter-y-extensiones)
  - [3.1 Recommended IDE Setup](#31-recommended-ide-setup)
  - [3.2 Formateo de código y Linter](#32-formateo-de-código-y-linter)
  - [3.3 Test unitarios](#33-test-unitarios)
  - [3.4 Check tipado](#34-check-tipado)
- [4. Descripción de servicios basicos](#4-descripción-de-servicios-basicos)

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


## 3. Linter y Extensiones

Nuestro proyecto cuenta con un **linter** que nos ayuda a mantener un código **limpio y ordenado**. Para poder utilizarlo es necesario instalar las siguientes **extensiones** en tu IDE:

- [VSCode](https://code.visualstudio.com/).
- [Python IntelliSense](vscode:extension/ms-python.python).
- [Black Formatter](vscode:extension/ms-python.black-formatter).
- [Ruff](vscode:extension/charliermarsh.ruff).
- [Pylance](vscode:extension/ms-python.vscode-pylance).
- [Mypy Checker](vscode:extension/ms-python.mypy-type-checker).


### 3.1 Recommended IDE Setup

Las siguientes extensiones son **recomendadas** para un mejor uso del IDE:

- [Debugpy](vscode:extension/ms-python.debugpy).
- [Docker](vscode:extension/ms-azuretools.vscode-docker).
- [Error Lens](vscode:extension/usernamehw.errorlens).
- [Better Comments](vscode:extension/aaron-bond.better-comments).
- [VsCode Action Buttons](vscode:extension/seunlanlege.action-buttons).

### 3.2 Formateo de código y Linter


Para correr el formateo de código utilizamos:

```sh
make format
```
Junto al check linter:
```sh
make linter
```

### 3.3 Test unitarios

Para correr los test unitarios utilizamos:
- [Pytest](https://docs.pytest.org/).

Este nos permite **correr** los **test unitarios** de forma rápida y sencilla.

```sh
make tests
```

### 3.4 Check tipado

Para correr el checkeo de tipado utilizamos:
- [MyPy](https://www.mypy-lang.org/).

```sh
make type-check
```


## 4. Descripción de servicios basicos

Toda la parte de **documentación** de la **API** se encuentra en [**`docs`**](http://localhost:3305/docs)

Los servicios más utilizados son:

| Resumen de servicio               | Método | URL                |
| --------------------------------- | ------ | ------------------ |
| Status de la aplicación           |   GET  | /health            |
| Consultas CRUD de tasks           |   GET  | /task              |
