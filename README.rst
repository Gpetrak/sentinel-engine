Sentinel-Engine
=============================

Sentinel-Engine created by **Senselab** within Crete-GIS project which received funding from the ** REGION OF CRETE's** research program: Crete-GIS. 

Sentinel Engine is a project that execute tasks like searching, downloading, processing or uploading data without supervising from the user.
It connects with Copernicus Open Acces Hub (https://scihub.copernicus.eu/dhus/) (an account is mandatory), searches every day for new datasets, downloads new datasets, processes them and finally (if the user has an up and rnning GeServer instance), uploads them on it.

The program has been tested in Ubuntu 16.04.

Installation
=============================

First we are going to install the software packages we are going to need for the Sentinel-Engine setup::
    
    sudo apt-get install python unzip python-pip

To install the program type::

    git clone https://github.com/Gpetrak/sentinel-engine.git
    cd sentinel-engine
    sudo pip install -e .

Run the program
=============================

To run the program sentinel_engine_24.py type::

    sudo python sentinel_engine_24.py <username> <password> <yes / no>
    # we type yes if we want our data to be uploaded in GeoServer

To run the program sentinel_engine_24.py in the background type::
   
    nohup sudo python sentinel_engine_24.py <username> <password> <yes / no> &

To run the program sentinel_engine_now.py type::

    sudo python sentinel_engine_now.py <username> <password> <yes / no> 

