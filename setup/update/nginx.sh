upstream odoo {
 server 127.0.0.1:8069;
}

upstream odoo-chat {
 server 127.0.0.1:8072;
}

server {
    server_name odoo.example.com;
    return 301 https://utc2forum2.eastus.cloudapp.azure.com$request_uri;
}

server {
   listen 443 ssl http2;
   server_name utc2forum2.eastus.cloudapp.azure.com;

   ssl_certificate /path/to/signed_cert_plus_intermediates;
   ssl_certificate_key /path/to/private_key;
   ssl_session_timeout 1d;
   ssl_session_cache shared:SSL:50m;
   ssl_session_tickets off;

   ssl_dhparam /path/to/dhparam.pem;

   ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
   ssl_ciphers 'ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS';
   ssl_prefer_server_ciphers on;

   add_header Strict-Transport-Security max-age=15768000;

   ssl_stapling on;
   ssl_stapling_verify on;
   ssl_trusted_certificate /path/to/root_CA_cert_plus_intermediates;
   resolver 8.8.8.8 8.8.4.4;

   access_log /var/log/nginx/odoo.access.log;
   error_log /var/log/nginx/odoo.error.log;

   proxy_read_timeout 720s;
   proxy_connect_timeout 720s;
   proxy_send_timeout 720s;
   proxy_set_header X-Forwarded-Host $host;
   proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
   proxy_set_header X-Forwarded-Proto $scheme;
   proxy_set_header X-Real-IP $remote_addr;

   location / {
     proxy_redirect off;
     proxy_pass http://odoo;
   }

   location /longpolling {
       proxy_pass http://odoo-chat;
   }

   location ~* /web/static/ {
       proxy_cache_valid 200 90m;
       proxy_buffering    on;
       expires 864000;
       proxy_pass http://odoo;
  }

  # gzip
  gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript;
  gzip on;
}



upstream odooserver {
     server 127.0.0.1:8069;
}

server {
     listen 80;
     server_name utc2forum2.eastus.cloudapp.azure.com;

     access_log /var/log/nginx/odoo_access.log;
     error_log /var/log/nginx/odoo_error.log;

     proxy_read_timeout 720s;
     proxy_connect_timeout 720s;
     proxy_send_timeout 720s;
     proxy_set_header X-Forwarded-Host $host;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
     proxy_set_header X-Real-IP $remote_addr;

     location / {
        proxy_redirect off;
        proxy_pass http://odooserver;
     }

     location ~* /web/static/ {
         proxy_cache_valid 200 90m;
         proxy_buffering on;
         expires 864000;
         proxy_pass http://odooserver;
     }

     gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript;
     gzip on;
 }

upstream odooserver {
     server 127.0.0.1:8069;
 }

 server {
     listen [::]:80;
     listen 80;

     server_name utc2forum2.eastus.cloudapp.azure.com www.utc2forum2.eastus.cloudapp.azure.com;

     return 301 https://utc2forum2.eastus.cloudapp.azure.com$request_uri;
 }

 server {
     listen [::]:443 ssl;
     listen 443 ssl;

     server_name www.utc2forum2.eastus.cloudapp.azure.com;

     ssl_certificate /etc/letsencrypt/live/domainname.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/domainname.com/privkey.pem;

     return 301 https://utc2forum2.eastus.cloudapp.azure.com$request_uri;
 }

 server {
     listen [::]:443 ssl http2;
     listen 443 ssl http2;

     server_name utc2forum2.eastus.cloudapp.azure.com;

     ssl_certificate /etc/letsencrypt/live/utc2forum2.eastus.cloudapp.azure.com/fullchain.pem;
     ssl_certificate_key /etc/letsencrypt/live/utc2forum2.eastus.cloudapp.azure.com/privkey.pem;

     access_log /var/log/nginx/odoo_access.log;
     error_log /var/log/nginx/odoo_error.log;

     proxy_read_timeout 720s;
     proxy_connect_timeout 720s;
     proxy_send_timeout 720s;
     proxy_set_header X-Forwarded-Host $host;
     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     proxy_set_header X-Forwarded-Proto $scheme;
     proxy_set_header X-Real-IP $remote_addr;

     location / {
        proxy_redirect off;
        proxy_pass http://odooserver;
     }

     location ~* /web/static/ {
         proxy_cache_valid 200 90m;
         proxy_buffering on;
         expires 864000;
         proxy_pass http://odooserver;
     }

     gzip_types text/css text/less text/plain text/xml application/xml application/json application/javascript;
     gzip on;
 }
