from Database import Database

db = Database("/Users/Goon/Desktop/Duke/ECE496/PFHV/db/db.ini")

print(db.macro_regional_df.head())
print(db.homes_df.head())
print(db.history_df.head())
print(db.macro_national_df.head())
