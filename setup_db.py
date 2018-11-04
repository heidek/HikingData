import sqlite3

def main():
	db = sqlite3.connect('db/hikes.db')
	c = db.cursor()

	c.execute('''CREATE TABLE IF NOT EXISTS hikes (
	name TEXT,
	region TEXT,
	area TEXT,
	subarea TEXT,
	length TEXT,
	gain TEXT, 
	max_elevation TEXT
	)''')

	db.commit()
	db.close()

if __name__ == '__main__':
	main()