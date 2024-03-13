// document.addEventListener("DOMContentLoaded", function () {
//     const chatForm = document.getElementById("chat-form");
//     const chatMessages = document.getElementById("chat-messages");
//     const messageInput = document.getElementById("message-input");
//     const chatButton = document.getElementById("chatbtn");
  
//     chatForm.addEventListener("submit", function (e) {
//       e.preventDefault();
  
//       const messageText = messageInput.value.trim();
//       if (messageText) {
//         // User message
//         addMessageToChat("user", messageText);
  
//         // OpenAI 요청 전송 전 "질문 완료"를 확인
//         if (messageText === "질문 완료") {
//           // 사용자 정의 처리를 여기에 추가
//           addMessageToChat("ai", "여기에 원하는 답변을 처리하여 표시합니다.");
//           messageInput.value = ""; // 입력 필드 초기화
//         } else {
//           // OpenAI API로 메시지 전송
//           fetch('/chat/', {
//               method: 'POST',
//               headers: {
//                   'Content-Type': 'application/x-www-form-urlencoded',
//               },
//               body: `message=${encodeURIComponent(messageText)}`
//           })
//           .then(response => response.json())
//           .then(data => {
//               addMessageToChat("ai", data.message);
//           })
//           .catch(error => console.error('Error:', error));
  
//           // Clear input after sending
//           messageInput.value = "";
//         }
//       }
//     });
  
//     function addMessageToChat(sender, text) {
//       const messageDiv = document.createElement("div");
//       const messageTextDiv = document.createElement("div");
//       const iconDiv = document.createElement("div");
  
//       messageTextDiv.textContent = text;
//       messageTextDiv.className = "message-text px-3 py-2 rounded-lg max-w-xs";
  
//       if (sender === "user") {
//         messageDiv.className = "message user-message flex justify-end items-center my-1";
//         messageTextDiv.classList.add("bg-blue-500", "text-white", "order-2");
//         iconDiv.className = "icon w-8 h-8 order-1 ml-2";
//       } else {
//         messageDiv.className = "message ai-message flex justify-start items-center my-1";
//         messageTextDiv.classList.add("bg-blue-100", "text-blue-800", "order-2");
//         iconDiv.className = "icon w-8 h-8 order-1 mr-2";
//         iconDiv.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-robot" viewBox="0 0 16 16">' +
//         '<path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/>' +
//         '<path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"/>' +
//         "</svg>"; // AI 아이콘 SVG 코드
//       }
  
//       messageDiv.appendChild(iconDiv);
//       messageDiv.appendChild(messageTextDiv);
//       chatMessages.appendChild(messageDiv);
//       chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to the bottom of the chat
//     }
//   });
  

document.addEventListener("DOMContentLoaded", function() {
    // 'send' 버튼과 메시지 입력 필드의 DOM 요소를 가져옵니다.
    const sendButton = document.getElementById("chatbtn");
    const messageInput = document.getElementById("message-input");
    const chatMessages = document.getElementById("chat-messages");

    // 서버로부터 받은 데이터로 폼을 채우는 함수
    function fillFormWithData(data) {
        // ID가 'title', 'contents' 등인 입력 필드에 값을 설정합니다.
        // ID는 실제 HTML 요소의 ID와 일치해야 합니다.
        console.log(data.title)
        console.log(data.content)
        console.log(data.etc)
        console.log(data.title)
        document.getElementById('title').value = data.title;
        document.getElementById('contents').value = data.Content;
        // 날짜 형식에 맞게 조정해야 할 수도 있습니다.
        // document.getElementById('start-date').value = data.date || "";
        // document.getElementById('end-date').value = data.date || "";
        // document.getElementById('mission-contents').value = data.mission || "";
        document.getElementById('others-contents').value = data.etc;
    }


    sendButton.addEventListener("click", function(e) {
        e.preventDefault(); // 폼 제출 기본 동작 방지

        const messageText = messageInput.value.trim();
        if (messageText) {
            // 서버에 메시지를 전송하고 AI 응답을 받습니다.
            fetch('/post/get_ai_response/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText })
            })
            .then(response => response.json())
            .then(data => {
                // AI의 응답을 채팅창에 추가합니다.
                addMessageToChat("ai", data.answer);

                try {
                    // 응답이 JSON 형식인지 확인
                    const responseData = JSON.parse(data.answer);
                    
                    // JSON 형식의 데이터가 있고, 예상하는 프로퍼티들이 존재하는지 확인
                    if (responseData) {
                        // 데이터로 폼을 채우는 함수를 호출합니다.
                        fillFormWithData(responseData);
                    }
                } catch(e) {
                    // 응답이 JSON 형식이 아닌 경우 콘솔에 오류 출력
                    console.error("Received data is not valid JSON:", e);
                }
            })
            .catch(error => console.error('Error:', error));

            messageInput.value = ""; // 입력 필드 초기화
        }
    });

    // 메시지를 채팅창에 추가하는 함수입니다.
    function addMessageToChat(sender, text) {
        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}-message`;

        const profilePic = document.createElement("div");
        profilePic.className = "profile-pic";

        const textDiv = document.createElement("div");
        textDiv.className = "text ml-2 bg-blue-100 text-blue-800 p-2 rounded-lg";
        textDiv.innerText = text;

        messageDiv.appendChild(profilePic);
        messageDiv.appendChild(textDiv);
        chatMessages.appendChild(messageDiv);

        chatMessages.scrollTop = chatMessages.scrollHeight; // 채팅창을 최신 메시지 위치로 스크롤
    }
});
