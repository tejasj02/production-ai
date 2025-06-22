import os
import time
import base64
import io
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from google import genai
from PIL import Image

load_dotenv()
app = FastAPI()

@app.post("/process")
async def process(prompt: str = Form(...), image: UploadFile = Form(...)):
    start = time.time()
    image_bytes = await image.read()

    try:
        img = Image.open(io.BytesIO(image_bytes))
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    
    # Prompting Gemini to grade the chatbot's answer
        response = client.models.generate_content(model='gemini-2.0-flash', contents=[img, prompt])
        output = response.text
        status = "success"
    except Exception as e:
        output = str(e)
        status = "error"

    latency = round((time.time() - start) * 1000, 2)
    log_entry = {
        "prompt": prompt,
        "status": status,
        "latency_ms": latency
    }

    with open("performance_log.txt", "a") as f:
        f.write(str(log_entry) + "\n")

    return JSONResponse({
        "output": output,
        "latency_ms": latency
    })

@app.post("/analyze-image")
async def analyze_image(image: UploadFile = Form(...)):
    image_bytes = await image.read()
    img = Image.open(io.BytesIO(image_bytes))
    return {
        "format": img.format,
        "mode": img.mode,
        "size": img.size
    }

@app.post("/analyze-text")
async def analyze_text(prompt: str = Form(...)):
    try:
        client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
    # Prompting Gemini to grade the chatbot's answer
        response = client.models.generate_content(model='gemini-2.0-flash', contents=[prompt])
        return {"output": response.text}
    except Exception as e:
        return {"error": str(e)}