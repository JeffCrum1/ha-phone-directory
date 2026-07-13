#!/bin/bash
set -e

rsync -av --inplace --delete \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude 'contacts.json' \
  /opt/git/homeassistant-custom/custom_components/phone_directory/ \
  /mnt/components/phone_directory/

echo "phone_directory deployed"