import sqlite3
import time
class Database(object):
  def __init__(self, filename='jonnyboards.db'):
    self.conn = sqlite3.connect(filename)
    self.CreateTables()

  def close(self):
    self.conn.close()

  def CreateTables(self):
    self.conn.execute('''CREATE TABLE IF NOT EXISTS sensor_events
             (timestamp INTEGER, sensor text, value INTEGER, count INTEGER,
              duration INTEGER, note TEXT, uploaded_on INTEGER)''')

  def StoreSensorData(self, sensor, value, count, duration, note):
    q = """
        INSERT INTO sensor_events(timestamp, sensor, value, count, duration, note)
        VALUES(?, ?, ?, ?, ?, ?)
        """
    cursor = self.conn.cursor()
    timestamp = int(time.time()*1000)
    cursor.execute(q, (timestamp, sensor, value, count, duration, note))
    self.conn.commit()

  def RetrieveNotUploadedRows(self):
    q = """
        SELECT rowid, * FROM sensor_events WHERE uploaded_on IS NULL
        """
    cursor = self.conn.cursor()
    cursor.execute(q)
    rows = cursor.fetchall()
    return rows

  def MarkRecordAsUploaded(self, record_id):
    timestamp = int(time.time()*1000)
    t = (timestamp, record_id)
    self.conn.execute("UPDATE sensor_events SET uploaded_on=? WHERE rowid=?", t)
    self.conn.commit()
\