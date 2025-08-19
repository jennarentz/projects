import { useEffect, useState } from "react";
import { getGenres } from "../services/api";
import "../css/Filters.css";

function Filters({ onFilter }) {
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState("");
  const [selectedYear, setSelectedYear] = useState("");
  const [selectedRating, setSelectedRating] = useState("");

  useEffect(() => {
    const fetchGenres = async () => {
      const genreList = await getGenres();
      setGenres(genreList);
    };
    fetchGenres();
  }, []);

  const handleFilterChange = () => {
    onFilter({
      genre: selectedGenre,
      year: selectedYear,
      rating: selectedRating,
    });
  };

  return (
    <div className="filters-container">
        <div className="filter-group">
            <label>Genre</label>
            <select 
                value={selectedGenre} 
                onChange={(e) => { 
                    setSelectedGenre(e.target.value); 
                    handleFilterChange(); 
                }}
            >
                <option value="">All Genres</option>
                {genres.map((g) => (
                    <option key={g.id} value={g.id}>
                        {g.name}
                    </option>
                ))}
            </select>
        </div>

        <div className="filter-group">
            <label>Year</label>
            <input
            type="number"
            placeholder="Year (e.g. 2020)"
            value={selectedYear}
            onChange={(e) => {
            setSelectedYear(e.target.value);
            handleFilterChange();
            }}
        />
        </div>

        <div className="filter-group">
            <label>Min Rating</label>
            <input
            type="number"
            placeholder="Min Rating (1-10)"
            value={selectedRating}
            onChange={(e) => {
            setSelectedRating(e.target.value);
            handleFilterChange();
            }}
        />
        </div>
    </div>
  );
}

export default Filters;
