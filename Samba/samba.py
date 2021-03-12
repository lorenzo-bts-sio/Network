#-*- coding=utf8 -*-

import os 

os.system("apt-get update")
os.system("apt-get install acl")
os.system("apt-get install samba")


Création_User=input("voulez vous crée un utilisateur  ( oui / non) : ")
while Création_User != "non":
	
	Nom_User=input("entré  le nom de l'utilisateur crée : ")
	os.system("adduser "+Nom_User)
	os.system("smbpasswd -a "+Nom_User)
	print("l'utilisateur a bien etais crée sur sur la machine et dans samba ")
	Création_User=input("voulez vous crée un autre  utilisateur  ( oui / non) : ")
else:
	pass

Création_Groupe=input("voulez vous crée un groupe pour les machine ? (oui/non) : ")
if Création_Groupe =="oui":
	Groupe_Machine=input("entre le nom du groupe pour les machine : ")
	os.system("addgroup "+ Groupe_Machine)
else:
	pass

Création_Machine=input("voulez vous ajouter une machine :  ( oui / non) : ")
while Création_Machine != "non":
	Création_Machine=input("entré  le nom de la machine a ajouter : ")
	os.system( "useradd -d /dev/null -s /bin/false -g "+Groupe_Machine +" "+Création_Machine+"$")
	os.system("smbpasswd -a -m "+Création_Machine)
	print("la machine a bien etais ajouter dans samba ")
	Création_Machine=input("voulez vous ajouter une autre machine  ( oui / non) : ")
else:
	pass

domaine=input("entré le domaine a créé : ")
os.system("rm -r /etc/samba/smb.conf")
Smb_Conf=open("/etc/samba/smb.conf","a")
Smb_Conf.write("""
##############################
### Configuration générale ###
##############################

[global]

# workgroup = Nom du domaine NT (client/serveur).
# workgroup = Nom du groupe de travail (poste à poste).
    workgroup = """+domaine+"""
    netbios name = lgmX

# Description du serveur.
    server string = Serveur Samba

# Gestion des accents
    display charset = UTF-8
    unix charset = UTF-8
    dos charset = CP850

# Adresses IP des clients autorisés à se connecter sur Samba.
    ;hosts allow = 192.168.1. 192.168.2. 127.

# Chargement automatique de la liste des imprimantes.
    ;load printers = yes

# Emplacement du fichier "printcap".
    ;printcap name = /etc/printcap

# Pour utiliser le serveur d'impression "cups".
    ;printcap name = cups
    ;printing = cups

# Autoriser les accès anonymes. Dans l'exemple, l'utilisateur "nobody" sera
# le propriétaire des fichiers.
    guest account = nobody
    map to guest = bad user

# Emplacement des mots de passes Samba
    passdb backend = smbpasswd 
    passdb expand explicit = no

# Samba sépare les fichiers logs pour chaque ordinateur qui se connecte.
    log file = /var/log/samba/log.clients

# Taille maximum des fichiers log en Ko.
    max log size = 50

# Mode de sécurité. On utilise généralemnt "security = user".
    security = user

# Utilisation d'un serveur de mot de passe (uniquement si "security = server").
    ;password server = 192.168.1.50

# Cryptage des mots de passes.
    encrypt passwords = true

# Personnalisation du script de configuration de Samba.
# %m sera remplacé par le nom netbios de chaque machine connectée.
    ;include = /usr/local/samba/lib/smb.conf.%m

# Cette option améliore les performances.
    socket options = TCP_NODELAY 

# Permet à Samba d'être utilisable sur différents réseaux.
    ;interfaces = 192.168.12.2/24 192.168.13.2/24 

# Le serveur Samba est un controleur de domaine (PDC ou SDC)
    domain logons = yes

# Le serveur Samba est le controleur principal du domaine (PDC).
# Ne pas utiliser si un autre serveur de domaine est déja PDC du même domaine !
    domain master = yes 

# Pour interdire à Samba de participer à l'élection du serveur PDC.
    local master = yes

# Niveau de l'OS utilisé pour les élections (NT4 a le niveau 33).
    os level = 33

# Force une nouvelle élection à chaque démarrage du serveur Samba.
    preferred master = yes

# Cherche à lancer un script à chaque connexion d'un utilisateur.
# %m nom de l'ordinateur qui se connecte.
# %u nom de l'utilisateur qui se connecte.
# %I ip de l'ordinateur qui se connecte.
# %L nom du serveur.
# %g nom du groupe principal de l'utilisateur qui se connecte.
# %T date et heure de connexion.
# Ne pas oublier de decommenter le partage [netlogon].
    ;logon script = %u.bat

# Emplacement du profil itinérant pour les ordinateurs de la famille win9X.
    logon home =
    ;logon home = \\%L\%u\profile

# Emplacement du profil itinérant pour les ordinateurs des familles NT,2000,XP.
    ;map system = yes
    ;map hidden = yes
    ;map archive = yes
    logon path =
    ;logon path = \\%L\%u\profile

# Samba est un serveur wins
    ;wins support = yes

# Samba est un client wins. Attention Samba ne peut pas être à la fois un
# client et un serveur wins !
    ;wins server = w.x.y.z

# Samba essaye de résoudre les noms netbios par nslookups sur les DNS.
    dns proxy = no 

################
### Partages ###
################

############
# EXEMPLES #
############

# Partage minimaliste, utilisable avec les droits ACL.
#[minimal]
    ;path = /home/SAMBA/exemple
    ;browseable = yes
    ;writable = yes

# Partage privé, utilisable uniquement par fred, invisible dans
# les favoris réseau de Windows.
#[fredsdir]
    ;comment = Dossier de Fred
    ;path = /home/fred
    ;valid users = fred
    ;browseable = no
    ;writable = yes

# Partage qui varie en fonction de l'ordinateur qui se connecte.
#[pchome]
    ;path = /home/SAMBA/pc/%m
    ;writable = yes

# Partage accessible en lecture/écriture par mary et fred,
# accessible en lecture seule pour bryan et le groupe users.
#[maryandfredshare]
    ;path = /home/SAMBA/shared
    ;writable = yes
    ;create mode = 770
    ;directory mode = 770
    ;valid users = mary,fred,bryan,@users
    ;write list = mary,fred
    ;read list = mary,fred,bryan,@users

####################
# Fin des EXEMPLES #
####################

[homes]
    comment = Dossiers personnels
    browseable = no
    writable = yes

#[guest]
    :path = /var/samba/guest
    ;writable = yes
    ;create mode = 777
    ;directory mode = 777
    ;delete readonly = yes
    ;public = yes
    ;guest only = yes

#[netlogon]
    ;path = /var/samba/netlogon
    ;writable = yes
    ;browseable = no
    ;valid users = root,@users
    ;write list = root
    ;read list = @users
    ;create mode = 644
    ;directory mode = 755

#[printers]
    ;comment = All Printers
    ;path = /var/spool/cups
    ;browseable = no	
    ;public = yes
    ;guest ok = yes
    ;writable = no
    ;printable = yes

		
""")
Création_Partage=input("voulez crée un partage ? (oui/non)")
while Création_Partage =="oui":
	Chemin_Partage=input("enté le chemin du partage :")
	os.system("mkdir "+Chemin_Partage)
	Nom_Partage=input("entre  le nom du partage :")
	Users_Accès=input("quel utilisateur a accès au partage ? :")

	Smb_Conf.write("""
["""+Nom_Partage+"""]
path ="""+Chemin_Partage+""" 
read only = no
writeable = yes
valid users = """+Users_Accès
)
	Création_Partage=input("voulez vous faire un autre Partage ? (oui/non) :")

else:
	print("fin de programme")
	Smb_Conf.close()
Smb_Conf.close()