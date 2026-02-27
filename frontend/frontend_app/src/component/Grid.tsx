import { buildings } from '../buildingDataExtract'
import BuildingCard from './Card'
import styles from './Grid.module.css'

export default function BuildingGrid() {
  return (
    <main className={styles.grid}>
      {buildings.map((building) => (
        <BuildingCard key={building.name} building={building} />
      ))}
    </main>
  )
}