from Database import Database

db = Database("/Users/hannahtaubenfeld/Documents/duke/S21/ECE496/PFHV/db/db.ini")

print(db.zipcode_to_region_df.head())
print(db.regions_df.head())
print(db.macro_regional_df.head())