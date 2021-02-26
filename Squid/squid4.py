import os 

def Installation():
	os.system("clear")
	os.system("cd")
	os.system("apt update && apt install -y squid  apache2-utils ")
	os.system("rm -r /etc/squid/squid.conf")
	os.system("touch /etc/squid/Block_Domaine.txt")
	os.system("touch /etc/squid/utilisateurs")
	os.system("touch /etc/squid/squid.conf")
	Configuration()



def Configuration():
	os.system("service squid stop")
	nom=input("quel est le nom du serveur proxy : ")
	ip=input("quel est l'ip du serveur proxy  : ")
	port=input("quel est le port du serveur proxy : ")
	réseau=input("quel est le réseau sur le quel le proxy doit etre actif : ")
	masque=input("quel est son masque  en  CIDR ( 8,16,24 ...) : ")

	Squid_Conf=open("/etc/squid/squid.conf","a")
	Squid_Conf.write("""

# Squid a besoin de savoir le nom de la machine, notre machine s’appelle """+nom+""", donc :
visible_hostname """+nom+"""

# Par défaut le proxy écoute sur ses deux interfaces, pour des soucis de sécurité il faut donc le
# restreindre à écouter sur l’interface du réseau local (LAN)
http_port """+ip+""":"""+port+"""

# Changer la taille du cache de squid, changer la valeur 100 par ce que vous voulez (valeur en Mo)
cache_dir ufs /var/spool/squid 100 16 256

#################################### AUTH_PROGRAMES ##############################################

auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/utilisateurs # On déclare le programme qui gère l'authentification 
auth_param basic children 10
auth_param basic realm connectez-vous au serveur proxy
auth_param basic credentialsttl 2 hours
auth_param basic casesensitive off 

#################################### ACL ####################################

#acl all src all # ACL pour autoriser/refuser tous les réseaux (Source = All) – ACL obligatoire
acl lan src """+réseau+"""/"""+masque+""" # ACL pour autoriser/refuser le réseau 172.16.0.0
acl Safe_ports port 80 # Port HTTP = Port 'sure'
acl Safe_ports port 443 # Port HTTPS = Port 'sure'
acl Safe_ports port 21 # Port FTP = Port 'sure'
acl Block_Domaine url_regex -i "/etc/squid/Block_Domaine.txt" # Déclarer un fichier qui contient les domaines à bloquer
acl utilisateurs proxy_auth REQUIRED # Grâce à cette ACL, le Proxy demandera une authentification

#################################### HTTP_ACCESS ##############################################

# Désactiver tous les protocoles sauf les ports sures
http_access deny !Safe_ports

# Désactiver l'accès pour tous les réseaux sauf les clients de l'ACL Lan
# deny = refuser ; ! = sauf ; lan = nom de l’ACL à laquelle on fait référence.
http_access deny !lan

# Port utilisé par le Proxy :
# Le port indiqué ici, devra être celui qui est précisé dans votre navigateur.
http_port """+port+"""

# Refuser les domaines déclarés dans le fichier définit dans l'ACL deny_domain
http_access deny Block_Domaine

# Refuse tout le monde sauf les personnes de la liste des utilisateurs 
http_access deny !utilisateurs 

###############################################################################################

""")
	Squid_Conf.close()
	os.system("service squid start")
	Menu()

def Block_Domaine():
	Domaine=open("/etc/squid/Block_Domaine.txt","a")
	block=input("quel domaines vous voulez bloquer : ")
	Domaine.write( "\n {}").format(block)


def Ajout_Utilisateur():
	
	utilisateur=input("entrer le nom de l'utilisateur :")
	mdp=input("entrer le mot de passe de l'utilisateur :")
	os.system("htpasswd -b /etc/squid/utilisateurs {} {} ".format(utilisateur,mdp))
	os.system("service squid reload ")
	Menu()

def Fin_Programme():
	print("bye")
	os.system("exit")

def Menu():
	os.system("clear")
	print("""

	# # # # # # # # # # # # # # # # # # # # # # # # # #
	#      Programme Création De Proxy (Squid)        #
	#                     &                           #
	#      Création de certificat ssl auto signé      #
	#                                                 #
	#                              By:Oznerol         #
	# # # # # # # # # # # # # # # # # # # # # # # # # #
	#                                                 #
	#  Bienvenue sur le Programme de création de FTP  #
	#  via Pure-Ftpd et de création de certificat     #
	#  ssl via openssl                                #
	#                                                 #
	#                                                 #
	#-------------------------------------------------#
	#                                                 #
	#  Veuillez choisir dans les options ci dessous   #
	#  en entrant son numéro (exemple 1 , 2 etc )     #
	#                                                 #
	#-------------------------------------------------#
	#  1) Installation                                #
	#  2) Configuration du Proxy                      #
	#  3) Création d'utilisateur                      #
	#  4) Bloquage d'un domaine                       # 
	#  5) Création du certificat ssl                  #
	#  6)                                             #
	#  7) Fin de Programme                            #
	#                                                 #
	# # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	Numéro=input("Veuillez entrer le numéro de l'option : ")
	if Numéro=="1":
		Installation()
	elif Numéro=="2":
		Configuration()
	elif Numéro=="3" :
		Ajout_Utilisateur()
	elif Numéro=="4" :
		Block_Domaine()
	elif Numéro=="5":
		Openssl()
	elif Numéro=="7":
		Fin_Programme()
	else:
		Menu()
Menu()
