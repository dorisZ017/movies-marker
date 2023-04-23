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
  const [operation, setOperation] = useState("like");
  const [operationInput, setOperationInput] = useState("");
  const [selectedOperation, setSelectedOperation] = useState("");
  const [viewOp, setViewOp] = useState("")
  const [opsMovies, setOpsMovies] = useState([])

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
    if (selectedMovie) {
    console.log(operationInput)
      const res = await axios.post("http://localhost:5000/add_operation", {
      proxy: {
        host: "cors-proxy.com",
      },
      params: {
      title: selectedMovie._source.title,
      release_year: selectedMovie._source.release_year,
      operation: operation,
      input: operationInput,
      }
    });
    console.log(res.data);
    setSelectedMovie(null);
    setOperationInput("");
    }
  };

  const handleView = operation => async(event) => {
    const res = await axios.get("http://localhost:5000/get_movies", {
      proxy: {
        host: "cors-proxy.com",
      },
      params: {
        operation: operation,
      }
    });
    setOpsMovies(res.data);
  };


  return (
    <div>
      <h2>Search Movies</h2>
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
      <h2> My Movies </h2>
      <p>
      <button onClick={handleView("like")}>Liked</button>
      <button onClick={handleView("bookmark")}>Bookmarked</button>
      <button onClick={handleView("rate")}>Rated</button>
      <button onClick={handleView("review")}>Reviewed</button>
      </p>
      </div>
      <div>
      {opsMovies.map((om) =>
        <div>
        <h3>{om.title}({om.release_year})</h3>
        <p>Added At: {om.activity_time}</p>
        <p>Detail: {om.detail}</p>
        </div>
      )}
      </div>
      <div>
        {movies.length > 0 && (<h2> Search Results: </h2>)}
        {movies.map((movie) => (
          <div key={movie._id}>
            <h3>{movie._source.title}</h3>
            <p>Actors: {movie._source.actors}</p>
            <p>Genres: {movie._source.genres}</p>
            <p>Release Year: {movie._source.release_year}</p>
            <img src={movie._source.poster_url} alt={movie._source.title} />
            <p><button onClick={() => setSelectedMovie(movie)}>Select</button></p>
            <div>
              <label>
                Select operation:
                <select value={selectedOperation} onChange={(event) => handleOperationSelect(event.target.value)}>
                  <option value="like">Like</option>
                  <option value="rate">Rate</option>
                  <option value="review">Add Review</option>
                  <option value="bookmark">Bookmark</option>
                </select>
              </label>
              {selectedOperation === "rate" && (
                <label>
                  Rate:
                  <input type="number" min="1" max="5" onChange={(event) => setOperationInput(event.target.value)} />
                </label>
              )}
              {selectedOperation === "review" && (
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