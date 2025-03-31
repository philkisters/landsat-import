import os
import psycopg2
from datetime import datetime

DB_USER = 'ods_user'
DB_PASSWORD = 'ods_2023'
DB_HOST = 'postgis'
DB_PORT = '5432'
DB_NAME = 'ods'

SRID = '32632'
os.environ['PGPASSWORD'] = DB_PASSWORD

# def save_raster_data(source_name, raster_values, x_size, y_size, x_min, y_max, pixel_width, pixel_height, phenomenon_time):
def save_raster_data(source, raster_data, phenomenon_time, result_time = datetime.now()):
    
  
  conn = psycopg2.connect(
      dbname=DB_NAME,
      user=DB_USER,
      password=DB_PASSWORD,
      host=DB_HOST,
      port=DB_PORT
  )
  cursor = conn.cursor()
  
  insert_sql = """
      INSERT INTO raster_observations (source, rast, phenomenon_time, result_time)
      VALUES (%s, 
        %s,
        %s, 
        %s)
      RETURNING rid
      """
  values = (
      source,
      raster_data,
      phenomenon_time,
      result_time
  )
  
  cursor.execute(insert_sql, values)
  
  rid = cursor.fetchone()[0]
  
  conn.commit()
  cursor.close()
  conn.close()
  
  return rid