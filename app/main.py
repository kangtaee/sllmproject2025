from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import os


os.environ['HF_TOKEN'] = ""  # 필요 시만

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.getenv("HF_TOKEN"))
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,  # 성능 최적화
    token=os.getenv("HF_TOKEN")
)
model.eval()

class TextRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(req: TextRequest):
    try:
        start = time.time()
        prompt = f"Q: {req.text}\nA:"
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            **inputs,
            max_length=200,
            temperature=0.8,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
            eos_token_id=tokenizer.eos_token_id
        )
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Q: ~ A: ~ 포맷이 포함된 전체 답변에서 A: 뒤만 추출
        result = response_text.split("A:")[-1].strip()

        elapsed = round(time.time() - start, 2)
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"generated": result, "response_time_sec": elapsed}
    except Exception as e:
        return {"generated": f"❌ 오류: {str(e)}", "response_time_sec": 0}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
