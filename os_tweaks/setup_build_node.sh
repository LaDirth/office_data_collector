#! /bin/sh

# config
INSTALLDIR="/var/local/office-data-collector"


echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Starting Now"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

sudo -i
pushd

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Installing PreReqs"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"


cp boot/firmware/config.txt /boot/firmware/config.txt
cp etc/dphys-swapfile /etc/dphys-swapfile
apt install python3-venv i2c-tools raspi-gpio python3-full

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Installing App"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

mkdir $INSTALLDIR
python3 -m venv $INSTALLDIR
cp ../src/app/* $INSTALLDIR
/bin/sh $INSTALLDIR/bin/activate
pip3 install -r $INSTALLDIR/requirements.txt


echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Rebooting Now"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

sudo reboot