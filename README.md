# 🎵 BolillonFelizbot

Bot de Telegram desarrollado en **Python** que recomienda música a los usuarios de acuerdo con sus mensajes.

El bot utiliza **expresiones regulares (Regex)** para identificar géneros musicales, estados de ánimo y comandos dentro de los mensajes del usuario. A partir de la categoría detectada, proporciona una playlist de **Spotify**.

---

## ✨ Características

- 🤖 Bot para Telegram.
- 🎵 Recomendación de música mediante playlists de Spotify.
- 🔎 Detección de mensajes mediante expresiones regulares.
- 😊 Recomendaciones según estado de ánimo.
- 🎸 Recomendaciones según género musical.
- 🔄 Comando para solicitar otra recomendación.
- 💬 Respuestas conversacionales básicas mediante NLTK.
- 🔐 Token de Telegram almacenado mediante variables de entorno.
- 👤 Mantiene la categoría musical actual de cada usuario para poder solicitar otra recomendación.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **python-telegram-bot**
- **NLTK**
- **Regex (`re`)**
- **Spotify**
- **python-dotenv**

---

## 📂 Estructura del proyecto

```text
BolillonFelizbot/
│
├── bot.py
├── .env
├── .gitignore
└── README.md
```

### `bot.py`

Contiene toda la lógica principal del bot:

- Configuración de Telegram.
- Patrones de expresiones regulares.
- Detección de categorías.
- Recomendación de playlists.
- Manejo de conversaciones.
- Comandos de Telegram.

### `.env`

Contiene información sensible, principalmente el token del bot.

Ejemplo:

```env
TELEGRAM_TOKEN=TU_TOKEN_AQUI
```

El archivo `.env` **no debe subirse a GitHub**.

---

## ⚙️ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/BolillonFelizbot.git
cd BolillonFelizbot
```

### 2. Crear un entorno virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install python-telegram-bot nltk python-dotenv nest-asyncio
```

---

## 🔐 Configuración del token

El bot utiliza el token proporcionado por **BotFather**.

Crear un archivo llamado:

```text
.env
```

y agregar:

```env
TELEGRAM_TOKEN=TU_TOKEN
```

En `bot.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
```

> ⚠️ Nunca publiques el token directamente dentro del código ni lo subas a GitHub.

También se recomienda agregar `.env` al archivo `.gitignore`.

---

## 🧠 Funcionamiento

El bot recibe el mensaje del usuario y analiza su contenido.

Por ejemplo:

```text
"hola, quiero escuchar rock"
```

El sistema analiza el mensaje utilizando expresiones regulares y puede detectar:

```text
rock
```

Después busca una playlist correspondiente a esa categoría y la envía al usuario.

El flujo general es:

```text
Usuario
   │
   ▼
Mensaje de Telegram
   │
   ▼
Expresiones regulares
   │
   ▼
Detección de categoría
   │
   ├── Género
   │
   ├── Estado de ánimo
   │
   └── Comando
   │
   ▼
Playlist correspondiente
   │
   ▼
Spotify
```

---

# 🔎 Expresiones regulares

Una de las partes principales del bot es el uso de **expresiones regulares** para reconocer diferentes formas en las que un usuario puede escribir una petición.

Por ejemplo:

```python
r"\b(triste|tristeza|para llorar)\b"
```

permite detectar expresiones como:

```text
estoy triste
quiero algo para llorar
ando con tristeza
```

También pueden utilizarse expresiones como:

```python
r"hol.*"
```

para reconocer mensajes que comiencen con `hol`, por ejemplo:

```text
hol
hola
holaaa
hol que tal
hol amigo
```

### Algunos símbolos utilizados

| Regex | Significado |
|---|---|
| `.` | Cualquier carácter |
| `*` | Cero o más repeticiones |
| `+` | Una o más repeticiones |
| `?` | Cero o una repetición |
| `^` | Inicio del texto |
| `$` | Final del texto |
| `\b` | Límite de palabra |
| `(...)` | Grupo |
| `\|` | OR |

Por ejemplo:

```python
r"^(hola|hol.*)$"
```

permite reconocer diferentes formas de saludo.

---

# 🎸 Categorías musicales

El bot puede organizar las recomendaciones mediante diferentes categorías.

### Géneros

- 🎸 Rock
- 🎤 Pop
- 🤘 Metal
- 🎧 Electrónica
- 🎤 Rap
- 🎙️ Hip Hop
- 🇰🇷 K-Pop
- 🎹 Instrumental
- 🎻 Música clásica
- 🎷 Jazz
- 🎵 Indie
- 🥁 Punk
- 🌌 Ambiental
- 💃 Salsa

### Estados de ánimo

- 😢 Triste
- 😄 Feliz
- 😡 Enojado
- 😌 Relajante
- 🌌 Escapar de la realidad

Las categorías pueden ampliarse agregando nuevos patrones y playlists.

---

# 🔄 Sistema de "Otra"

El bot permite que el usuario solicite otra recomendación sin tener que indicar nuevamente el género.

Por ejemplo:

```text
Usuario: quiero rock

Bot: 🎸 [Playlist de Rock]

Usuario: otra

Bot: 🎸 [Otra Playlist de Rock]
```

Para conseguir esto, el bot guarda temporalmente la categoría actual del usuario:

```python
context.user_data["categoria_actual"]
```

También puede guardar la última playlist enviada:

```python
context.user_data["ultima_playlist"]
```

Esto permite evitar que `"otra"` devuelva inmediatamente la misma playlist.

---

# 🎧 Playlists

Las playlists se almacenan mediante un diccionario de Python.

Un ejemplo simplificado:

```python
playlists = {
    "rock": [
        "https://open.spotify.com/playlist/...",
        "https://open.spotify.com/playlist/...",
    ],

    "pop": [
        "https://open.spotify.com/playlist/...",
        "https://open.spotify.com/playlist/...",
    ],

    "triste": [
        "https://open.spotify.com/playlist/...",
        "https://open.spotify.com/playlist/...",
    ]
}
```

Cuando el usuario solicita una categoría, el bot selecciona una playlist disponible.

---

# 💬 Ejemplos de interacción

### Saludo

```text
Usuario:
hola

Bot:
¡Hola! 🎵 ¿Qué quieres escuchar?
```

### Género

```text
Usuario:
quiero escuchar rock

Bot:
🎸 Aquí tienes una playlist de Rock:
https://open.spotify.com/playlist/...
```

### Estado de ánimo

```text
Usuario:
estoy triste

Bot:
😢 Tal vez esta playlist te acompañe:
https://open.spotify.com/playlist/...
```

### Otra recomendación

```text
Usuario:
otra

Bot:
🎸 Aquí tienes otra playlist:
https://open.spotify.com/playlist/...
```

### Petición más natural

```text
Usuario:
holaaa, hoy quiero algo tranquilo para trabajar

Bot:
😌 Aquí tienes una playlist relajante:
https://open.spotify.com/playlist/...
```

---

# 🧩 NLTK

Además de las expresiones regulares, el proyecto utiliza **NLTK** para generar algunas respuestas conversacionales.

Por ejemplo:

```python
from nltk.chat.util import Chat, reflections
```

Se pueden definir patrones de conversación:

```python
pares = [
    (
        r"hola|hol.*",
        ["¡Hola! 🎵 ¿Qué quieres escuchar?"]
    ),
    (
        r"gracias|muchas gracias",
        ["¡De nada! 🎶"]
    )
]
```

Esto permite que el bot tenga respuestas básicas antes de realizar una recomendación musical.

---

# ▶️ Ejecutar el bot

Una vez configurado el entorno y el archivo `.env`, ejecutar:

```bash
python bot.py
```

Si todo está configurado correctamente aparecerá un mensaje similar a:

```text
🎵 Bot en ejecución...
```

El programa debe permanecer ejecutándose para que Telegram pueda recibir los mensajes.

---

# 🔒 Seguridad

El token del bot es información sensible.

Se recomienda utilizar un `.gitignore` como:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Nunca se debe hacer:

```python
TOKEN = "123456789:ABC..."
```

dentro del código que será publicado.

Si un token llega a publicarse accidentalmente, debe **revocarse y generar uno nuevo mediante BotFather**.

---

# 🚀 Posibles mejoras

Algunas mejoras que pueden incorporarse posteriormente:

- 🎶 Integración con la API de Spotify.
- 🎧 Generación de playlists personalizadas.
- 🧠 Detección de múltiples categorías en un mismo mensaje.
- ❤️ Sistema para registrar canciones o playlists favoritas.
- 👎 Sistema de likes/dislikes.
- 📊 Historial de recomendaciones.
- 👤 Perfiles de usuario.
- 🎼 Recomendaciones basadas en preferencias anteriores.
- 🔍 Búsqueda de canciones directamente desde Telegram.
- 🎵 Recomendaciones combinando género y estado de ánimo.
- 🤖 Utilizar un modelo de lenguaje para mejorar la comprensión de mensajes.

---

# 📌 Objetivo del proyecto

El objetivo de **BolillonFelizbot** es desarrollar un bot conversacional capaz de interpretar solicitudes sencillas de los usuarios y recomendar música de acuerdo con sus preferencias.

El proyecto sirve como práctica de:

- Programación en Python.
- Expresiones regulares.
- Desarrollo de bots para Telegram.
- Manejo de estados de usuario.
- Programación asíncrona.
- Uso de APIs y servicios externos.
- Manejo seguro de variables de entorno.
- Diseño de sistemas conversacionales.

---

## 👨‍💻 Autor

**Fernando Ocampo Tovar**

Proyecto académico/personal desarrollado en Python.
