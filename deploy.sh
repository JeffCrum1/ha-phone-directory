#!/bin/bash
set -e

rsync -av --delete \
/opt/git/homeassistant-custom/custom_components/phone_directory/ \
/mnt/components/phone_directory/

echo "phone_directory deployed"
