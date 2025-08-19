import {createContext, useState, useContext, useEffect} from "react"

const MovieContext = createContext()

export const useMovieContext = () => useContext(MovieContext)

//any component in app can access state- which movies are favorited
//since app is inside component it's automatically added to children prop
export const MovieProvider = ({children}) => {
    const [favorites, setFavorites] = useState([])

    //look in storage for movies
    useEffect(() => {
        const storedFavs = localStorage.getItem("favorites")

        if (storedFavs) setFavorites(JSON.parse(storedFavs))
    }, [])

    //updates whats stored in local storage
    useEffect(() => {
        localStorage.setItem('favorites', JSON.stringify(favorites))
    }, [favorites])

    const addToFavorites = (movie) => {
        setFavorites(prev => [...prev, movie])
    }

    const removeFromFavorites = (movieId) => {
        setFavorites(prev => prev.filter(movie => movie.id !== movieId))
    }

    //searches for movie id in favorites and returns true or false
    const isFavorite = (movieId) => {
        return favorites.some(movie => movie.id === movieId)
    }

    //children to pass
    const value = {
        favorites,
        addToFavorites,
        removeFromFavorites,
        isFavorite
    }

    return <MovieContext.Provider value={value}>
        {children}
    </MovieContext.Provider>
}