import os 

numero=inout("quel est le numero du site (00X) : ")
nom=input("quel est le nom du site : ")
os.system("toutch "+numero+nom +"etc/apache2/site-available")
site=open("etc/apache2/site-available/"+numero+nom)
site.write("""
<VirtualHost *:80>
	ServerName example.com
	ServerAlias www.example.com
	DocumentRoot "/var/www/example"
	<Directory "/var/www/example">
		Options +FollowSymLinks
		AllowOverride all
		Require all granted
	</Directory>
	ErrorLog /var/log/apache2/error.example.com.log
	CustomLog /var/log/apache2/access.example.com.log combined
</VirtualHost>
""")