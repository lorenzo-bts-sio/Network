import os 

def configuration(self):
	ip=input("# quel est l'ip du serveur nas ? : ")
	repertoire= input("# quel est le répertoire de la sauvegarde ? :")
	login=input("# quel est le login pour accéder au serveur ? :")
	password=input("# quel est le mot de passe ? :")

	os.system("mkdir /media/backup")
	os.system("toutch /root/.smblogin")
	smblogin=open('/root/.smblogin','a')
	smblogin.write("username="+login /n)
	smblogin.write("password="+password)
	smblogin.close()

	fstab=open("/etc/fstab",'a')
	fstab.write("//"+ip+"/"+repertoire+  "/media/backup cifs credentials=/root/.smblogin,iocharset=utf8,gid=0,uid=0,_netdev	0")
	fstab.close()
	print("le serveur nas est monter dans /media/backup")
	pass


def Backup_Intergrale(self):
	os.system("tar zcvf etc.tgz /etc/ | mv etc.tgz /media/backup")
	os.system("tar zcvf home.tgz /home/ | mv home.tgz /media/backup")
	pass
def Backup_Différencielle(self):
	os.system("rsync -e ssh -avz --delete-after /var/ uvar@192.168.16.207:/")
	pass