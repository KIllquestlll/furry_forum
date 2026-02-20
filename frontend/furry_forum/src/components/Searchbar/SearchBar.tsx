import { useState } from "react";
import { useNavigate } from "react-router-dom"; 
import styles from './SearchBar.module.css';

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
      className={styles.Searchbar}
    >
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder='Search'
        className={styles.SearchInput} />
      <button type="submit"
        disabled={!input}
        className={styles.SearchButton}
      >
        🔍
      </button>
    </form>
  );
}

export default SearchBar;