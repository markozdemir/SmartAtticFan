#!/bin/bash

echo "DELETING FLASH"
esptool.py --port /dev/tty.usbserial-021FE2F5 erase_flash

echo "FLASHBANG!"
esptool.py --chip esp32 --port /dev/tty.usbserial-021FE2F5 --baud 460800 write_flash --flash_size=2MB 0 esp32-idf3-20210202-v1.14.bin
