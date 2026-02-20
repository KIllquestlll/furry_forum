import { useState, useEffect } from "react";
import styles from "./Hero.module.css";
import heroBg from "../../assets/hero-background.png";
import axios from "axios";

export function Hero() {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                // 1. Пытаемся взять данные с бэкенда
                const response = await axios.get("http://127.0.0.1:8000/api/category/show");
                setPosts(response.data);
            } catch (error) {
                console.warn("Бэкенд недоступен, загружаю локальный файл...");

                try {
                    // 2. ПЛАН Б: Загружаем локальный JSON из папки public
                    // Путь "/data/categories.json" соответствует файлу в public/data/categories.json
                    const fallback = await axios.get("/data/categories.json");
                    setPosts(fallback.data);
                } catch (fallbackError) {
                    console.error("Даже локальный файл не найден!", fallbackError);
                }
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
