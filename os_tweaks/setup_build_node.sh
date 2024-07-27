#! /bin/sh

# config
INSTALLDIR="/var/local/office-data-collector"
SCRIPTPATH="$(pwd)"

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Starting Now"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

pushd

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Installing PreReqs"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"


sudo cp $SCRIPTPATH/boot/firmware/config.txt /boot/firmware/config.txt
sudo cp $SCRIPTPATH/etc/dphys-swapfile /etc/dphys-swapfile
sudo apt install python3-venv i2c-tools raspi-gpio python3-full -y

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Installing App"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

sudo mkdir $INSTALLDIR
sudo python3 -m venv $INSTALLDIR
sudo cp $SCRIPTPATH/../src/app/* $INSTALLDIR
cd $INSTALLDIR/bin/
/bin/sh activate
pip3 install -r $INSTALLDIR/requirements.txt


echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Rebooting Now"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

popd
#sudo reboots