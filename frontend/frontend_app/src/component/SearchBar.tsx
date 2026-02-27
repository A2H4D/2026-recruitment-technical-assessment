import styles from './SearchBar.module.css'

export default function SearchBar() {
    return (
        <div className={styles.filterBar}>
            {/* Filters button */}
            <button className={styles.filtersBtn}>
            <span className="material-icons">filter_alt</span>
            Filters
            </button>

            {/* Search input */}
            <div className={styles.searchWrapper}>
            <span className={`material-icons ${styles.searchIcon}`}>search</span>
            <input
                className={styles.searchInput}
                type="text"
                placeholder="Search for a building..."
            />
            </div>

            {/* Sort button */}
            <button className={styles.sortBtn}>
            <span className="material-icons">filter_list</span>
            Sort
            </button>
        </div>
    )
}