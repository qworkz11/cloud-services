#!/bin/sh

echo "Configuring via post-install script:"

php occ db:add-missing-indices
php occ app:install calendar
php occ app:install contacts

echo "Post-install script done."