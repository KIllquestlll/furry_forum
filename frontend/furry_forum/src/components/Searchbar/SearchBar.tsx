"use client";
import { useState } from "react";
import { useNavigate } from "react-router-dom"; 

function SearchBar() {
  const [input, setInput] = useState("");
  const navigate = useNavigate(); 

  function handleSearch(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (!input) return;
    
    navigate(`/search?q=${input}`);
  }

  return ( 
    <form
      onSubmit={handleSearch}
      className=""
    >
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder='Search'
        className="" />
      <button type="submit"
        disabled={!input}
        className="text-blue-400 disabled:text-gray-400"
      >
        Search
      </button>
    </form>
  );
}

export default SearchBar;