import rasterio
import os
from rasterio.mask import mask
from pyproj import Transformer
from shapely.geometry import box, mapping

# We need a transformer to transform from EPSG:4326 (geografic) to EPSG:32632 (UTM zone 32N)
transformer_to_utm = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

def cutTIFF(foldername, filename):
    min_lon, min_lat, max_lon, max_lat = 9.7, 53, 10, 53.4

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

