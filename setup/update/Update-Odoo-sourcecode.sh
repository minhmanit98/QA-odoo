# Update Odoo source code
sudo su odoo
cd ~/odoo-13
git tag --force 13-last-prod
git pull
# ~/odoo-12/odoo-bin -d odoo-stage --http-port=8080 -c /etc/odoo/odoo.conf  # optionally add: -u base 
exit
sudo service odoo restart  # or: sudo systemctl restart odoo

# Undo code update
sudo su odoo
cd ~/odoo-13
git checkout 13-last-prod
exit

# Upgrade production database
sudo service odoo stop
sudo su -c "~/odoo-13/odoo-bin -c /etc/odoo/odoo.conf -u qa_app --load-language=vi_VN --stop-after-init" odoo
sudo service odoo start

--load-language=vi_VN
ssh minhmanit98@52.168.25.103
sudo su -c "~/odoo-13/odoo-bin shell -d UTC2Forum -u all --stop-after-init" odoo
