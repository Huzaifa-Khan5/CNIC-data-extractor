from google import genai
import os
import PIL.Image
import json
from dotenv import load_dotenv
from fastapi import FastAPI,File, UploadFile
import uvicorn
from typing import Dict,Any
from fastapi.responses import JSONResponse
import io

app = FastAPI()


load_dotenv()
 
def process_img(img):
    # GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = genai.Client()


    prompt = """This image contains ID card information. 
    Extract name, father name, date of birth, date of issue and date of expiry from this.
    Give me the result in json formet"""

# model = genai.GenerativeModel('gemini-2.0-flash')
    response = client.models.generate_content(
    model="gemma-3-12b-it",
    contents=[prompt, img])

    json_response=response.text[8:-3]
    json_data = json.loads(json_response)
    return json_data


@app.post("/extract_data/")
async def main(file: UploadFile= File(...))-> Dict[str, Any]:

    img = await file.read()
    img = PIL.Image.open(io.BytesIO(img))
    
    data=process_img(img)

    return {"data":data}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


