#!/bin/sh

# Install the prerequisites (if not already included in the base image)
apt update && apt install -y curl gnupg2 ca-certificates lsb-release debian-archive-keyring

# Import an official nginx signing key so apt could verify the packages authenticity.
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    > /usr/share/keyrings/nginx-archive-keyring.gpg

# Verify that the downloaded file contains the proper key
gpg --dry-run --quiet --no-keyring --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
# The output should contain the full fingerprint 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62

# Set up the apt repository for stable nginx packages
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
http://nginx.org/packages/debian `lsb_release -cs` nginx" \
    > /etc/apt/sources.list.d/nginx.list

# Set up repository pinning to prefer our packages over distribution-provided ones
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
    > /etc/apt/preferences.d/99nginx

# Update the package lists
apt update

# Install nginx
apt install -y nginx

# Clean up to reduce the image size
apt clean && rm -rf /var/lib/apt/lists/*
