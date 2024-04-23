document.addEventListener('DOMContentLoaded', function () {

    // Retrieve the selected model from sessionStorage
    const selectedModel = sessionStorage.getItem('selectedModel');

    if (selectedModel) {
        // Play the corresponding voice based on the selected model
        switch (selectedModel) {
            case 'iu':
                playVoice('../static/voices/iu_talk.mp3');
                break;
            case 'cha':
                playVoice('../static/voices/cha_talk.mp3');
                break;
            case 'chunsik':
                playVoice('../static/voices/liam_talk.mp3');
                break;
            default:
                console.error('Invalid model selected.');
        }
    } else {
        console.error('No model selected.');
    };

    function playVoice(voicePath) {
        // Implement your code to play the voice
        const audio = new Audio(voicePath);
        audio.play();

        // 채팅 내용 입력
        var messageInput = document.getElementById('message-input');
        const sendButton = document.getElementById('send-button');
        // 채팅 화면창
        var chatMessages = document.getElementById('chat-messages');
        // 웹소켓 연결 생성
        var ws = new WebSocket(`ws://${document.domain}:${location.port}/chatting`);

        // fetch('/card-path', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     }
        // })
        // .then(response => {
        //     if (!response.ok) {
        //         throw new Error('Network response was not ok');
        //     }
        //     else {console.log("hi");}
        //     return response.json(); // JSON 형식으로 변환
        // })
        // .then(data => {
        //     const taroImgContainer = document.querySelector('.taro-img');
        //     taroImgContainer.innerHTML = '';
        //     console.log(data);
        //     const img = document.createElement('img');
        //     img.src = data.cardPath; // JSON에서 불러온 imgPath 값을 사용
        //     taroImgContainer.appendChild(img);
        // })
        // .catch(error => console.error('Error:', error));


        // 서버에서 메시지를 받을 때 처리
        ws.onmessage = function (event) {
            var data = JSON.parse(event.data);
            var messageText = data.message; // JSON 데이터에서 메시지 텍스트를 가져옴
            var sender = data.sender; // 메시지의 발신자
            var time = new Date().toLocaleTimeString();

            if (sender === "나") {
                receiveMessage(messageText, 'right-bubble', time, sender);
            } else {
                receiveMessage(messageText, 'left-bubble', time, sender);
            }
        };

        messageInput.addEventListener('keypress', function (event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });

        // 전송 버튼을 클릭했을 때 메시지 전송
        sendButton.addEventListener('click', function () {
            sendMessage();
        });

        function sendMessage() {
            var messageContent = messageInput.value;
            var currentTime = new Date().toLocaleTimeString(); // 현재 시간을 가져옵니다.
            if (messageContent.trim() !== '') {
                var message = {
                    message: messageContent,
                    time: currentTime, // 메시지 객체에 시간 추가
                    sender: '나', // 메시지 객체에 발신자 추가
                    celebrity: selectedModel
                };
                ws.send(JSON.stringify(message)); // 메시지를 서버로 JSON 형식으로 전송
                messageInput.value = '';
            }
            console.log(message);
        }

        // 받은 메시지를 채팅창에 추가하는 함수 수정
        function receiveMessage(message, className, time, sender) {
            let senderName;
            if (sender === "나") {
                senderName = sender
            } else if (sender === "iu") {
                senderName = "아이유";
            } else if (sender === "cha") {
                senderName = "차은우";
            } else {
                senderName = "춘식이";
            }
            console.log(`receiveMessage\nsender : ${senderName}\ntime : ${time}`);
            appendMessage(message, className, time, senderName);
            //// resizeChatContainer();
        }

        // CSS 적용 코드.
        function applyStyles(element, styles) {
            for (const property in styles) {
                element.style[property] = styles[property];
            }
        }

        function appendMessage(message, className, time, sender) {
            const messageContainer = document.createElement('div');
            const senderInfoContainer = document.createElement('div');
            const senderImageElement = document.createElement('img');
            const senderElement = document.createElement('div');
            const messageElement = document.createElement('div');
            const timeInfoContainer = document.createElement('div');
            const timeElement = document.createElement('div');

            let senderImagePath;
            console.log(sender);
            let senderImg;

            if (sender === "나") {
                senderImagePath = "../static/images/default.png";
                className = 'right-bubble';
            } else {
                if (sender === "아이유") {
                    senderImg = "iu";
                } else if (sender === "차은우") {
                    senderImg = "cha";
                } else {
                    senderImg = "chun";
                }
                senderImagePath = `../static/celeb-img/${senderImg}.png`;
                className = 'left-bubble';
            }
            senderImageElement.src = senderImagePath;
            console.log(`appendMessage\n${senderImagePath}`);


            // 이미지 크기 조정
            applyStyles(senderImageElement, {
                width: '30px',
                height: '30px',
                borderRadius: '20px',
                marginRight: '10px'
            });
            // 시간 표시 크기 스타일 적용
            applyStyles(timeElement, {
                fontSize: '50%', // 글씨 크기 반으로
                // 화면 크기에 따라 유연하게 조정되는 스타일 추가
            });

            senderElement.textContent = sender;
            messageElement.textContent = message;
            timeElement.textContent = time;

            // 발신자 정보 컨테이너 스타일 적용
            applyStyles(senderInfoContainer, {
                display: 'flex',
                alignItems: 'center',
                justifyContent: (className === 'right-bubble') ? 'flex-end' : 'flex-start',
                marginBottom: '10px'
            });

            // 메시지 컨테이너 스타일 적용
            applyStyles(messageContainer, {
                display: 'flex',
                flexDirection: 'column',
                alignItems: (className === 'right-bubble') ? 'flex-end' : 'flex-start',
                maxWidth: '80%'
            });
            // 시간 정보 컨테이너 스타일링
            applyStyles(timeInfoContainer, {
                display: 'flex',
                flexDirection: 'column',
                alignItems: (className === 'right-bubble') ? 'flex-end' : 'flex-start',
                // maxWidth: '80%'
            });

            // 메시지 요소 추가
            if (sender === "나") {
                applyStyles(senderElement, {
                    marginRight: '10px' // "나" 문구와 이미지 사이 간격 조정
                });
                senderInfoContainer.appendChild(senderElement);
                senderInfoContainer.appendChild(senderImageElement);
            } else {
                senderInfoContainer.appendChild(senderImageElement);
                senderInfoContainer.appendChild(senderElement);
            }
            messageContainer.appendChild(messageElement);
            timeInfoContainer.appendChild(timeElement);

            // 클래스 추가 및 채팅창에 메시지 컨테이너 추가
            messageContainer.classList.add(className);
            chatMessages.appendChild(senderInfoContainer);
            chatMessages.appendChild(messageContainer);
            chatMessages.appendChild(timeInfoContainer);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // 말풍선 너비 조절 함수 CSS
        function adjustBubbleWidth(messageElement) {
            const maxWidth = 600;
            const minWidth = 50;
            messageElement.style.display = 'inline-block';
            messageElement.style.whiteSpace = 'normal';
            messageElement.style.maxWidth = maxWidth + 'px';

            const messageWidth = messageElement.offsetWidth;
            if (messageWidth < minWidth) {
                messageElement.style.width = minWidth + 'px';
            } else {
                messageElement.style.width = 'auto';
            }
        }

    };
});