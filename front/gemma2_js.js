function sendRequest() {
  const input = document.getElementById("input").value.trim();
  const responseBox = document.getElementById("responseBox");

  if (!input) {
    responseBox.innerText = "❗ 질문을 입력하세요.";
    return;
  }

  responseBox.innerText = "⏳ 생성 중입니다...";

  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/generate",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    },
    data: JSON.stringify({ text: input }),
    success: function (response) {
      responseBox.innerText = response.generated;
    },
    error: function (xhr, status, error) {
      responseBox.innerText = "❌ 오류 발생: " + error;
      console.error("에러 상태:", status);
      console.error("에러 내용:", xhr.responseText);
    }
  });
}
