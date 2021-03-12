import os
import subprocess 


def installation():
	os.system("clear")
	subprocess.Popen(["apt update"],shell=True,stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
	subprocess.Popen(["apt install -y isc-dhcp-server "],shell=True,stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
	print("Installation en cours ...")
	if stderr == "":
		print("Installation de isc-dhcp-server : [\033[32;1m SUCCES \033[0m]")
	else:
		pass
	retour=input("Pour retourner au menu principal appuyer sur n'importe qu'elle touche : ")
	if retour==retour:
		menu()

def configuration():
	os.system("clear")
	print("""
	# # # # # # # # # # # # # # # # # # # # # # # # # # #
	#                                                   #
	#  Bienvenue dans la configuration du serveur DHCP  #
	#  plusieur questions vont vous etes poser afin de  #
	#  configurer le serveur DHCP comme le voulais      #
	#  de manière par défaut d'autres ajouts seront     #
	#  possible grace au choix du menu principal        #  
	#                                                   #
	# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	os.chdir("/etc/dhcp")
	os.system("mv dhcpd.conf dhcpd.conf.old")

	reseau=input("Veuillez saisir le  sous réseau : ")
	masque=input("Veuillez saisir son masque : ")
	debutPlage=input("Veuillez saisir la premiere ip de la plage : ")
	finPlage=input("Veuillez saisir la derniere ip de la plage : ")
	#masque=input("Veuillez saisir son masque : ")
	brodacast=input("Veuillez saisir le brodacast : ")
	passerelle= input("Veuillez saisir la passerelle : ")
	dns=input("Veuillez saisir l'ip du serveur dns primaire: ")
	dns2=input("Veuillez saisir l'ip du serveur dns secondaire : ")
	nomDomaine=input("Veuillez saisir le nom de domaine que vous voulais : ")
	bailDefault=input("Veuillez saisir la durée en seconde du bail par défaut : ")
	bailMax=input("Veuillez saisir la durée maximal du bail en seconde : ")
#----------------------------------------------------------------------------------------------------------------------
	configuration= open("dhcpd.conf" ,"w") 
	subnet=open("subnet.txt","w")
	configuration.write("# CONFIGURATION PAR DEFAULT CREER VIA LE PROGRAMME \n")
	configuration.write("\n")
	configuration.write("log-facility local 17 ; #PERMET UNE REDIRECTION DES LOGS \n")
	configuration.write("ddns-update-style none ;  # NE FAIT PAS DE MISE A JOUR DNS ENLEVER NONE POUR FAIRE L'INVERSE \n")
	configuration.write("\n")
	configuration.write("subnet {} netmask {}   # DECLARATION DU SOUS RESEAU \n".format(reseau,masque))
	subnet.write("subnet {} netmask {}  \n".format(reseau,masque))
	subnet.close()
	configuration.write("{ \n")
	configuration.write("range {} {} ;  # PLAGE D'IP UTILISER \n".format(debutPlage,finPlage))
	configuration.write("option subnet-mask  {} ; # MASQUE DE SOUS RESEAU \n".format(masque))
	configuration.write("option brodacast-address {} ; # ADDRESSE BRODCAST \n".format(brodacast))
	configuration.write("option routers {} ; # PASERELLE PAR DEFAULT \n".format(passerelle))
	configuration.write("option domain-name-servers {} , {} ; # IP DES SERVEURS DNS \n".format(dns,dns2))
	configuration.write("option domain-name '{}' ;# NOM DU DOMAINE \n".format(nomDomaine))
	configuration.write("default-lease-time {} ; # TEMPS  DE ROUNOUVELLEMENT DES IP PAR DEFAULT \n".format(bailDefault))
	configuration.write("max-lease-time {} ; # TEMPS DE ROUNOUVELLEMENT DES IP MAX \n".format(bailMax))
	configuration.write("\n")
	configuration.write("	} \n")
	configuration.write("\n")
	configuration.write("# -------------------------------------------------------------------------------------")
	configuration.close()

	print("La configuration du serveur DHCP est : [\033[32;1m SUCCES  \033[0m] ")
	retour=input("Pour retourner au menu principal appuyer sur n'importe qu'elle touche : ")
	if retour==retour:
		menu()
		
def creationClasse():
	os.system("clear")
	print("""
	# # # # # # # # # # # # # # # # # # # # # # # # # # #
	#                                                   #
	#  Bienvenue dans la configuration du serveur DHCP  #
	#  plusieur questions vont vous etes poser afin de  #
	#  configurer le serveur DHCP comme le voulais      #
	#  de manière par défaut d'autres ajouts seront     #
	#  possible grace au choix du menu principal        #  
	#                                                   #
	# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	print("""
	# # # # # # # # # # # # # # # # # # # # # # # # # # #
	#                                                   #
	#  Vous voulez creer une classe en fonctions de     #
	#---------------------------------------------------#
	#                                                   #
	#  [\033[32;1m1\033[0m] le nom des machines                          #
	#  [\033[32;1m2\033[0m] leur marques                                 #
	#  [\033[32;1m3\033[0m] leur addresse MAC                            #  
	#                                                   #
	# # # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	choix = int(input("Veuillez entrer votre choix : " ))
	if choix==1:
		os.system("clear")
		nom=input("Veuillez saisir le nom de votre classe : ")
		positon=int(input("Veuillez saisir l'emplacement a partir de 0 ou ce trouve le nom sur le client (labo-1 = 6): "))
		#-------------------------------------------------------------------------------------------------------
		os.chdir("/etc/dhcp")
		classe=open("dhcpd.conf" ,"a") 
		classe.write("\n")
		classe.write("#------------------- {} -------------------------- \n".format(nom.upper()))
		classe.write("class '{}' \n".format(nom))
		classe.write("{ \n")
		classe.write("match if substring(option user-class,{},{})='{} ;' \n".format(positon,len(nom),nom))

		ajout=input("voulez vous ajouter un filtre supplementaire a la classe en cours (y/n) : ")
		if ajout=="y":
				with open("subnet.txt",'r') as subnet:
					sub=subnet.readline()

				classe.write("{} \n".format(sub))
				classe.write("{ \n") 
				classe.write("pool \n")
				classe.write("{ \n")
				classe.write("allowed members of '{}' ; \n".format(nom))
				debutPlage=input("Veuillez saisir la premiere ip de la plage : ")
				finPlage=input("Veuillez saisir la derniere ip de la plage : ")
				masque=input("Veuillez saisir son masque : ")
				brodacast=input("Veuillez saisir le brodacast : ")
				passerelle= input("Veuillez saisir la passerelle : ")
				dns=input("Veuillez saisir l'ip du serveur dns primaire: ")
				dns2=input("Veuillez saisir l'ip du serveur dns secondaire : ")
				
			
#----------------------------------------------------------------------------------------------------------------------
	
				classe.write("range {} {} ;  # PLAGE D'IP UTILISER \n".format(debutPlage,finPlage))
				classe.write("option subnet-mask  {} ; # MASQUE DE SOUS RESEAU \n".format(masque))
				classe.write("option brodacast-address {} ; # ADDRESSE BRODCAST \n".format(brodacast))
				classe.write("option routers {} ; # PASERELLE PAR DEFAULT \n".format(passerelle))
				classe.write("option domain-name-servers {} , {} ; # IP DES SERVEURS DNS \n".format(dns,dns2))
				classe.write("\n")
				classe.write("	} \n")
				classe.write("\n")
				classe.write("		} \n")
				classe.write("				} \n")

				classe.write("# -------------------------------------------------------------------------------------")
				classe.close()
				retour=input("Pour retourner au menu principal appuyer sur n'importe qu'elle touche : ")
				if retour==retour:
					menu()

		else:
			with open("subnet.txt",'r') as subnet:
				sub=subnet.readline()

		classe.write("{} \n".format(sub))
		classe.write("{ \n") 
		classe.write("pool \n")
		classe.write("{ \n")
		classe.write("allowed members of '{} ;' \n".format(nom))
		debutPlage=input("Veuillez saisir la premiere ip de la plage : ")
		finPlage=input("Veuillez saisir la derniere ip de la plage : ")
		masque=input("Veuillez saisir son masque : ")
		brodacast=input("Veuillez saisir le brodacast : ")
		passerelle= input("Veuillez saisir la passerelle : ")
		dns=input("Veuillez saisir l'ip du serveur dns primaire: ")
		dns2=input("Veuillez saisir l'ip du serveur dns secondaire : ")
				
			
#----------------------------------------------------------------------------------------------------------------------
	
		classe.write("range {} {} ;  # PLAGE D'IP UTILISER \n".format(debutPlage,finPlage))
		classe.write("option subnet-mask  {} ; # MASQUE DE SOUS RESEAU \n".format(masque))
		classe.write("option brodacast-address {} ; # ADDRESSE BRODCAST \n".format(brodacast))
		classe.write("option routers {} ; # PASERELLE PAR DEFAULT \n".format(passerelle))
		classe.write("option domain-name-servers {} , {} ; # IP DES SERVEURS DNS \n".format(dns,dns2))
		classe.write("\n")
		classe.write("	} \n")
		classe.write("\n")
		classe.write("			} \n")
		classe.write("					} \n")
		classe.write("# -------------------------------------------------------------------------------------")
		classe.close()
		retour=input("Pour retourner au menu principal appuyer sur n'importe qu'elle touche : ")
		if retour==retour:
			menu()

def fin():
	os.system("clear")
	print("fin de Programme")
	os.system(exit)

def menu():
	os.system("clear")

	print(
"""
	# # # # # # # # # # # # # # # # # # # # # # # # # #
	#      Programme Création de Serveur DHCP         #
	#                       &                         #
	#         Administration du Serveur DHCP          #
	#                                                 #
	#                              By:Oznerol         #
	# # # # # # # # # # # # # # # # # # # # # # # # # #
	#                                                 #
	#                                                 #
	#  Veuillez choisir dans les options ci dessous   #
	#  en entrant son numéro (exemple 1 , 2 etc )     #
	#                                                 #
	#-------------------------------------------------#
	#  [\033[32;1m1\033[0m] Installation                               #
	#  [\033[32;1m2\033[0m] Configuration                              #
	#  [\033[32;1m3\033[0m] Création d'une Classe                      #
	#                                                 #
	#  [\033[31;1m99\033[0m] Fin de Programme                          #
	#                                                 #
	# # # # # # # # # # # # # # # # # # # # # # # # # #
""")
	choix=int(input("saisisez votre choix : "))
	if choix==1:
		installation()
	elif choix==2:
		configuration()
	elif choix==3:
		creationClasse()
	elif choix==99:
		fin()
	else:
		menu()
	

menu()