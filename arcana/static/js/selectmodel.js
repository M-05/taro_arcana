document.addEventListener("DOMContentLoaded", function () {
    // Define the mapping of items to their respective audio files
    const itemAudioMap = {
        'iu': '../static/voices/iu_hi.mp3',
        'cha': '../static/voices/cha_hi.mp3',
        'chunsik': '../static/voices/liam_ogu.mp3'
    };

    // Preload all audio files and store them in an object
    const audioElements = {};
    for (const itemName in itemAudioMap) {
        const audio = new Audio(itemAudioMap[itemName]);
        audioElements[itemName] = audio;
    }

    // Function to play hover sound for a specific item
    function playHoverSound(itemName) {
        const audio = audioElements[itemName];
        audio.currentTime = 0; // Rewind audio to start (in case it's already playing)
        audio.play(); // Play the audio associated with the item
    }

    // Find all elements with class "item"
    const items = document.querySelectorAll('.item');

    // Loop through each "item" element
    items.forEach(function (item) {
        const itemName = item.dataset.item; // Get the item name from data-item attribute

        // Add click event listener to each "item" (existing functionality)
        item.addEventListener('click', function () {
            const model = item.dataset.model;

            fetch(`/firstGame?model=${model}`)
            .then(response => {
                // 응답 유형 확인
                const contentType = response.headers.get('Content-Type');
                if (contentType && contentType.includes('application/json')) {
                  // JSON 응답 처리
                return response.json();
                } else {
                  // 텍스트 응답 처리
                return response.text();
                }
            })
            .then(data => {
                console.log(data);
                sessionStorage.setItem('selectedModel', model);
                window.location.href = `/firstGame?model=${model}`;
            })
            .catch(error => {
                console.error('Error:', error);
            });
            // // AJAX 요청으로 서버에 데이터 전송
            // fetch('/celebName', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json'
            //     },
            //     body: JSON.stringify({ 
            //         celebText: model 
            //     })
            // })
            // .then(response => response.json())
            // .then(data => console.log(data))
            // .catch(error => console.error('Error:', error));

            // sessionStorage.setItem('selectedModel', model);
            
            // // 0.3초 후에 /firstGame?model=${model} 페이지로 이동합니다.
            // setTimeout(() => {
            //     window.location.href =`/firstGame?model=${model}`;
            // }, 300);
        });

        // Add mouseenter event listener to play hover sound for the specific item
        item.addEventListener('mouseenter', function () {
            console.log(`hover된 연예인은 : ${itemName}`);
            playHoverSound(itemName);
        });
    });
});
