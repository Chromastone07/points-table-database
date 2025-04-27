document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const recipeId = this.dataset.recipeId;
            const isFavorited = this.classList.contains('favorited');

            if (isFavorited) {
                this.classList.remove('favorited');
                this.textContent = 'Favorite';
                console.log(`Recipe ${recipeId} unfavorited.`);
                // In a real application, you might update local storage or a server here
            } else {
                this.classList.add('favorited');
                this.textContent = 'Favorited!';
                console.log(`Recipe ${recipeId} favorited.`);
                // In a real application, you might update local storage or a server here
            }
        });
    });
});