import os 
	
def Installation():
	os.system("clear")
	print("Installation en cours : ...")
	os.system("apt-get install -y  pure-ftpd pure-ftpd-common fail2ban")
	
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
	os.system("touch /etc/pure-ftpd/donnes")
	Création_Utilisateur(Groupe,Chemin)
	return Groupe,Chemin 

def Retour_Menu():
	Retour_Menu=input("Appuyer sur une touche pour retourner au menu principal : ")
	if Retour_Menu!="}":
		Menu()
	else:
		Menu()

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
	Retour_Menu()


def Suppression():
	Chemin="/var/ftp"
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
		contenue=input("voulez vous supprimer également le contenue du compte {} (y/n) : ".format(utilisateur))
		if contenue !="y":
			print("abandon suppression du contenue du compte {}".format(utilisateur))
			Retour_Menu()
		else:
			chemin=input("le compte se trouve bien dans {}/{} (y/n) ? :".format(chemin,utilisateur))
			if chemin == "n":
				new_chemin=input("quel est le chemin du repertoire du compte {} : ".format(utilisateur))
				print("suppression en cours du contenue du compte {}".format(utilisateur))
				os.system("rm -r {}/{}".format(new_chemin,utilisateur))
				
			else:
				print("suppression en cours du contenue du compte {}".format(utilisateur))
				os.system("rm -r {}/{}".format(Chemin,utilisateur))
				Retour_Menu()


def Nombre_Compte():
	os.system("clear")
	print("le nombre de compte FTP sur le serveur est de : ")
	os.system("pure-pw list | wc -l ")
	Retour_Menu()

def Information_Compte(): 
	info=input("entre le nom de l'utilisateur sur le quel vous voulez avoir des information : ")
	os.system("pure-pw show {}".format(info))
	Retour_Menu()

def Changement_Mot_De_Passe():
	print("vous allez changer le mot de passe d'un compte")
	user=input("entre l'utilisateur : ")
	os.system("pure-pw passwd {} -m ".format(user))
	print("le mot de passe a bien etais changer ")
	Retour_Menu()

def Telechargement():
	print("vous allez changer la limitation de la bande passante du téléchargement d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer la limitation en ko/s : ")
	os.system("pure-pw usermod {} -t {} -m ".format(user,limitation))
	Retour_Menu()

def Envoie():
	print("vous allez changer la limitation de la bande passante d'envoie d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer la limitation en ko/s : ")
	os.system("pure-pw usermod {} -T {} -m ".format(user,limitation))
	Retour_Menu()

def Fichier_Max():
	print("vous allez changer la limitation du nombre de fichier maximum d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer la limitation du nombre de fichier  : ")
	os.system("pure-pw usermod {} -n {} -m ".format(user,limitation))
	Retour_Menu()
	
def Espace_Max():
	print("vous allez changer la limitation du nombre d'espace maximum d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer la limitation du nombre de MO maximum  : ")
	os.system("pure-pw usermod {} -N {} -m ".format(user,limitation))
	Retour_Menu()

def Autorisation_Ip():
	print("vous allez changer l'autorisation ip  d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer l'addresse ip a autorisée  : ")
	os.system("pure-pw usermod {} -i {} -m ".format(user,limitation))
	Retour_Menu()

def Interdiction_Ip():
	print("vous allez changer l'interdiction ip  d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer l'addresse ip a interdire  : ")
	os.system("pure-pw usermod {} -I {} -m ".format(user,limitation))
	Retour_Menu()

def Autorisation_Hotes():
	print("vous allez changer l'autorisation du noms d'hôtes depuis lesquelles l'utilisateur est autorisé à se connecter ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer le noms d'hôtes a autorisée  : ")
	os.system("pure-pw usermod {} -r {} -m ".format(user,limitation))
	Retour_Menu()

def Interdiction_Hotes():
	print("vous allez changer l'interdiction du noms d'hôtes depuis lesquelles l'utilisateur est autorisé à se connecter ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer le noms d'hôtes a interdire  : ")
	os.system("pure-pw usermod {} -R {} -m ".format(user,limitation))
	Retour_Menu()

def Limitation_Horaire():
	print("vous allez changer la plage Horaire depuis lesquelles l'utilisateur est autorisé à se connecter ")
	user=input("entrer le nom du compte  : ")
	heure=input("entrer l'heure d'ouverture du serveur (00 a 23) :")
	minutes=input("entre les minutes d'ouverture (00 a 59) :")
	Fin_Heure=input("entrer l'heure de fermeture du serveur (00 a 23) :")
	Fin_Minutes=input("entrer les minutes de fermeture du serveur (00 a 59) :")
	os.system("pure-pw usermod "+user+" -z "+heure+minutes+"-"+Fin_Heure+Fin_Minutes+" -m ")
	print("vous avez autorisé "+user+" a ce connecter de "+heure+minutes+" a "+Fin_Heure+Fin_Minutes )
	Retour_Menu()

def Nombre_Session():
	print("vous allez changer le nombre de session simultané d'un compte ")
	user=input("entrer le nom du compte  : ")
	limitation=input("entrer le nombre de session simultané a accepter  : ")
	os.system("pure-pw usermod  {} -y {} -m ".format(user,limitation))
	Retour_Menu()



def fail2ban_IpB_FTP():
	print("voici la liste des ip bannis pour le ftp ")
	os.system("fail2ban-client status pure-ftpd")
	Retour_Menu=input("Appuyer sur une touche pour retourner au options de fail2ban")
	if Retour_Menu=="a":
		Fail2Ban()
	else:
		Fail2ban()

def fail2ban_IpB_SSH():
	print("voici la liste des ip bannis pour le ssh ")
	os.system("fail2ban-client status sshd")
	Retour_Menu=input("Appuyer sur une touche pour retourner au options de fail2ban")
	if Retour_Menu=="a":
		Fail2Ban()
	else:
		Fail2ban()

def fail2ban_debane_FTP():
	ip=input("entrer l'ip que vous voulez débanir pour le ftp : ")
	os.system("fail2ban-client set pure-ftpd unbanip {}".format(ip))
	print("l'ip : {} a bien etais débanie".format(ip))
	Retour_Menu=input("Appuyer sur une touche pour retourner au options de fail2ban")
	if Retour_Menu=="a":
		Fail2Ban()
	else:
		Fail2ban()

def fail2ban_debane_SSH():
	ip=input("entrer l'ip que vous voulez débanir pour le ssh : ")
	os.system("fail2ban-client set sshd unbanip {}".format(ip))
	print("l'ip : {} a bien etais débanie".format(ip))
	Retour_Menu=input("Appuyer sur une touche pour retourner au options de fail2ban")
	if Retour_Menu=="a":
		Fail2Ban()
	else:
		Fail2ban()

def fail2ban_debane_SSH():
	ip=input("entrer l'ip que vous voulez banir pour le ssh : ")
	os.system("fail2ban-client set sshd banip {}".format(ip))
	print("l'ip : {} a bien etais banie".format(ip))
	Retour_Menu=input("Appuyer sur une touche pour retourner au options de fail2ban")
	if Retour_Menu=="a":
		Fail2Ban()
	else:
		Fail2ban()

def fail2ban_debane_FTP():
	ip=input("entrer l'ip que vous voulez banir pour le ftp : ")
	os.system("fail2ban-client set pure-ftpd banip {}".format(ip))
	print("l'ip : {} a bien etais banie".format(ip))
	Retour_Menu=input("Appuyer sur une touche pour retourner au options de fail2ban")
	if Retour_Menu=="a":
		Fail2Ban()
	else:
		Fail2ban()


def Fin_Programme():
	print("bye")
	os.system("exit")



def Fail2Ban():
	print("""
# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#  1) voir les ip banis ftp                         #
#  2) voir les ip banis ssh                         #
#  3)banir une ip pour le ftp                       #
#  4)banir une ip pour le ssh                       #
#  5)débanir une ip pour le ftp                     #
#  6)débanir une ip pour le ssh                     #
#  7)retour au menu principal                       #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	choix=input("entre le numéro : ")
	if choix=="1":
		fail2ban_IpB_FTP()
	elif choix=="2":
		fail2ban_IpB_SSH()
	elif choix=="5":
		fail2ban_debane_FTP()
	elif choix=="6":
		fail2ban_debane_SSH()
	elif choix=="3":
		fail2ban_bane_FTP()
	elif choix=="4":
		fail2ban_bane_SSH()




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
	#  6) Fail2Ban                                    #
	#  7) Liste des comptes                           #
	#  8) Information compte                          #
	#  9) Changement mot de passe                     #
	#  10)Limitation du téléchargement                # 
	#  11)Limitation de l'envoie                      #
	#  12)Limitation nombre fichier                   #
	#  13)Limitation de l'espace                      #
	#  14)Autorisation IP                             #
	#  15)Interdiction IP                             #
	#  16)Autorisation non hote                       #
	#  17)Interdiction non hote                       #
	#  18)Limitation Horaire                          #
	#  19)Nombre de session                           #
	#  20)Backup                                      #
	#  21)Fin de programme                            #
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
	elif Numéro=="6":
		Fail2Ban()
	elif Numéro=="7":
		Nombre_Compte()
	elif Numéro=="8":
		Information_Compte()
	elif Numéro=="9":
		Changement_Mot_De_Passe()
	elif Numéro=="10":
		Telechargement()
	elif Numéro=="11":
		Envoie()
	elif Numéro=="12":
		Fichier_Max()
	elif Numéro=="13":
		Espace_Max()
	elif Numéro=="14":
		Autorisation_Ip()
	elif Numéro=="15":
		Interdiction_Ip()
	elif Numéro=="16":
		Autorisation_Hotes()
	elif Numéro=="17":
		Interdiction_Hotes()
	elif Numéro=="18":
		Limitation_Horaire()
	elif Numéro=="19":
		Information_Compte()
	else:
		Menu()
Menu()
