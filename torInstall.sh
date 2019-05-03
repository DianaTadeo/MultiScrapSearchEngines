# Debian y Ubuntu
apt install apt-transport-https
# Ubuntu 16.04
echo "deb https://deb.torproject.org/torproject.org xenial main" >> /etc/apt/sources.list
echo "deb-src https://deb.torproject.org/torproject.org xenial main" >> /etc/apt/sources.list

# Debian stable (stretch)
echo "deb https://deb.torproject.org/torproject.org stretch main" >> /etc/apt/sources.list
echo "deb-src https://deb.torproject.org/torproject.org stretch main" >> /etc/apt/sources.list

curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -

apt update
apt install tor deb.torproject.org-keyring

# Se descomenta el puerto 9051 para Tor Controll
sudo sed -i '/#.*ControlPort 9051/s/^#//' /etc/tor/torrc
