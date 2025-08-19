import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import "../css/MovieDetails.css";

const API_KEY = "dcaf3875660294871c4a8078104280f9";

function MovieDetails() {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true); // <-- controls loading state
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const res = await fetch(`https://api.themoviedb.org/3/movie/${id}?api_key=${API_KEY}`);
        if (!res.ok) throw new Error("Failed to fetch movie details");
        const data = await res.json();
        setMovie(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false); // <-- Make sure this is inside finally!
      }
    };

    fetchMovie();
  }, [id]);
  

  if (loading) return <p>Loading...</p>;
  if(error) return <p>{error}</p>

  return (
    <div className="movie-details">
      <h2>{movie.title}</h2>
      <img src={`https://image.tmdb.org/t/p/w500/${movie.poster_path}`} alt={movie.title} />
      <p>{movie.overview}</p>
      <p><strong>Genres:</strong> {movie.genres.map(g => g.name).join(", ")}</p>
      <p><strong>Release Date:</strong> {movie.release_date}</p>
      <p><strong>Rating:</strong> {movie.vote_average}</p>
    </div>
  );
}

export default MovieDetails;
