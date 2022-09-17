tables_sql = (
"PRAGMA foreign_keys = ON;",
"BEGIN TRANSACTION;",
'''
CREATE TABLE IF NOT EXISTS "klienti" (
"klienti_id"	INTEGER,
"jmeno"	TEXT NOT NULL,
"prijmeni"	TEXT NOT NULL,
"datum_narozeni"	TEXT NOT NULL,
"telefon"	NUMERIC,
PRIMARY KEY("klienti_id" AUTOINCREMENT)
);
''',
"""
CREATE TABLE IF NOT EXISTS klienti_smlouvy(
	klienti_smlouvy_id INTEGER,
	klient_id INTEGER NOT NULL,
	smlouva_id INTEGER NOT NULL,
	datum_zalozeni TEXT NOT NULL,
	datum_ukonceni TEXT NOT NULL,
	PRIMARY KEY(klienti_smlouvy_id AUTOINCREMENT),
	FOREIGN KEY (klient_id)
	REFERENCES klienti(klienti_id)
	ON DELETE CASCADE
	);
""",
"""
CREATE TABLE IF NOT EXISTS smlouvy(
smlouvy_id INTEGER,
nazev TEXT,
popis TEXT,
PRIMARY KEY(smlouvy_id AUTOINCREMENT)
);
""",
"COMMIT TRANSACTION;"
)