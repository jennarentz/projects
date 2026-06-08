# Movie Explorer

Movie Explorer is a React app that lets users browse, search, filter, and save movies. It uses The Movie Database API to display popular movies and movie details.

## Features

- Browse popular movies
- Search for movies by title
- Filter movies by genre, year, and rating
- View detailed movie information
- Save favorite movies
- View saved favorites on a separate page
- Responsive movie card layout

## Tech Stack

- React
- Vite
- React Router
- JavaScript
- CSS
- The Movie Database API

## Project Structure

```text
movie-explorer/
└── frontend/
    ├── public/
    ├── src/
    │   ├── components/
    │   ├── contexts/
    │   ├── css/
    │   ├── pages/
    │   ├── services/
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    └── vite.config.js
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/jennarentz/projects.git
cd projects/movie-explorer/frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Set Up the API Key

This project uses The Movie Database API.

Create a `.env` file inside the `frontend` folder:

```env
VITE_TMDB_API_KEY=your_tmdb_api_key
```

Then make sure the API service file uses:

```js
const API_KEY = import.meta.env.VITE_TMDB_API_KEY;
```

## How to Run

From the `frontend` folder:

```bash
npm run dev
```

Then open the local Vite URL in your browser.

## How to Use

1. Open the app in your browser.
2. Browse the popular movies displayed on the home page.
3. Use the search bar to search for a specific movie.
4. Use filters to narrow movies by genre, year, or rating.
5. Click on a movie to view more details.
6. Click the favorite button to save a movie.
7. Go to the Favorites page to view saved movies.

## Future Improvements

- Add pagination for search results
- Add user accounts
- Store favorites in a backend database
- Improve mobile styling
