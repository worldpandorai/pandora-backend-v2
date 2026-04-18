from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

# 🔐 Cargar variables de entorno
load_dotenv()

# 🔐 API KEY SEGURA
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# 🌐 CORS (permite conexión con tu app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Mensaje(BaseModel):
    texto: str

# 💬 RESPUESTA NORMAL
def responder(texto):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres Pandora, una asistente inteligente, natural y directa."},
            {"role": "user", "content": texto}
        ],
        max_tokens=80
    )

    return response.choices[0].message.content

# 🎨 GENERAR IMAGEN
def generar_imagen(prompt):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    imagen_base64 = result.data[0].b64_json
    data_url = f"data:image/png;base64,{imagen_base64}"

    return data_url

# 🚀 ENDPOINT PRINCIPAL
@app.post("/chat")
def chat(msg: Mensaje):
    texto = msg.texto.lower()

    # 🎨 detectar imagen
    if any(p in texto for p in ["imagen", "dibuja", "crea", "genera"]):
        img = generar_imagen(texto)
        return {"tipo": "imagen", "respuesta": img}

    # 💬 respuesta normal
    respuesta = responder(texto)
    return {"tipo": "texto", "respuesta": respuesta}