from . import CONN, CURSOR

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        """Create the dogs table."""
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the dogs table."""
        sql = "DROP TABLE IF EXISTS dogs;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new dog or update existing dog."""
        if self.id is None:
            sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
        else:
            self.update()
        return self

    @classmethod
    def create(cls, name, breed):
        """Create a new dog instance + DB row."""
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        """Convert database row into Dog instance."""
        return cls(id=row[0], name=row[1], breed=row[2])

    @classmethod
    def get_all(cls):
        """Return all records as Dog instances."""
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        """Find dog by name and return Dog instance."""
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, id):
        """Find dog by ID."""
        sql = "SELECT * FROM dogs WHERE id = ? LIMIT 1"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        """Return existing dog or create new one."""
        sql = """
        SELECT * FROM dogs
        WHERE name = ? AND breed = ? LIMIT 1
        """
        row = CURSOR.execute(sql, (name, breed)).fetchone()

        if row:
            return cls.new_from_db(row)
        else:
            return cls.create(name, breed)

    def update(self):
        """Update existing dog record."""
        sql = """
        UPDATE dogs
        SET name = ?, breed = ?
        WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()
