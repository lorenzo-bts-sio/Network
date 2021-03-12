import os 

os.system("apt-get update")
os.system("apt-get install pure-ftpd pure-ftpd-common")

Groupe=input("entrer le nom du groupe a crée : ")
os.system("groupadd "+Groupe)
os.system("useradd -g "+Groupe+" -d /dev/null -s /etc ftpuser")
os.system("cd /etc/pure-ftpd/auth/")
os.system("ln -s ../conf/PureDB 50puredb")
os.system("mv 50puredb /etc/pure-ftpd/auth")
Chemin=input("entrer le chemin du repertoire ftp :  ")
os.system("mkdir "+Chemin)

User=input("entre le nom de l'utilisateur : ")
Autre_User=input("voulez vous ajouter un autre utilisateur ? (oui/non) : ")
while Autre_User !="non":
	User=input("entrer le nom de l'utilisateur : ")
	Repertoire_User=os.system("mkdir "+Chemin+"/"+User)
	repertoire=Chemin+"/"+User
	os.system("chown -R ftpuser:"+Groupe +" "+ Chemin)
	os.system("pure-pw useradd "+User+"-u ftpuser -g "+Groupe+" -d "+repertoire)
	print("le repertoire de "+User +" a etais creér dans  : "+repertoire)
	Autre_User=input("voulez vous ajouter un autre utilisateur ? (oui/non) : ")

else:
	Repertoire_User=os.system("mkdir "+Chemin+"/"+User)
	repertoire=Chemin+"/"+User
	os.system("chown -R ftpuser:"+Groupe +" "+ Chemin)
	os.system("pure-pw useradd "+User+" -u ftpuser -g "+Groupe+" -d "+repertoire)


os.system("pure-pw mkdb")
os.system("/etc/init.d/pure-ftpd restart")


