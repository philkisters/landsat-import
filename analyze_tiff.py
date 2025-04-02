import rasterio
import os
import subprocess
from datetime import datetime
from rasterio.mask import mask
from pyproj import Transformer
from shapely.geometry import box, mapping
from db import save_raster_data

# We need a transformer to transform from EPSG:4326 (geografic) to EPSG:32632 (UTM zone 32N)
transformer_to_utm = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

SRID = '32632'

def cut_tiff(foldername, filename):
  min_lon, min_lat, max_lon, max_lat = 9.66, 53.39, 10.37, 53.73

  min_x, min_y = transformer_to_utm.transform(min_lon, min_lat)
  max_x, max_y = transformer_to_utm.transform(max_lon, max_lat)

  bbox = box(min_x, min_y, max_x, max_y)

  with rasterio.open(os.path.join('./uploads', filename)) as src:
    out_meta = src.meta
    bounds = src.bounds
    
    print(f"UTM Bounding Box:     min_x={min_x}, min_y={min_y}, max_x={max_x}, max_y={max_y}")
    print(f"GeoTIFF Bounding Box: min_x={bounds.left}, min_y={bounds.bottom}, max_x={bounds.right}, max_y={bounds.top}")
    
    out_image, out_transform = mask(src, [mapping(bbox)], crop=True)

    out_meta.update({
      "driver": "GTiff",
      "height": out_image.shape[1],
      "width": out_image.shape[2],
      "transform": out_transform,
      "crs": src.crs
    })
    
    with rasterio.open(os.path.join(foldername, 'cut_' + filename), 'w', **out_meta) as dest:
      dest.write(out_image)

def store_tiff(foldername, filename):
  file = os.path.join(foldername, 'cut_' + filename)
  file_info = filename.split('_')
  
  if file_info[0] == "LC08":
    source_name = "NASA Landsat 8"
  elif file_info[0] == "LC09":
    source_name = "NASA Landsat 9"
  else:
    raise ValueError("Unbekannte Datenquelle im Dateinamen")

  phenomenon_time = datetime.strptime(file_info[3], "%Y%m%d")
  
  raster2pgsql_cmd = f"raster2pgsql -s 32632 -I -C -M {file} > temp.sql"
  
  # run raster2pgsql command
  try:
    print("Starting raster2pgsql subprocess")
    print(f"Running: {raster2pgsql_cmd}")
    raster2pgsql_process = subprocess.Popen(raster2pgsql_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (stdout, stderr) = raster2pgsql_process.communicate()
    
    if raster2pgsql_process.returncode == 0:
      print("TIF imported successfully.")
    else:
      print("Error while importing TIF to DB.")
      print(stderr.decode())
    
    with open('temp.sql', 'r') as file:
      lines = file.readlines()
      if len(lines) >= 3:
        third_line = lines[2].strip()
      else:
        raise ValueError("Something is wrong file has less the 3 lines.")

    # find binary raster data
    start_index = third_line.find("VALUES ('") + len("VALUES ('")
    end_index = third_line.find("'::raster")

    if start_index != -1 and end_index != -1:
      binary_raster = third_line[start_index:end_index]
    else:
      raise ValueError("Couldn't find raster data.")

    return save_raster_data(source=source_name, raster_data=binary_raster, phenomenon_time=phenomenon_time)

  except Exception as e:
    print(f"Error occurred: {e}")
    
  return