// Define the playVoice function to play audio
function playVoice(voicePath) {
    const audio = new Audio(voicePath);
    audio.play();
}

// Define the flipCard function to handle card flipping and data storage
function flipCard(cardElement, imagePath) {
    cardElement.innerHTML = ''; // Clear the card
    const cardFront = document.createElement('img');
    cardFront.src = imagePath; // Display the front of the card
    cardElement.appendChild(cardFront);

    // Store the selected card's image path in sessionStorage
    sessionStorage.setItem('selectedCardPath', imagePath);

    // // Send card information to the server (e.g., via fetch)
    // fetch('/cardPath', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({
    //         cardPath: imagePath // Send card path or other identification
    //     })
    // });
}

// Define the shuffleArray function to shuffle an array using Fisher-Yates algorithm
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// Define the displayCards function to create and display shuffled cards
function displayCards() {
    const basePath = '../static/taro-img/';
    const cards = [
        'death.png', 'devil.png', 'emperor.png', 'empress.png',
        'fool.png', 'hang.png', 'hermit.png', 'judgement.png', 'magician.png',
        'priestess.png', 'star.png', 'strength.png', 'sun.png',
        'temperance.png', 'tower.png', 'world.png'
    ];

    // Mapping relative paths to absolute paths
    const finalCards = cards.map(card => basePath + card);
    console.log('Game Script:', finalCards); // Output for verification or further use

    const gameContainer = document.getElementById('game-container');

    // Shuffle the cards array
    shuffleArray(finalCards);

    // Create and display the cards after shuffling
    finalCards.forEach((cardPath, index) => {
        var newCard = document.createElement('div');
        newCard.classList.add('card');

        var cardBack = document.createElement('img');
        cardBack.src = basePath + 'back.png'; // Path to card back image
        newCard.appendChild(cardBack);

        gameContainer.appendChild(newCard);

        // Set up click event listener for each card
        newCard.addEventListener('click', () => {
            // Hide all cards
            document.querySelectorAll('.card').forEach(card => {
                card.style.display = 'none';
            });

            // Display the selected card in a larger size
            newCard.style.display = 'block';
            newCard.style.position = 'absolute';
            newCard.style.top = '50%';
            newCard.style.left = '50%';
            newCard.style.width = '84px';
            newCard.style.transform = 'translate(-50%, -50%) scale(3.0)';
            newCard.style.zIndex = '1000';

            // Flip the selected card and store data
            flipCard(newCard, cardPath);

            // Redirect to /chat page after a delay
            setTimeout(() => {
                window.location.href = '/chat';
            }, 2000);
        });
    });
};

// Execute the code after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Retrieve the model from the query parameter
    const urlParams = new URLSearchParams(window.location.search);
    //
    const selectedModel = sessionStorage.getItem('selectedModel');
    // const selectedModel = urlParams.get('model');

    if (selectedModel) {
        // Store the selected model in sessionStorage ///
        sessionStorage.setItem('selectedModel', selectedModel);

        // Play the corresponding voice based on the selected model
        switch (selectedModel) {
            case 'iu':
                playVoice('../static/voices/iu_card.mp3');
                break;
            case 'cha':
                playVoice('../static/voices/cha_card.mp3');
                break;
            case 'chunsik':
                playVoice('../static/voices/liam_guruguru.mp3');
                break;
            default:
                console.error('Invalid model selected.');
        }

        // Display the cards after voice playback
        displayCards();
    } else {
        console.error('No model selected.');
    }
});