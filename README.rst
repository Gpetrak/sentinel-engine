Sentinel-Engine
=============================

Sentinel-Engine was created by **Senselab** within Crete-GIS project which received funding from the **REGION OF CRETE's** research program: Crete-GIS. 

Sentinel Engine is a project that execute tasks like searching, downloading, processing and uploading Sentinel data in GeoServer, without supervising from the user. The geographic area which is covered is the region of Crete.
It is connected with Copernicus Open Access Hub (https://scihub.copernicus.eu/dhus/) (it is mandatory to have an account), searches every day for new datasets, downloads new datasets, processes them and finally (if the user has an up and running GeoServer instance), uploads them on it.

The program developed and tested in Ubuntu 16.04.

Installation
=============================

First we are going to install the software packages we are going to need for the Sentinel-Engine setup::
    
    sudo apt-get install python unzip python-pip

To install the program type::

    git clone https://github.com/Gpetrak/sentinel-engine.git
    cd sentinel-engine
    sudo pip22 install -e .

Run the program
=============================

To run the program sentinel_engine_24.py type::

    cd sentinel_engine
    sudo python sentinel_engine_24.py <username> <password> <yes / no> <workspace>
    # we type yes if we want our data to be uploaded in GeoServer

To run the program sentinel_engine_24.py in the background type::
   
    nohup sudo python sentinel_engine_24.py <username> <password> <yes / no> <workspace> &

To test Sentinel-Engine run sentinel_engine_test.py type::

    sudo python sentinel_engine_test.py <username> <password> <yes / no> <workspace>

