document.getElementById('search-bar').addEventListener('input', function() {
    let query = this.value;
    if (query.length > 2) {
        fetchSuggestions(query);
    } else {
        document.getElementById('suggestions').innerHTML = '';
    }
});

function fetchSuggestions(query) {
    fetch(`https://api.themoviedb.org/3/search/movie?api_key=YOUR_API_KEY&query=${query}`)
        .then(response => response.json())
        .then(data => displaySuggestions(data.results))
        .catch(error => console.error('Error fetching data:', error));
}

function displaySuggestions(movies) {
    const suggestionsBox = document.getElementById('suggestions');
    suggestionsBox.innerHTML = '';
    movies.forEach(movie => {
        const suggestionItem = document.createElement('div');
        suggestionItem.classList.add('suggestion');
        suggestionItem.innerHTML = `
            <img src="https://image.tmdb.org/t/p/w92${movie.poster_path}" alt="${movie.title}">
            <p>${movie.title}</p>
        `;
        suggestionsBox.appendChild(suggestionItem);
    });
}
