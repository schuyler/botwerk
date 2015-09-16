sudo apt-get install git build-essential gfortran hdf5 libblas-dev liblapack-dev
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py 
sudo pip install virtualenv
git clone git@tridity.org:botsnpieces.git
cd botsnpieces
virtualenv .
. bin/activate
pip install -r requirements.txt 
