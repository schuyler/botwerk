Notes on installing from scratch:

```
sudo apt-get update
sudo apt-get install git build-essential gfortran libhdf5-dev libopenblas-dev liblapack-dev python-dev zip
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py 
sudo pip install virtualenv
git clone http://github.com/schuyler/botwerk
cd botwerk
virtualenv .
. bin/activate
pip install -r requirements.txt 
```