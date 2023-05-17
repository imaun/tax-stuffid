import xml.etree.ElementTree as ET
import sqlite3

db_name = 'stuff-ids.db'
db = sqlite3.connect(db_name)


def create_db():
	sql = """
		CREATE TABLE IF NOT EXISTS [Stuff] (
			[Id] TEXT NOT NULL PRIMARY KEY,
			[TypeName] TEXT NOT NULL,
			[ShamsiDate] TEXT,
			[IsGeneral] INTEGER NOT NULL Default(0),
			[Taxable] INTEGER NOT NULL DEFAULT(0),
			[Vat] INTEGER NOT NULL,
			[VatCustom] INTEGER,
			[Description] TEXT
		)
	"""
	db.cursor().execute(sql)
	db.commit()
	

def add_to_db(params):
	sql = """
		INSERT INTO [Stuff] 
			([Id], [TypeName], [ShamsiDate], [IsGeneral], [Taxable], [Vat], [VatCustom], [Description])
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)
	"""
	db.cursor().execute(sql, params)


def is_general(text)-> int:
	if text == 'عمومی':
		return 0
	return 1

def is_taxable(text)-> int:
	if text == 'مشمول':
		return 0
	return 1


create_db()

tree = ET.parse('StuffIDs.xml')
root = tree.getroot()

for item in root:
	id = item.find('ID').text
	print(id)
	type_name = item.find('Type').text
	print(type_name)
	shamsi_date = item.find('Date').text
	print(shamsi_date)
	special_general = is_general(item.find('SpecialOrGeneral').text)
	print(special_general)
	taxable_fee = is_taxable(item.find('TaxableOrFree').text)
	vat = item.find('Vat').text
	print(vat)
	vat_custom = item.find('VatCustomPurposes').text
	print(vat_custom)
	desc = item.find('DescriptionOfID').text
	print(desc)
	add_to_db([id, type_name, shamsi_date, special_general, taxable_fee, vat, vat_custom, desc])
	

db.commit()
print('completed press any key to exit...')
input()

exit()


	

	
