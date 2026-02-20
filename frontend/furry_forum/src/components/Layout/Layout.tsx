import styles from "./Layout.module.css"
import { Header } from "../Header/Header"
import { Hero } from "../Hero/Hero"
import { Footer }from "../Footer/Footer"
import { NavigationBar } from "../NavBar/NavBar"


type LayoutProps = {
    children: React.ReactNode
}

export function Layout({ children }: LayoutProps) {
    return (
        <div className={`${styles.layout} bg-[#2c2c2c] bg-[#ebe6ff] transition-all
        duration-7`}>
            <Header />
            <Hero />
            <NavigationBar />
            <main className={`${styles.mainContent} `}>
                {children}
            </main>
            <Footer />
        </div>
    );
}