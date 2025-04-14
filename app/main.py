from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi.middleware.cors import CORSMiddleware
import torch
import uvicorn
import os

# HuggingFace token 환경변수 설정 (필요시만)
os.environ['HF_TOKEN'] = ""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = AutoTokenizer.from_pretrained('google/gemma-2-2b-it', token=os.getenv("HF_TOKEN"))
model = AutoModelForCausalLM.from_pretrained('google/gemma-2-2b-it', token=os.getenv("HF_TOKEN"))

class TextRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(req: TextRequest):
    try:
        input_ids = tokenizer(req.text, return_tensors="pt")
        with torch.no_grad():
            output_ids = model.generate(**input_ids, max_length=512)
        result = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return {"generated": result}
    except Exception as e:
        return {"generated": f"오류 발생: {str(e)}"}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
