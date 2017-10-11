# Convert Badge into a RetroPie

## You will need:

* SaintCon 2017 Badge
* Keyboard
* Mini HDMI to HDMI

## Download RetroPie
Download Retropie from
[here](https://retropie.org.uk/download)

Badges are a Raspberry Pi 0, you will need to download that image.

[Download for Raspberry Pi 0,](https://github.com/RetroPie/RetroPie-Setup/releases/download/4.3/retropie-4.3-rpi1_zero.img.gz)

Should expect MD5sum: `6cfb11dbe3554581e10d3deb8559ed63`

## To get the screen working
Go to this link [Docs](https://learn.adafruit.com/running-opengl-based-games-and-emulators-on-adafruit-pitft-displays/pitft-setup)

### Change keyboard to US from UK
* Quit RetroPie by pressing: `F4`
* `sudo dpkg-reconfigure keyboard-configuration`
* `Generic 105-key (intl) PC`
* `other`
* `English (US)`
* (at the very top) `English (US)`
* `Default for the keyboard layout`
* `No compose key`
* Type: `sudo reboot`

## Wireless setup
* `sudo vi /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines at the end of wpa_supplicant.conf:

    network={
        ssid="{YOUR_SSID}"
        psk="{YOUR_PASSWORD}"
        proto=RSN
        key_mgnt=WPA-PSK
        pairwise=CCMP
        auth_alg=OPEN
    }

* Save: wpa_supplicant.conf
* Type: `sudo reboot`

## Get Screen Working
* `sudo raspi-config`

Select the following:

* `advanced options`
* `overscan`
* `NO`
* `Interfacing options`
* `SPI`
* `YES`
* `FINISH`
* `reboot`


* `sudo vi /etc/modules-load.d/fbtft.conf`
````
    spi-bcm2835
    fbtft_device
````
* save

* `sudo vi /etc/modprobe.d/fbtft.conf`

    options fbtft_device custom name=fb_ili9341 gpios=reset:25,dc:24,led:15 speed=48000000 rotate=270 bgr=1

* save
* `sudo reboot`

* `con2fbmap 1 1`

* `curl -O https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/pitft-fbcp.sh`
* `sudo bash pitft-fbcp.sh`

* y (YES)
* 3 (PiGRRL Zero)
* y (YES)

Downloads and installing Frame Buffer Copy

* (do you want to reboot now) y


## Get Gamepad working on Badge

At the RetroPie Home Screen
*  (Exit to terminal) press `F4`
* in a command line:

    curl -O https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/retrogame.sh;
    sudo bash retrogame.sh;


* pick 2 Pocket PiGRRRL
* (reboot) y

Edit Keys

* sudo vi /boot/retrogame/.cfg

* edit keys

     LEFT       4  # Joypad left
     RIGHT     19  # Joypad right
     UP        16  # Joypad up
     DOWN      26  # Joypad down
     A         14  # 'A' button
     B         15  # 'B' button
     ESC        5  # 'Select' button
     ENTER      6  # 'Start' button
     X         20  # 'X' button
     Y         23  # 'Y' button
     L         12  # Left shoulder button
     R         13  # Right shoulder button
* (save) `:wq`
* `sudo reboot`

* hold A

Match Keys

hold any key to skip
