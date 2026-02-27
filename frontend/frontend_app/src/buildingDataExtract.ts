import dataJson from '@data'

export interface BuildingData {
  name: string
  rooms_available: number
  building_picture: string
}

export const buildings: BuildingData[] = dataJson.map((entry) => {
  const filename = (entry.building_picture || entry.building_file || '').replace('./', '')
  
  return {
    name: entry.name,
    rooms_available: entry.rooms_available,
    building_picture: `/assets/${filename}`
  }
})