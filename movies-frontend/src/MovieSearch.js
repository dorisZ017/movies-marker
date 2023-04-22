import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MovieSearch.css";

const MovieSearch = () => {
  const [title, setTitle] = useState("");
  const [actor, setActor] = useState("");
  const [genre, setGenre] = useState("");
  const [year, setYear] = useState("");
  const [movies, setMovies] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [operation, setOperation] = useState("");
  const [operationInput, setOperationInput] = useState("");
  const [selectedOperation, setSelectedOperation] = useState("");

  const handleSearch = async (event) => {
    event.preventDefault();
    const res = await axios.get("http://localhost:5000/search", {
      proxy: {
        host: "cors-proxy.com",
      },
      params: {
        title: title,
        actor: actor,
        genre: genre,
        year: year,
      },
    });
    setMovies(res.data);
  };

  const handleOperationSelect = (operation) => {
    setOperation(operation)
    setSelectedOperation(operation)
  }

  const handleOperationSubmit = async (event) => {
    console.log("here!")
    console.log(operation)
    console.log(operationInput)
    const res = await axios.post("http://localhost:5000/operation", {
      proxy: {
        host: "cors-proxy.com",
      },
      params: {
      title: selectedMovie._source.title,
      operation: operation,
      input: operationInput,
      }
    });
    console.log(res.data);
    setSelectedMovie(null);
    setOperation("")
    setOperationInput("");
  };

  return (
    <div>
      <form onSubmit={handleSearch}>
        <label>
          Title:
          <input type="text" value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>
        <br />
        <label>
          Actor:
          <input type="text" value={actor} onChange={(event) => setActor(event.target.value)} />
        </label>
        <br />
        <label>
          Genre:
          <input type="text" value={genre} onChange={(event) => setGenre(event.target.value)} />
        </label>
        <br />
        <label>
          Release Year:
          <input type="text" value={year} onChange={(event) => setYear(event.target.value)} />
        </label>
        <br />
        <button type="submit">Search</button>
      </form>
      <div>
        {movies.map((movie) => (
          <div key={movie._id}>
            <img src={movie._source.poster_url} alt={movie._source.title} />
            <h2>{movie._source.title}</h2>
            <p>Actors: {movie._source.actors}</p>
            <p>Genres: {movie._source.genres}</p>
            <p>Release Year: {movie._source.release_year}</p>
            <button onClick={() => setSelectedMovie(movie)}>Select</button>
            <div>
              <label>
                Select operation:
                <select value={selectedOperation} onChange={(event) => handleOperationSelect(event.target.value)}>
                  <option value="like">Like</option>
                  <option value="rate">Rate</option>
                  <option value="add_review">Add Review</option>
                  <option value="bookmark">Bookmark</option>
                </select>
              </label>
              {selectedOperation === "rate" && (
                <label>
                  Rate:
                  <input type="number" min="1" max="5" onChange={(event) => setOperationInput(event.target.value)} />
                </label>
              )}
              {selectedOperation === "add_review" && (
                <label>
                  Review:
                  <input type="text" onChange={(event) => setOperationInput(event.target.value)} />
                </label>
              )}
              <button onClick={() => handleOperationSubmit(selectedMovie._source.title)}>Submit</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

};

export default MovieSearch;