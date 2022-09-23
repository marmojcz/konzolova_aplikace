tables_sql = (
"PRAGMA foreign_keys = ON;",
"BEGIN TRANSACTION;",
#### TABLE USERS ####
'''
CREATE TABLE IF NOT EXISTS users_auth(
users_id TEXT PRIMARY KEY,
hash_passwd TEXT NOT NULL,
admin INTEGER DEFAULT 0
);
''',
### TABLE KLIENTI
'''
CREATE TABLE IF NOT EXISTS "klienti" (
"klienti_id"	INTEGER,
"jmeno"	TEXT NOT NULL,
"prijmeni"	TEXT NOT NULL,
"datum_narozeni"	TEXT NOT NULL,
"telefon"	NUMERIC,
"email" TEXT NOT NULL,
PRIMARY KEY("klienti_id" AUTOINCREMENT)
FOREIGN KEY(email)
REFERENCES users_auth(users_id)
ON DELETE CASCADE
);
''',
###	TABLE SMLOUVY ####
"""
CREATE TABLE IF NOT EXISTS smlouvy(
smlouvy_id INTEGER,
nazev TEXT,
popis TEXT,
PRIMARY KEY(smlouvy_id AUTOINCREMENT)
);
""",
#### TABLE KLIENTI_SMLOUVY ####
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
"COMMIT TRANSACTION;"
)


DATA_SMLOUVY = [
	("Životní pojištění"," Životní pojištění si můžete nastavit tak, aby odpovídalo vašemu aktuálnímu příjmu a životnímu stylu. Jste svobodný? Máte rodinu? Rádi vám pomůžeme se rozhodnout, co je právě pro vás v pojištění důležité. Dlouhá nebo opakovaná pracovní neschopnost, vážná nemoc a následná invalidita, trvalé následky úrazu – to jsou věci, na které bychom v životním pojištění měli myslet především. Je důležité mít dobře pojištěny vážné situace, které mohou mít dlouhodobý dopad. Až poté je čas na pojištění drobnějších rizik. Životní pojištění myslí i na děti, kterým se neštěstí také nevyhýbají. Pojištění nemoci nebo úrazu pomůže, abyste se mohli soustředit především na uzdravení svého dítěte nebo mu mohli poskytnout lepší péči. Při náhlých zdravotních komplikacích nebo když se potřebujete vyznat ve složitém systému sociální pomoci, může být také užitečná zdravotní a sociální infolinka MAJÁK. Konzultační a asistenční služby MAJÁK+ vám navíc umožní konzultace s právníkem, podporu při psychických potížích a pomoc řemeslníků v domácnosti. Rádi vám poradíme s nastavením vašeho pojištění tak, aby vás dokázalo nejlépe ochránit."),
	("Poviné ručení","Pojištění odpovědnosti z provozu vozidla, též nesprávně povinné ručení, je povinné smluvní pojištění odpovědnosti, jehož základním účelem je pojistná ochrana zdraví a majetku třetích osob, kterým byla způsobena škoda zapříčiněná provozem vozidla. Podmínky sjednávání a plnění pojistné smlouvy v ČR upravuje zákon č. 168/1999 Sb., jenž mj. stanoví, že povinné ručení musí být uzavřeno pro každé vozidlo, které je provozováno na pozemní komunikaci včetně vozidel, která jsou pouze ponechána na pozemní komunikaci. Jako profesní organizaci pojistitelů, kteří jsou na území ČR oprávněni provozovat pojištění odpovědnosti z provozu vozidla, tento zákon zřizuje Českou kancelář pojistitelů. "),
	("Úrazové pojištění","Úrazové pojištění je druh pojištění, který zahrnuje výplatu pojistného plnění v případě, že v důsledku úrazu dojde k přechodnému tělesnému poškození, trvalému tělesnému poškození, či smrti pojištěného. Pojištění se může vztahovat na jednotlivce i skupinu osob. Výplata pojistného plnění po úrazu neprobíhá ihned, ale až po skončení šetření úrazu, což bývá obvykle do několika měsíců od úrazu. V případě trvalých následků se může jednat až o několik let, kdy se čeká například na výši trvalých následků, které pojistná událost způsobila. Úrazové pojištění má mezinárodní platnost."),
	("Důchodové pojištění","V oblasti důchodového pojištění má doba účasti na pojištění zásadní význam jednak proto, že jde vždy o jednu z podmínek nároku na důchod, a dále proto, že celková délka získané doby účasti na pojištění ovlivňuje výši procentní výměry důchodu.")
]