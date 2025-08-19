import MovieCard from "../components/MovieCard"
import {useState, useEffect} from "react"
import {searchMovies, getPopularMovies} from "../services/api"
import Filters from "../components/Filters";
import "../css/Home.css"

function Home() {
    //rerender component based on state - updates
    const [searchQuery, setSearchQuery] = useState("");
    const [movies, setMovies] = useState([]);
    //also need a state to catch errors
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true)

    const [filteredMovies, setFilteredMovies] = useState([]);
    const [filters, setFilters] = useState({ genre: "", year: "", rating: "" });


    //allows you to run side effects like getting api data
    useEffect(() => {
        const loadPopularMovies = async () => {
            try {
                const popularMovies = await getPopularMovies()
                setMovies(popularMovies)
            } catch(err) {
                console.log(err)
                setError("Failed to load movies...")
            }
            finally {
                setLoading(false)
            }
        }
        loadPopularMovies()
    }, [])

    // When API movies are fetched
    useEffect(() => {
        applyFilters(movies);
    }, [movies, filters]);

    const handleSearch = async (e) => {
        //won't update the page after search
        e.preventDefault()
        //won't search anything if user only types spaces - removes all spaces
        if (!searchQuery.trim()) return
        //won't allow to search if already searching for something else
        if(loading) return 

        setLoading(true)
        try {
            const searchResults = await searchMovies(searchQuery)
            setMovies(searchResults)
            setError(null)
        } catch (err) {
            console.log(err)
            setError("Failed to search movies...")
        } finally {
            setLoading(false)
        }

        setSearchQuery("")
    };

    // When API movies are fetched
    useEffect(() => {
    applyFilters(movies);
    }, [movies, filters]);

    const applyFilters = (allMovies) => {
    let result = [...allMovies];

    if (filters.genre) {
        result = result.filter((movie) => movie.genre_ids.includes(Number(filters.genre)));
    }

    if (filters.year) {
        result = result.filter((movie) => movie.release_date?.startsWith(filters.year));
    }

    if (filters.rating) {
        result = result.filter((movie) => movie.vote_average >= Number(filters.rating));
    }

    setFilteredMovies(result);
    };

    return <div className="home">
        <form onSubmit={handleSearch} className="search-form">
            {/* setSearchQuery updates state from input - allows user to type in search*/}
            <input 
                type="text" 
                placeholder="Search for movies..." 
                className="search-input"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button type="submit" className="search-button">Search</button>
        </form>

            {error && <div className="error-message">{error}</div>}

        {/*if loading display message otherwise display grid */}
        {loading ? (
            <div className="loading">Loading...</div> 
        ) : (
            <>
                <Filters onFilter={setFilters} />
                <div className="movies-grid">
                    {/* iterates over each movie*/}
                    {/*could use movie.title.toLowerCase().startsWith(searchQuery) && to search */}
                    {filteredMovies.map((movie) => (
                        <MovieCard movie={movie} key={movie.id}/>
                    ))}
                </div>
            </>
        )}
    </div>
};

export default Home