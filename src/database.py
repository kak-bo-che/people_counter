import sqlite3
import time
class Database(object):
  def __init__(self):
    self.conn = sqlite3.connect('jonnyboards.db')
    self.CreateTables()

  def CreateTables(self):
    self.conn.execute('''CREATE TABLE IF NOT EXISTS sensor_events
             (timestamp INTEGER, sensor text, value INTEGER, note TEXT, uploaded INTEGER DEFAULT 0)''')

  def StoreSensorData(self, sensor, value, note):
    q = """
        INSERT INTO sensor_events(timestamp, sensor, value, note)
        VALUES(?, ?, ?, ?)
        """
    cursor = conn.cursor()
    timestamp = int(time.time())
    cursor.execute(q, (timestamp, sensor, value, note))
    self.conn.commit()

  def RetrieveNotUploadedRows(self):
    q = """
        SELECT * FROM sensor_events WHERE uploaded = 0
        """
    cursor = conn.cursor()
    cursor.execute(q)
    rows = cursor.fetchall()
    return rows

  def MarkRecordAsUploaded(self, record_id):
    t = (record_id, )
    self.conn.execute("UPDATE sensor_events SET uploaded=1 WHERE id=?", t)
    self.conn.commit()
