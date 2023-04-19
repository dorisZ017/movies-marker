import React, { useState, useEffect } from "react";
import axios from "axios";
import './MovieSearch.css';

const MovieSearch = () => {
  const [title, setTitle] = useState("");
  const [actor, setActor] = useState("");
  const [genre, setGenre] = useState("");
  const [year, setYear] = useState("");
  const [movies, setMovies] = useState([]);

  const handleSearch = async (event) => {
    event.preventDefault();
    const res = await axios.get("http://localhost:5000/search", {
      proxy: {
        host: 'cors-proxy.com',
      },
      params: {
        title: title,
        actor: actor,
        genre: genre,
        year: year
      }
    });
    setMovies(res.data);
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <label>
          Title:
          <input type="text" value={title} onChange={event => setTitle(event.target.value)} />
        </label>
        <br />
        <label>
          Actor:
          <input type="text" value={actor} onChange={event => setActor(event.target.value)} />
        </label>
        <br />
        <label>
          Genre:
          <input type="text" value={genre} onChange={event => setGenre(event.target.value)} />
        </label>
        <br />
        <label>
          Release Year:
          <input type="text" value={year} onChange={event => setYear(event.target.value)} />
        </label>
        <br />
        <button type="submit">Search</button>
      </form>
      <div>
        {movies.map(movie => (
          <div key={movie._id}>
            <img src={movie._source.poster_url} alt={movie._source.title} />
            <h2>{movie._source.title}</h2>
            <p>Actors: {movie._source.actors}</p>
            <p>Genres: {movie._source.genres}</p>
            <p>Release Year: {movie._source.release_year}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MovieSearch;
