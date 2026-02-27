import type { BuildingData } from '../buildingDataExtract';
import styles from './Card.module.css'

interface CardProps {
  building: BuildingData
}

export default function Card({ building }: CardProps) {
  const { building_picture, name, rooms_available } = building;

  return (
    <div className={styles.card}>
      <img src={building_picture} alt={name} className={styles.image} />
      <div className={styles.badge}>
        <div className={styles.dot} />
        <span className={styles.badge_desktop}>{rooms_available} rooms available</span>
        <span className={styles.badge_mobile}>{rooms_available} / {rooms_available}</span>
      </div>
      <div className={styles.label}>
        {name}
      </div>
    </div>
  )
}
