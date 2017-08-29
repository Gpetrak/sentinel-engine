# -*- coding: utf-8 -*-
# Copyright (C) 2017 George Petrakis <gkpetrak@gmail.com> 
#######################################################################   
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
########################################################################

# connect to the API
from sentinelsat.sentinel import SentinelAPI, get_coordinates
from datetime import date
import zipfile
import os
import sys
import schedule
import time

# To execute the program type sudo python file.py <user> <password> yes/no
# To execute the program in background type:nohup sudo python file.py <user> <password> yes/no &

# This is the path
f_path = os.path.abspath('')

api = SentinelAPI(sys.argv[1], sys.argv[2], 'https://scihub.copernicus.eu/dhus')

file_path = os.path.abspath('')
product_files = []
global hasRun 
global gdal_vrt_cmd
global gdal_trans_cmd
global gdal_jp2_to_tif_cmd
global gdal_culc_cmd
global gdal_ndvi_8bit_cmd
# gdal_merge.py command that creates an infrared composite
gdal_vrt_cmd = "gdalbuildvrt -separate -o"
gdal_trans_cmd = "gdal_translate -ot Byte -scale 0 4096 0 255 -b 1 -b 2 -b 3"
gdal_jp2_to_tif_cmd = "gdal_translate -of 'Gtiff'"
gdal_culc_cmd = ' --outfile=ndvi.tif --type="Float32"' + \
                ' --calc="(B.astype(float)-A.astype(float))/(B.astype(float)+A.astype(float))" --overwrite'
gdal_ndvi_8bit_cmd = "gdal_translate -ot Byte -scale -1 1 0 255"
hasRun = False

# search by polygon, time, and SciHub query keywords
def search():
    current_date = (time.strftime("%Y%m%d"))
    api.query(get_coordinates('polygon_crete.geojson'), \
          current_date, current_date, \
          platformname = 'Sentinel-2', \
          producttype='S2MSI1C', \
          cloudcoverpercentage = '[0 TO 30]')
   
    api.download_all()
    hasRun = True         
    if (hasRun == True): 
        if (len(api.products) != 0):
            processing(api.products)
        else:
            print "There is not new products"
    else:
        print "Downloading failed... :-( "
        return 0

# it executes processes of Sentinel-2 data
def processing(products): 
    # product_list will contain the processed products
    product_list = []
    for i in range(len(products)):
        unzip(products[i]["title"])
        # output variables
        output_infra = products[i]["title"].encode("utf-8") + "_infrared.vrt"
        output_infra_8bit = products[i]["title"].encode("utf-8") + "_infrared_8bit.tif"
        output_natural = products[i]["title"].encode("utf-8") + "_natural.vrt"
        output_natural_8bit = products[i]["title"].encode("utf-8") + "_natural_8bit.tif"
        output_nir_band_tiff = products[i]["title"].encode("utf-8") + "_nir.tif"
        output_red_band_tiff = products[i]["title"].encode("utf-8") + "_red.tif"
        output_ndvi = products[i]["title"].encode("utf-8") + "_ndvi.tif"
        output_ndvi_8bit = products[i]["title"].encode("utf-8") + "_8bit_ndvi.tif"
        
        # call the function band_list in order to return a list of bands (.jp2 format)
        bands_jp2 = band_list(f_path + "/unzip_files/" + products[i]["title"].encode("utf-8") + ".SAFE")
       
        # create infrared composite by merging 8, 4 and 3 bands of sentinel-2
        os.system(gdal_vrt_cmd + " %s %s %s %s" % (output_infra, bands_jp2[8], bands_jp2[4], bands_jp2[3]))
        os.system(gdal_trans_cmd + " %s %s" % (output_infra, output_infra_8bit))
        product_list.append(output_infra_8bit)
       
        # create natural composite by merging 4, 3 and 2 bands of sentinel-2
        os.system(gdal_vrt_cmd + " %s %s %s %s" % (output_natural, bands_jp2[4], bands_jp2[3], bands_jp2[2]))
        os.system(gdal_trans_cmd + " %s %s" % (output_natural, output_natural_8bit))
        product_list.append(output_natural_8bit)
       
        # create NDVI index 
        os.system(gdal_jp2_to_tif_cmd + "  %s %s" % (bands_jp2[8], output_nir_band_tiff))
        os.system(gdal_jp2_to_tif_cmd + "  %s %s" % (bands_jp2[4], output_red_band_tiff))  
        os.system('gdal_calc.py -A %s -B %s ' % (output_red_band_tiff, output_nir_band_tiff) + gdal_culc_cmd)
        os.system(gdal_ndvi_8bit_cmd + " ndvi.tif " + output_ndvi_8bit)
        product_list.append(output_ndvi_8bit)
        print product_list
    
    if sys.argv[3] == "yes":
        geoserver_upload(product_list)
    return product_list

# uploads to GeoServer the products
def geoserver_upload(products):
    for i in range(len(products)):
        print products[i]
        path = " http://localhost:8080/geoserver/rest/workspaces/geonode/coveragestores/"    \
               + products[i].replace(".tif","") + "/file.geotiff"
        create_cover_cmd = "curl -u admin:geoserver -v -XPOST -H 'Content-type: application/xml' -d '<coverageStore><name>"    \
                           + products[i].replace(".tif","") +    \
                           "</name><workspace>geonode</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:data/geonode/"    \
                           + products[i] + "</url></coverageStore>' http://localhost:8080/geoserver/rest/workspaces/geonode/coveragestores"
        upload_cover_cmd = "curl -u admin:geoserver -v -XPUT -H 'Content-type: image/tiff' --data-binary @"
      #  print create_cover_cmd
      #  print (upload_cover_cmd + products[i] + path)
        os.system(create_cover_cmd)
        os.system(upload_cover_cmd + products[i] + path)
    os.system("python /home/geonode/crete-gis/manage.py updatelayers")
   # remove_needless_files(products)

# Future function that will remove needless zip, vrt and tif files
'''
def remove_needless_files(files):
    for i in range(len(files)):
        os.remove(files[i])
        files.remove(i) 

    products = search()
    for j in range(len(products)):
        os.remove(products[j]["title"] + ".zip")
        products.remove(j) 
    # check if the list files and products are empty
    # if they are empty, it removes the folder unzip_files 
    if not (files and products):   
        os.rmdir("unzip_files") '''
 
# unzip the downloaded products and stores them in unzip_files folder
def unzip(f):
    zip_ref = zipfile.ZipFile(f + ".zip", 'r') 
    zip_ref.extractall(f_path + "/unzip_files")
    zip_ref.close()

# finds files with jp2 format and stores them in bands list
def band_list(band_path):
    bands = []
    for dirpath,subdirs, files in os.walk(band_path):
        for i in sorted(files):
            if i.endswith(".jp2"):
                bands.append(os.path.join(dirpath, i))
    return bands
    
# search for new data in sentinel archive every day at 20:00
# if it finds something call the processing function

schedule.every().day.at("20:00").do(search)

while True:
    schedule.run_pending()
    time.sleep(1)   


# GeoJSON FeatureCollection containing footprints and metadata of the scenes
api.get_footprints()
