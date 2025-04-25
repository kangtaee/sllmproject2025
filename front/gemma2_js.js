async function sendRequest() {
  const input = document.getElementById('input').value.trim();
  const responseBox = document.getElementById('responseBox');

  if (!input) {
    responseBox.innerText = "❗ 질문을 입력하세요.";
    return;
  }

  responseBox.innerText = "⏳ 생성 중입니다...";

  try {
    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: input })
    });

    const data = await res.json();
    responseBox.innerText = data.generated + "\n\n⚡ 응답 시간: " + data.response_time_sec + "초";
  } catch (err) {
    responseBox.innerText = "❌ 오류 발생: " + err.message;
  }
}
