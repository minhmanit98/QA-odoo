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
sudo su -c "~/odoo-13/odoo-bin -c /etc/odoo/odoo.conf -u qa_app,qld_app --load-language=vi_VN --stop-after-init" odoo
sudo su -c "~/odoo-13/odoo-bin -c /etc/odoo/odoo.conf -u website --load-language=vi_VN --stop-after-init" odoo

sudo service odoo start
website
sudo nginx -t
sudo service nginx restart

sudo rm /etc/nginx/sites-enabled/odoo.conf
sudo rm /etc/nginx/sites-available/odoo.conf
sudo nano /etc/nginx/sites-enabled/odoo.conf
sudo ln -s /etc/nginx/sites-enabled/odoo.conf /etc/nginx/sites-available/odoo.conf

sudo nano /etc/nginx/sites-enabled/minhmanit.me
sudo ln -s /etc/nginx/sites-enabled/minhmanit.me /etc/nginx/sites-available/minhmanit.me

sudo nano /etc/nginx/sites-enabled/utc2support.team
sudo ln -s /etc/nginx/sites-enabled/utc2support.team /etc/nginx/sites-available/utc2support.team

--load-language=vi_VN
ssh minhmanit98@52.168.25.103
sudo su -c "~/odoo-13/odoo-bin shell -d UTC2Forum -u all --stop-after-init" odoo

sudo su -c "~/odoo-13/odoo-bin -d jhkjk" odoo
sudo su -c "~/odoo-13/odoo-bin -d UTC2Forum" odoo
sudo su -c "~/odoo-13/odoo-bin" odoo
jhkjk
 $('#dongbodiem').trigger('click');
function autoclick(){
 
}

$(document).ready(function(){

setInterval(function(){
          $("button[name='utc2_sync_score']").trigger('click');
          }, 170000);

});


setTimeout(function(){
 
console.log("tee");
}, 100);

setInterval(function(){
           console.log("tee");
          }, 1000);

jhkjk
sudo su -c "~/odoo-13/odoo-bin -c /etc/odoo/odoo.conf" odoo
