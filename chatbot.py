import os
import random
import asyncio
import nest_asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from nltk.chat.util import Chat, reflections


# ============================================================
# CONFIGURACIÓN
# ============================================================

nest_asyncio.apply()

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    raise ValueError(
        "No se encontró la variable de entorno TELEGRAM_TOKEN"
    )


# ============================================================
# PLAYLISTS
# ============================================================
#
# Puedes agregar varias playlists a cada categoría.
# Cuando el usuario pida "otra", se elegirá una diferente
# de manera aleatoria.
#
# IMPORTANTE:
# Reemplaza estos enlaces por tus playlists reales de Spotify.
#

playlists = {

    # -------------------------
    # GÉNEROS
    # -------------------------

    "rock": [
        "https://open.spotify.com/intl-es/track/0grFc6klR3hxoHLcgCYsF4?si=d80a8cc434054f31",
        "https://open.spotify.com/intl-es/track/5VVWgWH8HFLAtM8lbttvn9?si=8dccee5b068c48e6"
    ],

    "pop": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_POP_1",
        "https://open.spotify.com/playlist/TU_PLAYLIST_POP_2"
    ],

    "clasico": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_CLASICO_1"
    ],

    "house": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_HOUSE_1"
    ],

    "metal": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_METAL_1"
    ],

    "rap": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_RAP_1"
    ],

    "hip hop": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_HIPHOP_1"
    ],

    "k-pop": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_KPOP_1"
    ],

    "instrumental": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_INSTRUMENTAL_1"
    ],

    "electronica": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_ELECTRONICA_1"
    ],

    "punk": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_PUNK_1"
    ],

    "ambiental": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_AMBIENTAL_1"
    ],

    "salsa": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_SALSA_1"
    ],

    "indie": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_INDIE_1"
    ],

    "psicodelico": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_PSICODELICO_1"
    ],


    # -------------------------
    # EMOCIONES
    # -------------------------

    "feliz": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_FELIZ_1",
        "https://open.spotify.com/playlist/TU_PLAYLIST_FELIZ_2"
    ],

    "triste": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_TRISTE_1",
        "https://open.spotify.com/playlist/TU_PLAYLIST_TRISTE_2"
    ],

    "enojado": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_ENOJADO_1"
    ],

    "relajado": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_RELAX_1"
    ],

    "dimension": [
        "https://open.spotify.com/playlist/TU_PLAYLIST_DIMENSION_1"
    ]
}


# ============================================================
# FUNCIONES DE RECOMENDACIÓN
# ============================================================

def recomendar_playlist(categoria, ultima_playlist=None):

    opciones = playlists.get(categoria, [])

    if not opciones:
        return None

    if len(opciones) == 1:
        return opciones[0]
    opciones_disponibles = [
        playlist
        for playlist in opciones
        if playlist != ultima_playlist
    ]

    if not opciones_disponibles:
        opciones_disponibles = opciones

    return random.choice(opciones_disponibles)


def obtener_nombre_categoria(categoria):

    nombres = {
        "rock": "Rock",
        "pop": "Pop",
        "clasico": "Clásico",
        "house": "House",
        "metal": "Metal",
        "rap": "Rap",
        "hip hop": "Hip Hop",
        "k-pop": "K-Pop",
        "instrumental": "Instrumental",
        "electronica": "Electrónica",
        "punk": "Punk",
        "ambiental": "Ambiental",
        "salsa": "Salsa",
        "indie": "Indie",
        "psicodelico": "Psicodélico",

        "feliz": "Feliz",
        "triste": "Triste",
        "enojado": "Enojado",
        "relajado": "Relajado",
        "dimension": "Para escapar de la realidad"
    }

    return nombres.get(categoria, categoria)


# ============================================================
# PATRONES NLTK
# ============================================================
#
# Aquí YA NO ponemos las playlists.
#
# Los patrones solamente identifican qué quiere el usuario.
#

pares = [

    # -------------------------
    # SALUDOS
    # -------------------------

    (
        r"hola|hol.*|buen.*|miau|buenas|buenas tardes|buenos días|buenos dias",
        [
            "¡Hola! ¿Cómo te llamas? Escribe mi nombre es + tu nombre jaja.",
        ]
    ),

    (
        r"mi nombre es (.*)",
        [
            "¡Hola %1! ¿Qué te gustaría escuchar?",
            "Bienvenido %1, soy tu bot musical. ¿Qué quieres escuchar?",
            "¡Hola %1! Te puedo recomendar música según tu estado de ánimo."
        ]
    ),


    # -------------------------
    # LISTAS
    # -------------------------

    (
        r"generos|géneros",
        [
            "Puedes elegir entre: Rock, Pop, Clásico, House, Metal, "
            "Rap, Hip Hop, K-Pop, Instrumental, Electrónica, Punk, "
            "Ambiental, Salsa, Indie y Psicodélico."
        ]
    ),

    (
        r"emociones|estados de animo|estados de ánimo",
        [
            "Tengo música para: Feliz, Triste, Enojado, Relajado "
            "y para escapar de la realidad."
        ]
    ),


    # -------------------------
    # RESPUESTAS GENERALES
    # -------------------------

    (
        r"no se|no sé|recomiendame|si|a.*|recomiéndame|ok|vale",
        [
            "Puedes escribir un género o una emoción para recomendarte "
            "una playlist.",
            "Dime cómo te sientes o qué género quieres escuchar 🎵"
        ]
    ),

    (
        r"gracias",
        [
            "¡No hay de qué! Si quieres otra recomendación hazmelo saber 😎"
        ]
    ),

    (
        r"no me gusto|no me gustó",
        [
            "Lamento leer eso 😭. Pídeme otra playlist y probamos con algo diferente."
        ]
    ),

    (
        r"me gusto|me gustó",
        [
            "¡Me da gusto leer eso! 😎 Puedes agregar la playlist a tu Spotify."
        ]
    ),


    # -------------------------
    # DESPEDIDA
    # -------------------------

    (
        r"adios|adiós|bye",
        [
            "¡Adiós! Que tengas un buen día 🎵",
            "Nos vemos pronto 😎"
        ]
    ),


    # ========================================================
    # EMOCIONES
    # ========================================================

    (
        r"ando triste|estoy triste|triste",
        [
            "__TRISTE__"
        ]
    ),

    (
        r"menos triste",
        [
            "__TRISTE__"
        ]
    ),

    (
        r"para llorar",
        [
            "__TRISTE__"
        ]
    ),

    (
        r"ando feliz|estoy feliz|feliz",
        [
            "__FELIZ__"
        ]
    ),

    (
        r"más feliz|mas feliz",
        [
            "__FELIZ__"
        ]
    ),

    (
        r"enojado|ando enojado|estoy enojado",
        [
            "__ENOJADO__"
        ]
    ),

    (
        r"algo tranqui|relajante|relajado|quiero relajarme",
        [
            "__RELAJADO__"
        ]
    ),

    (
        r"para ir a otra dimensión|para ir a otra dimension|"
        r"escapar de la realidad",
        [
            "__DIMENSION__"
        ]
    ),


    # ========================================================
    # GÉNEROS
    # ========================================================

    (
        r"rock|algo de rock",
        [
            "__ROCK__"
        ]
    ),

    (
        r"pop|algo de pop",
        [
            "__POP__"
        ]
    ),

    (
        r"clasico|clásico",
        [
            "__CLASICO__"
        ]
    ),

    (
        r"punk",
        [
            "__PUNK__"
        ]
    ),

    (
        r"psicodelico|psicodélico|pa darse un viaje",
        [
            "__PSICODELICO__"
        ]
    ),

    (
        r"instrumental",
        [
            "__INSTRUMENTAL__"
        ]
    ),

    (
        r"urbana|urbano",
        [
            "__URBANA__"
        ]
    ),

    (
        r"house",
        [
            "__HOUSE__"
        ]
    ),

    (
        r"electronica|electrónica",
        [
            "__ELECTRONICA__"
        ]
    ),

    (
        r"indie",
        [
            "__INDIE__"
        ]
    ),

    (
        r"rap",
        [
            "__RAP__"
        ]
    ),

    (
        r"hip hop|hip-hop",
        [
            "__HIP_HOP__"
        ]
    ),

    (
        r"metal",
        [
            "__METAL__"
        ]
    ),

    (
        r"salsa",
        [
            "__SALSA__"
        ]
    ),

    (
        r"k-pop|kpop",
        [
            "__KPOP__"
        ]
    ),

    (
        r"ambiental|ambiente",
        [
            "__AMBIENTAL__"
        ]
    )
]


chatbot = Chat(pares, reflections)


# ============================================================
# FUNCIÓN PARA ENVIAR PLAYLIST
# ============================================================

async def enviar_playlist(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    categoria: str
):

    ultima_playlist = context.user_data.get("ultima_playlist")

    playlist = recomendar_playlist(
        categoria,
        ultima_playlist
    )

    if not playlist:
        await update.message.reply_text(
            "No tengo una playlist para esa categoría todavía 😭"
        )
        return

    # Guardamos la categoría actual
    context.user_data["categoria_actual"] = categoria

    # Guardamos la playlist enviada
    context.user_data["ultima_playlist"] = playlist

    nombre = obtener_nombre_categoria(categoria)

    await update.message.reply_text(
        f"🎵 Creo que esto te puede gustar.\n\n"
        f"🎧 Playlist: {nombre}\n"
        f"{playlist}\n\n"
        f"Si quieres otra, escribe: otra"
    )


# ============================================================
# /start
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    # Reiniciar preferencias de la conversación
    context.user_data.clear()

    await update.message.reply_text(
        "🎵 ¡Holaa! Soy BolillonFelizbot.\n\n"
        "Soy un bot musical que te recomienda playlists "
        "según tu estado de ánimo o género favorito.\n\n"
        "Puedes escribir:\n"
        "• generos\n"
        "• emociones\n"
        "• rock\n"
        "• pop\n"
        "• estoy triste\n"
        "• estoy feliz\n\n"
        "Y si quieres otra recomendación escribe: otra"
    )


# ============================================================
# RESPUESTAS
# ============================================================

async def reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
) -> None:

    mensaje = update.message.text.lower().strip()

    # ========================================================
    # "OTRA"
    # ========================================================
    #
    # Ya no es un patrón general de NLTK.
    #
    # Utilizamos la categoría que el usuario había seleccionado.
    #

    if mensaje in ["otra", "otra playlist", "otra recomendación",
                    "otra recomendacion"]:

        categoria = context.user_data.get("categoria_actual")

        if not categoria:

            await update.message.reply_text(
                "Primero dime qué quieres escuchar 😎\n\n"
                "Por ejemplo: rock, pop, triste, feliz..."
            )

            return

        await enviar_playlist(
            update,
            context,
            categoria
        )

        return


    # ========================================================
    # NLTK
    # ========================================================

    respuesta = chatbot.respond(mensaje)

    if not respuesta:

        await update.message.reply_text(
            "No entendí eso jaja 😭\n\n"
            "Escribe un género o una emoción para "
            "ver las opciones disponibles."
        )

        return


    # ========================================================
    # DETECTAR CATEGORÍA
    # ========================================================

    categorias = {

        "__ROCK__": "rock",
        "__POP__": "pop",
        "__CLASICO__": "clasico",
        "__HOUSE__": "house",
        "__METAL__": "metal",
        "__RAP__": "rap",
        "__HIP_HOP__": "hip hop",
        "__KPOP__": "k-pop",
        "__INSTRUMENTAL__": "instrumental",
        "__ELECTRONICA__": "electronica",
        "__PUNK__": "punk",
        "__AMBIENTAL__": "ambiental",
        "__SALSA__": "salsa",
        "__INDIE__": "indie",
        "__PSICODELICO__": "psicodelico",

        "__FELIZ__": "feliz",
        "__TRISTE__": "triste",
        "__ENOJADO__": "enojado",
        "__RELAJADO__": "relajado",
        "__DIMENSION__": "dimension"
    }


    if respuesta in categorias:

        categoria = categorias[respuesta]

        await enviar_playlist(
            update,
            context,
            categoria
        )

        return


    # ========================================================
    # RESPUESTA NORMAL
    # ========================================================

    await update.message.reply_text(respuesta)


# ============================================================
# MAIN
# ============================================================

async def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            reply
        )
    )

    print("🎵 Bot en ejecución...")

    await app.run_polling()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())