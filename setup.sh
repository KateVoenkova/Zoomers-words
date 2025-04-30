cp flask_app.nginx.conf /etc/nginx/sites-enabled/zoomers-words.nginx.conf
certbot --nginx -d zoomers-words.silaeder.codingprojects.ru
