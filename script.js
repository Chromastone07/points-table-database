document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.favorite-btn');
    const favoriteRecipesContainer = document.getElementById('favorite-recipes');
    const favoritesLink = document.querySelector('a[href="favorites.html"]'); //Get the link.

    let favorites = JSON.parse(localStorage.getItem('favorites')) || [];  //Use localStorage

    function displayFavorites() {
        if (!favoriteRecipesContainer) return; //Check if the element exists.
        favoriteRecipesContainer.innerHTML = ''; // Clear the container

        if (favorites.length === 0) {
            favoriteRecipesContainer.innerHTML = '<p>No favorites added yet.</p>';
            return;
        }

        favorites.forEach(recipe => {
            const recipeCard = document.createElement('div');
            recipeCard.classList.add('recipe-card');
            recipeCard.innerHTML = `
                <h3>${recipe.title}</h3>
                <p>${recipe.description}</p>
                <a href="${recipe.link}">View Recipe</a>
            `;
            favoriteRecipesContainer.appendChild(recipeCard);
        });
    }
    function addToFavorites(recipeId, title, description, link) {
         const isFavorited = favorites.some(fav => fav.id === recipeId);

        if (!isFavorited) {
            favorites.push({ id: recipeId, title, description, link });
            localStorage.setItem('favorites', JSON.stringify(favorites)); //Store
            console.log(`Recipe ${recipeId} added to favorites.`);
        } else {
             console.log(`Recipe ${recipeId} is already in favorites.`);
        }

    }

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const recipeId = this.dataset.recipeId;
            const recipeCard = this.closest('.recipe-card'); //Find the card.
            const title = recipeCard.querySelector('h3').textContent;
            const description = recipeCard.querySelector('p').textContent;
            const link = recipeCard.querySelector('a').getAttribute('href');

            addToFavorites(recipeId, title, description, link);
             //Update the button
            this.classList.add('favorited');
            this.textContent = 'Favorited!';
        });
    });
    if(favoritesLink){ // If on a page with the favorites link.
         favoritesLink.addEventListener('click', function(event){
            if (favorites.length === 0) {
                event.preventDefault(); //Prevent navigation.
                alert("No favorites added yet!");
            }
         });
    }
   //Call
    displayFavorites();
});

