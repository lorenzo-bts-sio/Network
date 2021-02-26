import os 
	
def Installation():
	os.system("clear")
	print("Installation en cours : ...")
	os.system("apt-get install -y  pure-ftpd pure-ftpd-common")
	
	a=os.path.isdir('/etc/pure-ftpd')
	b=os.path.isdir('/etc/ssl/private')


	if a  !=True:
		print("Installation de pure-ftpd : \033[31;1m Echec  \033[0m ")
	else:
	 	print("Installation de pure-ftpd : \033[32;1m Succés  \033[0m ")
	if b  !=True:
		print("Installation de pure-ftpd : \033[31;1m Echec  \033[0m ")
	else:
	 	print("Installation de oppenssl : \033[32;1m Succés  \033[0m ")
	Retour_Menu=input("Appuyer sur une touche pour retourner au menu principal : ")
	if Retour_Menu!="}":
		Menu()
	else:
		Menu()

	
def Configuration():
	os.system("clear")
	print("""
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#  Bienvenue dans la configuration du serveur ftp   #
#  un nom de groupe ainsi qu'un chemin racine vont  #
#  vous etre demandé pour facilité la gestion dans  # 
#  le repertoire racine ce trouvera les dosiers des #
#  utilisateurs que vous créé plus tard             # 
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	Groupe=input("Entrer le nom du groupe a crée pour le ftp : ")
	os.system("groupadd "+Groupe)
	os.system("useradd -g "+Groupe+" -d /dev/null -s /etc ftpuser")
	os.system("cd /etc/pure-ftpd/auth/")
	os.system("ln -s ../conf/PureDB 50puredb")
	os.system("mv 50puredb /etc/pure-ftpd/auth")
	Chemin=input("entrer le chemin du repertoire ftp :  ")
	os.system("mkdir "+Chemin)
	Création_Utilisateur(Groupe,Chemin)
	return Groupe,Chemin 


def Création_Utilisateur(Groupe,Chemin):
	print("""
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#  Bienvenue dans la création d'utilisateur         #
#  du serveur ftp dans cette partie vous pouvez     #
#  crée un utilisateur a la fois néanmoins          #
#  a la fin une demande de création d'un autre      #
#  utilisateur vous seras faite si vous accepter    #
#  ce script sera relancer sinon vous retourner     #
#  au menu principale              				    # 
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	print("le chemin est : {} et le groupe : {}".format(Chemin,Groupe))
	
	User=input("Entre le nom de l'utilisateur : ")
	Repertoire_User=os.system("mkdir "+Chemin+"/"+User)
	repertoire=Chemin+"/"+User
	os.system("chown -R ftpuser:"+Groupe +" "+ Chemin)
	os.system("service pure-ftpd stop ") 
	os.system("pure-pw useradd "+User+" -u ftpuser -g "+Groupe+" -d "+repertoire+" -m")
	print("Le repertoire de "+User +" a etais creér dans  : "+repertoire)
	Autre_Utilisateur=input("Voulez vous creér un autre utilisateur (o/n) : ")

	if Autre_Utilisateur !="o":
		Menu()
	else:
		Création_Utilisateur(Groupe,Chemin)


def Openssl():
	
	os.system("echo 2 > /etc/pure-ftpd/conf/TLS")
	os.system("mkdir -p /etc/ssl/private/pure-ftpd")
	os.system("openssl req -x509 -nodes -days 7300 -newkey rsa:2048 -keyout /etc/ssl/private/pure-ftpd.pem -out /etc/ssl/private/pure-ftpd.pem")
	os.system("chmod 600 /etc/ssl/private/pure-ftpd.pem")
	os.system("/etc/init.d/pure-ftpd restart")

	Retour_Menu=input("Appuyer sur une touche pour retourner au menu principal : ")
	if Retour_Menu!="}":
		Menu()
	else:
		Menu()


def Suppression(chemin):
	chemin="/var/ftp"
	os.system("clear")
	print("""
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#  Bienvenue dans la suppression de compte du       #
#  serveur ftp le nom d'utilisateur a supprimer     #
#  vas vous etre demander ainsi que le choix        #
#  de garder ou non le contenue du compte           #  
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	utilisateur=input("entrer le nom de l'utilisateur a supprimer : ")
	sécurité=input("etes vous sur de vouloir supprimer {} (y/n) : ".format(utilisateur))
	if sécurité !="y":
		print("abandon de suppression du compte {}".format(utilisateur))
	else:
		contenue=input("voulez vous supprimer également le contenue du compte {} (y/n)".format(utilisateur))
		if contenue !="y":
			print("abandon suppression du contenue du compte {}".format(utilisateur))
			Menu()
		else:
			chemin=input("le compte se trouve bien dans {}/{} (y/n) ? :".format(chemin,utilisateur))
			if chemin == "n":
				new_chemin=input("quel est le chemin du repertoire du compte {} : ".format(utilisateur))
				print("suppression en cours du contenue du compte {}".format(utilisateur))
				os.system("rm -r {}/{}".format(new_chemin,utilisateur))
				
			else:
				print("suppression en cours du contenue du compte {}".format(utilisateur))
				os.system("rm -r {}/{}".format(chemin,utilisateur))
				Retour_Menu=input("Appuyer sur une touche pour retourner au menu principal : ")
				if Retour_Menu!="}":
					Menu()
				else:
					Menu()


def Nombre_Compte():
	os.system("clear")
	print("le nombre de compte FTP sur le serveur est de : ")
	os.system("pure-pw list | wc -l ")
	Retour_Menu=input("Appuyer sur une touche pour retourner au menu principal : ")
	if Retour_Menu!="}":
		Menu()
	else:
		Menu()

def Information_Compte(): 
	info=input("entre le nom de l'utilisateur sur le quel vous voulez avoir des information : ")
	os.system("pure-pw show {}".format(info))
	Retour_Menu=input("Appuyer sur une touche pour retourner au menu principal : ")
	if Retour_Menu!="}":
		Menu()
	else:
		Menu()

def Fin_Programme():
	print("bye")
	os.system("exit")

def Menu():
	os.system("clear")
	print("""

	# # # # # # # # # # # # # # # # # # # # # # # # # #
	#      Programme Création De FTP (Pure-Ftpd)      #
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
	#  2) Configuration du ftp                        #
	#  3) Création d'utilisateur                      #
	#  4) Suppresion d'utilisateur                    # 
	#  5) Création du certificat ssl                  #
	#  6) Ajout Fail2Ban                              #
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
		Création_Utilisateur()
	elif Numéro=="4" :
		Suppression()
	elif Numéro=="5":
		Openssl()
	elif Numéro=="7":
		Fin_Programme()
	else:
		Menu()
Menu()
