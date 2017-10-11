## Required Python/Linux
```
sudo apt-get install python-pip python-dev python-setuptools
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install bluetooth libbluetooth-dev
sudo apt-get install python-pygame
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
sudo apt-get install pi-bluetooth
```
```
sudo pip install cryptography
sudo pip install mpu6050-raspberrypi
sudo pip install pybluez
sudo pip install requests
sudo pip install dataset
```

## Animation Ideas
* https://stackoverflow.com/questions/41101662/typewriter-effect-pygame



## Enable i2c `/etc/modules`
```
i2c-bcm2708
i2c-dev
```

## i2c Bus
```
i2cdetect -y 1 <-- check for i2c devices
```

Create `/etc/modules-load.d/i2c.conf`
```
i2c-dev
i2c-bcm2708
```

Edit `/boot/config.txt` uncomment the following:
```
dtparam=i2c_arm=on
dtparam=i2c1=on
```


# i2c Python
```python
import smbus
bus = smbus.SMBus(1)
address = 0x70

bus.write_byte_data(address, 0, value)
light = bus.read_byte_data(address, 1)

```

## Accelerometer
https://github.com/Tijndagamer/mpu6050
```python
from mpu6050 import mpu6050
sensor = mpu6050(0x68)
accelerometer_data = sensor.get_accel_data()
```
## SPI Support `/boot/config.txt`
dtparam=spi=on

## TFT Screen Support
Create `/etc/modules-load.d/fbtft.conf`
```
spi-bcm2835
fbtft_device
```
Create `/etc/modprobe.d/fbtft.conf`
```
options fbtft_device custom name=fb_ili9341 gpios=reset:25,dc:24,led:15 speed=48000000 rotate=270 bgr=1
```

### Enable bluetooth
Add the following line above the exit in `/etc/rc.local`
```
hciconfig hci0 piscan

exit 0
```

# Power Managment Option
## Power off TFT Screen
```
echo 1 | sudo tee /sys/class/backlight/sc_ili9341/bl_power <--- off
echo 0 | sudo tee /sys/class/backlight/sc_ili9341/bl_power <--- on
```

## Set Bluetooth to discoverable or non-discoverable
```
sudo hciconfig hci0 piscan <-- visible
sudo hciconfig hci0 noscan <-- hidden
```

## Turn WiFi on and off
```
sudo ifconfig wlan0 up
sudo ifconfig wlan0 down
```
