# 3d-print-etc

3D printing HW and SW with ephasis to debugging and troubleshooting.

## Building the printer Anet8

[The big troubleshooting guide v2](https://gr33nonline.files.wordpress.com/2017/05/the-big-troubleshooting-guide.pdf)

__Board - HW__

* [ANET 3D Board v1.0](https://github.com/ralf-e/ANET-3D-Board-V1.0) - reverse engineered schematics
* [Sanguinololu/AVR1284p](https://reprap.org/wiki/Sanguinololu#Schematic_.26_Board_Images)

Google search `anet c43` (which is the number of capacitor/smoother for B_T ala bed termistor)

* https://www.thingiverse.com/groups/anet-a8-prusa-i3/forums/general/topic:17964
* https://www.reddit.com/r/3Dprinting/comments/6hoxei/troubleshooting_anet_a8_mobo/
* https://reprap.org/forum/read.php?406,758418
* https://3dfactory.cz/2018/04/09/chybna-teplota-podlozky/
* https://gr33nonline.files.wordpress.com/2017/05/the-big-troubleshooting-guide.pdf
* https://www.facebook.com/groups/1068531466501015/permalink/2116665988354219/?comment_id=2116717085015776&reply_comment_id=2116719315015553

## Marlin for Anet fun

* [marlinfw.org](https://marlinfw.org/) - the alternative firmware compatible with Anet 8 Mainboard
* [MarlinFirmware/Marlin](https://github.com/MarlinFirmware/Marlin)
* [MarlinFirmware/Configurations](https://github.com/MarlinFirmware/Configurations) in particular [config/examples/Anet/A8](https://github.com/MarlinFirmware/Configurations/tree/import-2.0.x/config/examples/Anet/A8)

> __Note:__ the files from `config/examples/Anet/A8` have to go into `<Marlin-folder>/Marlin` overwriting the existing ones. In order to quickly build them issue:

```bash
#!/bin/bash -x

pio run -e sanguino1284p "$@"
```

> __Note:__ you can use the [Visual studio code](https://code.visualstudio.com/) or [VSCodium](https://vscodium.com/) with plugins __PlatformIO IDE__ and eventually __Auto Build Marlin__. But I like the CLI which is neat and can be run even remotely.

### Patching firmware

When you decide to go non-stock or in other words

### Flashing firmware

The best and the most secure way is to use `usbasp` or its clone to write firmware via __J1__ connector which is SPI capable of ISP programming.

|USB ID   |Device
|---------|------
|1a86:7523| Anet A8 itself via USB cable
|16c0:05dc| Proper USBASP programmer

Optional but recomended, backup your firmware:

```bash
$AVRDUDE -c usbasp -p m1284p -P usb -U flash:r:$BACKUP -C $AVRDUDE_CONF
```

The flash the new firmware:

```bash
$AVRDUDE -v -p m1284p -C $AVRDUDE_CONF -c usbasp -U flash:w:$FW:i
```

the firmare file tends to be in `<Marlin-folder>/.pio/build/sanguino1284p/firmware.hex` folder.

```bash
AVRDUDE=$HOME/.platformio/packages/tool-avrdude/bin/avrdude
AVRDUDE_CONF=$HOME/.platformio/packages/tool-avrdude/avrdude.conf
BACKUP=$PWD/backup.hex
```

## The firmwares

* [Marlin](https://marlinfw.org/) - well known firmware
* [Repetier-Firmware](https://www.repetier.com/documentation/repetier-firmware/) - Reperier Host, Server and Firmware
* [RepRap Firmware](https://reprap.org/wiki/RepRap_Firmware) - the grand father of 3D printers
* [Smoothieware](http://smoothieware.org/howitworks) - own board, v1 and v2, both 32-bit
* [Teacup](https://www.reprap.org/wiki/Teacup_Firmware) - from the RepRap comunity
* [Klipper](https://www.klipper3d.org/) - combine power of host computer with the MCU (see [Step Benchmarks](https://www.klipper3d.org/Features.html#step-benchmarks))
* [Redeem](https://github.com/intelligent-agent/redeem) - BeagleBone (?black)

## The boards

[at Marlin](https://marlinfw.org/docs/hardware/boards.html)

[Best 5 @ all3dp.com](https://all3dp.com/2/5-fantastic-3d-printer-controller-boards/)

* Smoothieboard - Ethernet
* Panucatt Azteeg X5 GT - 32bit ARM
* Duet WiFi - TMC with WiFI, ATMEL SAM4E8E
* Revolve (preview) - 1 GHz CPU
* Panucatt Azteeg X3 Pro - 8 axis

### General CPUs

* AVR based
	* ATMega1284 - 124KB flash, 4K ram (Sanguinolu)
	* ATMega2560 - 256KB flash, 8K ram (Ramps)
* 32-bit ARM
	* Atmel SAM32
		* 
	* NXP LPC - Cortex M4
		* (Smoothieboard](http://smoothieware.org/smoothieboard)
	* STM32
		* Big Tree tech
		* [Rumba32](https://github.com/Aus3D/RUMBA32) and [Rumba32 @ RepRap](https://reprap.org/wiki/Rumba32)

### Big Tree tech

* [SKR Pro v1.1](https://github.com/bigtreetech/BIGTREETECH-SKR-PRO-V1.1)
* [SKR Mini E3](https://github.com/bigtreetech/BIGTREETECH-SKR-mini-E3)
* [BTT shop](http://www.bigtree-tech.com/shop)

They have many addons like displays, extension boards and even printer parts other then these boards (i.e.extruder).

## Refs

* [Solvespace](https://github.com/solvespace/solvespace) - 3D parametric modeling SW, last update 2016
* [Proterface Home](https://www.pronterface.com/) - tool for moving the printer around
* [Pronterface Github](https://github.com/kliment/Printrun) - clone and run

```bash
source virtualenv/bin/activate
pip install -r requirements.txt
```

