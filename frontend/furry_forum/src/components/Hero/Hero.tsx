import { useState, useEffect } from "react";
import styles from "./Hero.module.css";
import heroBg from "../../assets/hero-background.png";
import { categories } from "../constants";
import axios from "axios";

export function Hero() {
    // fetch the data
    const [posts, setPosts] = useState([]);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get("http://localhost:8000/posts", 
                    {
                        params: { categories: categories.join(",")}
                    });
                    
                    setPosts(response.data);
                } catch(error) {
                    console.error("Ошибка запроса: ", error);
                } finally {
                    setLoading(false);
                }
        };
        fetchPosts();
    }, []);

    return (
        <div 
            className={styles.hero}
            
            style={{ backgroundImage: `url(${heroBg})`,
             }}
        >
            <div className={styles.heroOverlay}>
                <h1 className={styles.heroTitle}>Rainbow Dash Day!</h1>
            </div>
        </div>
    )
}
