#! /bin/sh

sudo cp boot/firmware/config.txt /boot/firmware/config.txt
sudo cp etc/dphys-swapfile /etc/dphys-swapfile

echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"
echo "Rebooting Now"
echo "@@@@@@@@@@@@@@@@@@@@@@@@@@"

sudo reboot