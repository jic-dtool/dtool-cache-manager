"""Module for dealing with dtool cache manager persistance."""
import datetime
import sqlite3

"""
>>> db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
>>> c = db.cursor()
>>> c.execute('create table foo (bar integer, baz timestamp)')
<sqlite3.Cursor object at 0x40fc50>
>>> c.execute('insert into foo values(?, ?)', (23, datetime.datetime.now()))
<sqlite3.Cursor object at 0x40fc50>
>>> c.execute('select * from foo')
<sqlite3.Cursor object at 0x40fc50>
>>> c.fetchall()
[(23, datetime.datetime(2009, 12, 1, 19, 31, 1, 40113))]
"""


class BackendManager(object):
    """Class for managing cache manager backend."""

    def __init__(self, fpath):
        self.conn = sqlite3.connect(
            fpath,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS dtcache
            (
              dataset_uuid     TEXT NOT NULL,
              item_id          TEXT NOT NULL,
              size_in_bytes     INTEGER  NOT NULL,
              last_access_time TIMESTAMP NOT NULL );
        ''')


    def add_new_entry(self, dataset_uuid, item_id, size_in_bytes):
        """Add a new entry to the backend."""
        now = datetime.datetime.utcnow()
        entry = (dataset_uuid, item_id, size_in_bytes, now)
        self.cur.execute(
            '''INSERT INTO dtcache VALUES (?,?,?,?);''',
            entry
        )

    def total_size_in_bytes(self):
        """Return the total size in bytes."""
        self.cur.execute('''
            SELECT SUM(size_in_bytes) FROM dtcache;
        ''')
        total = self.cur.fetchone()[0]
        if total is None:
            total = 0
        return total

    def total_number_of_entries(self):
        """Return the number of entires in the backend."""
        self.cur.execute('''
            SELECT COUNT(*) FROM dtcache;
        ''')
        count = self.cur.fetchone()[0]
        return count

    def delete_entry(self, dataset_uuid, item_id):
        """Delete an entry from the backend."""
        self.cur.execute('''
            DELETE FROM dtcache WHERE (dataset_uuid=? AND item_id=?)
        ''',
            (dataset_uuid, item_id)
        )
