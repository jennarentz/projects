import './css/App.css'
import Home from "./pages/Home"
import Favorites from './pages/Favorites';
import MovieDetails from "./pages/MovieDetails";
import {Routes, Route} from "react-router-dom";
import { MovieProvider } from './contexts/MovieContext';
import NavBar from './components/NavBar';

//component
function App() {
  return (
    // can't have multiple divs at same level (one root/parent element)
    // instead return a fragment - empty html tag
    //need second set of braces for object
    <MovieProvider>
      <NavBar/>
      <main className='main-content'>
        <Routes>
          <Route path='/' element={<Home />}/>
          <Route path='/favorites' element={<Favorites />}/>
          <Route path="/movie/:id" element={<MovieDetails />} />
        </Routes>
      </main>
    </MovieProvider>
  );
}

export default App
