
from fastapi import FastAPI, Body, Depends, File, UploadFile
from fastapi.responses import FileResponse
import os
from decouple import config
import requests
import shutil
from app.model import UserSchema, UserLoginSchema, TextToSpeechSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from openai import OpenAI

users = []

app = FastAPI()


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False


# route handlers
@app.post("/STT",dependencies=[Depends(JWTBearer())], tags=["Speech2Text"])
async def speech_to_text(file: UploadFile = File(...)):
    temp_audio_dir = "./temp/audio_input"
    OPENAI_API_KEY = config("openaikey")
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        file_location = os.path.join(temp_audio_dir, file.filename)
        with open(file_location, "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file)
        
        with open(file_location, "rb") as content:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=content  
            )

        os.remove(file_location)
        return {"transcript": transcript.text}
    except Exception as e:
        return {"error": str(e)}
    
    
@app.post("/TTS", dependencies=[Depends(JWTBearer())], tags=["Text2Speech"])
async def text_to_speech(TTS: TextToSpeechSchema):
    temp_audio_dir = "./temp/audio_output/"
    OPENAI_API_KEY = config("openaikey")
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"}
        payload = {
            "model": TTS.model,
            "messages": [{
                "role": TTS.role,
                "content": TTS.content
            }]
        }
        response_data = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()
        response = client.audio.speech.create(
            model="tts-1",
            voice=TTS.voice,
            input=response_data['choices'][0]['message']['content'],
        )
        response.stream_to_file(temp_audio_dir + "output.mp3")
        return FileResponse(temp_audio_dir + "output.mp3", media_type="audio/mpeg"), {"text": response_data['choices'][0]['message']['content']}
    except Exception as e:
        return {"error": str(e)}
        
@app.post("/user/signup", tags=["user"])
def create_user(user: UserSchema = Body(...)):
    users.append(user) # replace with db call, making sure to hash the password first
    return signJWT(user.email)


@app.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
