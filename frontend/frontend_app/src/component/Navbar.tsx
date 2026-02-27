import { useState } from 'react'
import IconButton from '@mui/material/IconButton'
import styles from './Navbar.module.css'
const logoOpen = '/assets/freeRoomsLogo.png'
const logoClosed = '/assets/freeroomsDoorClosed.png'

export default function Navbar() {
  const [doorOpen, useDoor] = useState(true)
  const [activeView, setActiveView] = useState('grid')

  return (
    <nav className={styles.navbar}>
      <div className={styles.logo} onClick={() => useDoor(doorOpen => !doorOpen)}>
        <img
          src={doorOpen ? logoOpen : logoClosed}
          alt="Freerooms Logo"
          className={styles.logoImg}
        />
        <span className={styles.logoText}>Freerooms</span>
      </div>

      <div className={styles.actions}>
        <IconButton
          aria-label="Search"
          onClick={() => setActiveView('search')}
          className={`${styles.iconBtn} ${activeView === 'search' ? styles.iconBtnActive : ''}`}
        >
          <span className="material-icons">search</span>
        </IconButton>
        <IconButton
          aria-label="Grid View"
          onClick={() => setActiveView('grid')}
          className={`${styles.iconBtn} ${activeView === 'grid' ? styles.iconBtnActive : ''}`}
        >
          <span className="material-icons">grid_view</span>
        </IconButton>
        <IconButton
          aria-label="Map"
          onClick={() => setActiveView('map')}
          className={`${styles.iconBtn} ${activeView === 'map' ? styles.iconBtnActive : ''}`}
        >
          <span className="material-icons">map</span>
        </IconButton>
        <IconButton
          aria-label="Dark Mode"
          onClick={() => setActiveView('dark')}
          className={`${styles.iconBtn} ${activeView === 'dark' ? styles.iconBtnActive : ''}`}
        >
          <span className="material-icons">dark_mode</span>
        </IconButton>
      </div>
    </nav>
  )
}