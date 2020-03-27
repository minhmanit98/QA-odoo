# Install the PostgreSQL database
sudo apt update
sudo apt install postgresql # Install PostgreSQL
sudo su -c "createuser -s $USER" postgres # Create db superuser

# Install the Odoo system dependencies
sudo apt update
sudo apt upgrade
sudo apt install git  # Install Git
sudo apt install python3-dev python3-pip # Python 3 for dev
sudo apt install build-essential libxslt-dev libzip-dev libldap2-dev libsasl2-dev libssl-dev

# Install less CSS preprocessor, needed until Odoo 11
sudo apt install npm  # Install NodeJs and its package manager
sudo ln -s /usr/bin/nodejs /usr/bin/node  # node runs nodejs
sudo npm install -g less less-plugin-clean-css  # Install less

# Install Odoo from source
mkdir ~/odoo  # Create a directory to work in
cd ~/odoo  # Go into our work directory
git clone https://github.com/odoo/odoo.git -b 13.0 --depth=1  # Get Odoo sources

pip3 install -r ~/odoo-dev/odoo/requirements.txt 
pip3 install num2words phonenumbers psycopg2-binary watchdog xlwt

