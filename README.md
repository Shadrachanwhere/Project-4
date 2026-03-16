GROCERY STORE INVENTORY(APPLICATION)
 A Python-based Command Line Interface (CLI) application designed to manage a store's inventory. 
 This tool uses **SQLAlchemy ORM** and a **SQLite** database to track brands and products, 
 handle data cleaning, and provide business analytics.

FEATURES OF THIS APPILICATION
**Data Ingestion:** Automatically imports and cleans data from `brands.csv` and `inventory.csv` on startup.
- **View Product:** Look up specific items by their Unique ID.
- **Add New Product:** Input new inventory with automatic price-to-cents conversion.
- **Inventory Analysis:** Identify the most/least expensive items and the brand with the highest product count.
- **Database Backup:** Export the current database state back into a clean `.csv` format.


