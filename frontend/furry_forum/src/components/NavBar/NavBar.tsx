import { useState } from "react"
import { Link } from "react-router-dom"
import styles from "./NavBar.module.css"

type NavItem = {
    label: string
    path: string
    submenu?: NavItem[]
}

const navItems: NavItem[] = [
    { label: "Home", path: "/" },
    { label: "Art", path: "/art",
        submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },
            { label: "Pony Soapbox", path: "/community/pony-soapbox" },
            { label: "Discussion", path: "/community/discussion" },
            { label: "Convention List", path: "/community/convention-list" },
            { label: "Discord Server", path: "/community/discord-server" },
            { label: "Polls", path: "/community/polls" },
        ]
     },
    { label: "News", path: "/news",
            submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },

        ]
    },
    { label: "Fics", path: "/fics",
            submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },
        ]
     },
    { label: "Media", path: "/media",
            submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },
        ]
    },
    { label: "Comics", path: "/comics",
            submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },
        ]
     },
    { label: "Community", path: "/community",
        submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },
            { label: "Pony Soapbox", path: "/community/pony-soapbox" },
        ]
    },
    { label: "Editorial", path: "/editorial",
            submenu: [
            { label: "EQD Staff", path: "/community/eqd-staff" },
            { label: "Pony Soapbox", path: "/community/pony-soapbox" },
            ]
     },
    { label: "Submit", path: "/submit",
            submenu: [
            { label: "Sign up", path: "/authorization "},
            { label: "Sign in with Google", path: "/authorization "},
            { label: "Sign in with Github", path: "/authorization "},
            ]
    },
]

export function NavigationBar() {
    const [openMenu, setOpenMenu] = useState<string | null>(null)

    return (
        <nav className={styles.navbar}>
            <ul className={styles.navList}>
                {navItems.map(item => (
                    <NavDropdown
                        key={item.label}
                        item={item}
                        isOpen={openMenu === item.label}
                        onToggle={() => setOpenMenu(
                            openMenu === item.label ? null : item.label
                        )}
                        onClose={() => setOpenMenu(null)}
                    />
                ))}
            </ul>
        </nav>
    )
}

type NavDropdownProps = {
    item: NavItem
    isOpen: boolean
    onToggle: () => void
    onClose: () => void
}

function NavDropdown({ item, isOpen, onToggle, onClose }: NavDropdownProps) {
    return (
        <li 
            className={styles.navItem}
            onMouseEnter={() => item.submenu && onToggle()}
            onMouseLeave={onClose}
        >
            <Link 
                to={item.path} 
                className={styles.navLink}
            >
                {item.label}
            </Link>
            
            {item.submenu && (
                <ul className={`${styles.submenu} ${isOpen ? styles.show : ""}`}>
                    {item.submenu.map(subItem => (
                        <li key={subItem.label} className={styles.submenuItem}>
                            <Link 
                                to={subItem.path}
                                className={styles.submenuLink}
                            >
                                {subItem.label}
                            </Link>
                        </li>
                    ))}
                </ul>
            )}
        </li>
    )
}
