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
        INSERT OR REPLACE INTO [Stuff] 
            ([Id], [TypeName], [ShamsiDate], [IsGeneral], [Taxable], [Vat], [VatCustom], [Description])
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    db.cursor().execute(sql, params)


def is_general(text) -> int:
    if text == 'عمومی':
        return 0
    return 1


def is_taxable(text) -> int:
    if text == 'مشمول':
        return 0
    return 1


def record_exists(id):
    query = "SELECT COUNT(*) FROM Stuff WHERE Id = ?"
    result = db.cursor().execute(query, (id,)).fetchone()
    return result[0] > 0


create_db()

tree = ET.parse('StuffIDs.xml')
root = tree.getroot()

for item in root:
    id = item.find('ID').text
    type_name = item.find('Type').text
    shamsi_date = item.find('Date').text
    special_general = is_general(item.find('SpecialOrGeneral').text)
    taxable_fee = is_taxable(item.find('TaxableOrFree').text)
    vat = item.find('Vat').text
    vat_custom = item.find('VatCustomPurposes').text
    desc = item.find('DescriptionOfID').text

    if record_exists(id):
        # اگر رکورد با این Id وجود داشته باشد، بروزرسانی انجام شود
        update_query = """
            UPDATE [Stuff] SET 
                [TypeName] = ?,
                [ShamsiDate] = ?,
                [IsGeneral] = ?,
                [Taxable] = ?,
                [Vat] = ?,
                [VatCustom] = ?,
                [Description] = ?
            WHERE [Id] = ?
        """
        db.cursor().execute(update_query, (type_name, shamsi_date, special_general, taxable_fee, vat, vat_custom, desc, id))
    else:
        # اگر رکورد با این Id وجود نداشته باشد، افزودن رکورد جدید
        add_to_db([id, type_name, shamsi_date, special_general, taxable_fee, vat, vat_custom, desc])

db.commit()
print('completed press any key to exit...')
input()
exit()
