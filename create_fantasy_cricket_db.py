import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('fantasy_cricket.db')
cursor = conn.cursor()

# ------------------ DROP TABLES IF THEY EXIST ------------------
cursor.execute("DROP TABLE IF EXISTS stats")
cursor.execute("DROP TABLE IF EXISTS match")
cursor.execute("DROP TABLE IF EXISTS teams")

# ------------------ CREATE TABLES ------------------

cursor.execute("""
CREATE TABLE stats (
    player TEXT PRIMARY KEY,
    matches INTEGER,
    runs INTEGER,
    hundreds INTEGER,
    fifties INTEGER,
    value REAL,
    ctg TEXT
)
""")

cursor.execute("""
CREATE TABLE match (
    match_id INTEGER,
    player TEXT,
    scored INTEGER,
    faced INTEGER,
    fours INTEGER,
    sixes INTEGER,
    bowled INTEGER,
    maiden INTEGER,
    given INTEGER,
    wkts INTEGER,
    catches INTEGER,
    stumping INTEGER,
    ro INTEGER,
    PRIMARY KEY (match_id, player)
)
""")

cursor.execute("""
CREATE TABLE teams (
    name TEXT PRIMARY KEY,
    players TEXT,
    value REAL
)
""")

# ------------------ INSERT DATA ------------------

# Sample player stats
sample_stats = [
    ('Virat Kohli', 250, 12000, 43, 62, 9.5, 'BAT'),
    ('Rohit Sharma', 230, 9500, 30, 47, 9.0, 'BAT'),
    ('Shubman Gill', 50, 2000, 4, 12, 8.0, 'BAT'),
    ('Suryakumar Yadav', 45, 1800, 2, 10, 8.2, 'BAT'),
    ('Shikhar Dhawan', 150, 6000, 17, 29, 8.3, 'BAT'),
    ('Ajinkya Rahane', 90, 3200, 4, 18, 7.5, 'BAT'),
    ('Cheteshwar Pujara', 100, 4800, 10, 23, 7.8, 'BAT'),
    ('Prithvi Shaw', 25, 850, 1, 5, 7.2, 'BAT'),
    ('Hardik Pandya', 70, 1500, 0, 6, 8.5, 'ALL'),
    ('Ravindra Jadeja', 180, 2200, 1, 9, 9.0, 'ALL'),
    ('Axar Patel', 60, 1000, 0, 4, 7.5, 'ALL'),
    ('Washington Sundar', 35, 700, 0, 3, 7.8, 'ALL'),
    ('Vijay Shankar', 20, 400, 0, 2, 7.0, 'ALL'),
    ('Shivam Dube', 15, 350, 0, 1, 7.4, 'ALL'),
    ('KL Rahul', 100, 4000, 6, 25, 9.0, 'WK'),
    ('Rishabh Pant', 70, 2100, 5, 12, 8.5, 'WK'),
    ('Ishan Kishan', 30, 900, 2, 6, 7.5, 'WK'),
    ('Sanju Samson', 45, 1100, 3, 10, 8.2, 'WK'),
    ('Dinesh Karthik', 110, 2700, 2, 18, 7.9, 'WK'),
    ('Jasprit Bumrah', 110, 120, 0, 0, 8.5, 'BWL'),
    ('Mohammed Shami', 90, 100, 0, 0, 8.0, 'BWL'),
    ('Yuzvendra Chahal', 80, 150, 0, 0, 7.8, 'BWL'),
    ('Kuldeep Yadav', 65, 300, 0, 0, 7.9, 'BWL'),
    ('Bhuvneshwar Kumar', 115, 400, 0, 1, 8.0, 'BWL'),
    ('Ravichandran Ashwin', 140, 700, 1, 4, 8.6, 'BWL'),
    ('Umran Malik', 10, 50, 0, 0, 7.5, 'BWL'),
    ('Mohammed Siraj', 30, 90, 0, 0, 7.7, 'BWL'),
    ('Arshdeep Singh', 25, 70, 0, 0, 7.6, 'BWL'),
    ('Deepak Chahar', 20, 80, 0, 1, 7.4, 'BWL')
]
cursor.executemany('INSERT INTO stats VALUES (?, ?, ?, ?, ?, ?, ?)', sample_stats)

# Match data (3 matches)
sample_matches = [
    (1, 'Virat Kohli', 80, 60, 6, 2, 0, 0, 0, 0, 1, 0, 0),
    (1, 'Rohit Sharma', 45, 50, 4, 1, 0, 0, 0, 0, 0, 0, 0),
    (1, 'Hardik Pandya', 30, 25, 3, 1, 24, 1, 20, 1, 1, 0, 0),
    (1, 'KL Rahul', 65, 40, 7, 2, 0, 0, 0, 0, 2, 0, 1),
    (1, 'Jasprit Bumrah', 5, 7, 0, 0, 24, 2, 15, 3, 0, 0, 0),
    (2, 'Ravindra Jadeja', 35, 28, 2, 1, 24, 1, 22, 2, 1, 0, 0),
    (2, 'Axar Patel', 28, 23, 2, 0, 18, 1, 18, 1, 0, 0, 0),
    (2, 'Rishabh Pant', 50, 42, 4, 2, 0, 0, 0, 0, 1, 1, 0),
    (2, 'Kuldeep Yadav', 10, 12, 0, 0, 24, 2, 18, 3, 0, 0, 0),
    (2, 'Shubman Gill', 55, 45, 5, 1, 0, 0, 0, 0, 1, 0, 0),
    (3, 'Sanju Samson', 60, 38, 6, 2, 0, 0, 0, 0, 2, 0, 1),
    (3, 'Mohammed Shami', 12, 10, 1, 0, 24, 1, 21, 2, 0, 0, 0),
    (3, 'Bhuvneshwar Kumar', 8, 10, 0, 0, 24, 1, 19, 2, 0, 0, 0),
    (3, 'Ishan Kishan', 38, 33, 3, 1, 0, 0, 0, 0, 1, 0, 0),
    (3, 'Ajinkya Rahane', 40, 36, 4, 1, 0, 0, 0, 0, 0, 0, 0)
]
cursor.executemany('INSERT INTO match VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_matches)

# Sample teams
sample_teams = [
    ('Royal Challengers', 'Virat Kohli, Rohit Sharma, Shubman Gill, Hardik Pandya, Ravindra Jadeja, KL Rahul, Rishabh Pant, Jasprit Bumrah, Mohammed Shami, Axar Patel, Sanju Samson', 95.0),
    ('Chennai Kings', 'Virat Kohli, Hardik Pandya, Axar Patel, KL Rahul, Rishabh Pant, Shubman Gill, Ravindra Jadeja, Jasprit Bumrah, Mohammed Shami, Bhuvneshwar Kumar, Kuldeep Yadav', 94.8),
    ('Mumbai Indians', 'Rohit Sharma, Ishan Kishan, Suryakumar Yadav, Hardik Pandya, Bumrah, Shami, Jadeja, Gill, Pant, Axar Patel, Yuzvendra Chahal', 93.2),
    ('Delhi Capitals', 'Pant, Shaw, Kuldeep, Axar, Shami, Kohli, Gill, Rahul, Bumrah, Pandya, Dhawan', 92.4),
    ('Sunrisers Hyderabad', 'Gill, Umran, Chahal, Jadeja, Rahul, Samson, Pant, Siraj, Hardik, Axar, Rohit', 91.8),
    ('Punjab Kings', 'Sanju, Chahar, Sundar, Dhawan, Hardik, Gill, Rahul, Pant, Shami, Chahal, Bumrah', 91.5)
]
cursor.executemany('INSERT INTO teams VALUES (?, ?, ?)', sample_teams)

# ------------------ COMMIT & CLOSE ------------------

conn.commit()
conn.close()
print("✅ Fantasy Cricket DB created successfully with all sample data.")
