# 📘 Phi-2 기반 텍스트 생성기 프로젝트

---

## 1. 프로젝트 개요

Microsoft의 **Phi-2** 모델을 활용하여 FastAPI 서버를 통해 사용자의 질문에 대해 자연어 답변을 생성하는 텍스트 생성기 애플리케이션을 개발하였다.  
본 프로젝트는 경량화된 사전학습 언어모델을 실제 어플리케이션에 적용하는 과정을 실습하고, 학습되지 않은 다양한 질의에 대해 일관성 있는 답변을 생성하는 능력을 평가하는 데 목적이 있다.

---

## 2. 사용 모델: Phi-2

- 모델명: **microsoft/phi-2**
- 파라미터 수: 약 **2.7B**
- 특성: 수십억 개의 고품질 텍스트 데이터로 학습됨
- 지원 언어: 주로 영어 최적화 (간단한 한국어 문장 대응 가능)
- 장점:
  - 비교적 적은 리소스에도 강력한 성능
  - 빠른 추론 속도
  - 글쓰기 보조, Q&A 태스크에 우수한 결과

---

## 3. 시스템 개요

### 서버 측
- **FastAPI**를 이용한 API 서버 구축
- **Torch + Transformers**를 이용하여 모델 로드 및 추론
- GPU 환경(CUDA) 최적화 (float16 사용)

### 클라이언트 측
- **HTML + JavaScript**로 간단한 질문/응답 웹 인터페이스
- 답변 생성 시간 실시간 표시 기능 포함

---

## 4. 구현 화면


![phicap1](https://github.com/kangtaee/sllmproject2025/blob/main/imgfile/phicap3.PNG)

- 한국어 질문 ("세종대왕이 누구야?")에 대해 엉뚱하고 관련 없는 영어 답변을 생성함

- 이는 Phi-2 모델이 기본적으로 영어 데이터 위주로 학습되어 있기 때문

- 한국어 자연어 처리에 있어서는 fine-tuning 없이 성능을 기대하기 어려움

---

![phicap2](https://github.com/kangtaee/sllmproject2025/blob/main/imgfile/phicap1.PNG)

- 영어 질문 ("What is the difference between AI and machine learning?")에 대해 정확하고 논리적인 답변을 생성함

- 응답 시간: 약 49.3초 소요

- 답변 품질: 사실 기반, 문장 구조도 자연스러움
---

## 5. 핵심 코드 요약

### 1. 모델 로드 (GPU 사용)

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    device_map="auto",
    torch_dtype=torch.float16
)
model.eval()
```
### 2. 질문 넣고 답변 생성
 ```
prompt = "Q: What is the difference between AI and machine learning?\nA:"
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

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```
### 3. FastAPI 서버 기본 뼈대
```
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/generate")
async def generate_text(req: TextRequest):
    return {"generated": "답변 내용"}
```

---

## 6. 세부 기술적 특징

| 항목 | 내용 |
|:---|:---|
| 서버 프레임워크 | FastAPI |
| 추론 프레임워크 | PyTorch + Transformers |
| 디바이스 설정 | GPU 자동 할당 (`device_map="auto"`) |
| 최적화 설정 | float16 연산 최적화 |
| 생성 파라미터 | max_length=200, temperature=0.8, top_p=0.9, repetition_penalty=1.2 |

---

## 7. 느낀 점 및 개선 방향

- **모델 선택 이유**: Phi-2는 2.7B 크기에도 불구하고 개인 GPU에서 빠르게 동작 가능하고, 기본적인 질의응답 품질이 우수했다.
- **발견된 문제점**:
  - 한국어 질문 처리에는 한계 존재
  - 짧거나 모호한 질문에는 비논리적 답변이 나오는 경우가 있음
  - 반복 문장 현상이 완전히 억제되지는 않음

- **개선 아이디어**:
  - prompt template를 정교화하여 질문 명확성 개선
  - 생성 후 중복 문장 post-processing 추가
  - 한글 데이터로 별도 fine-tuning 고려

