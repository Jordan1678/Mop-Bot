# Mop-Bot
A Robot that Mops the robotics class

## Seting up your Raspberry Pi

This should work on all Pi's
This also assumes you have python already installed
which I hope you do its preloaded on Pi's


This command will install a load of packages to help with image processing

```
sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5 python3-dev
```

Something python needs to use the camera modul 

```
pip install "picamera[array]"
```

Install an older version of opencv that is compatible with the raspberry pi


```
sudo apt-get install python3-opencv
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
 ```

