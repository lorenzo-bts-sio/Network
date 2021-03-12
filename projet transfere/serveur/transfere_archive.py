#!/usr/bin/python3
import os 
import sys 
import subprocess

racine = os.getcwd()

def verification_root(fonction):
    utilisateur = os.getlogin()

    if utilisateur != "root":
        print("{} désoler il faut  passer root ou te mettre en sudo :) ".format(utilisateur))
        exit()

    return fonction 

@verification_root
def test_repertoire_existe():
    try:
        os.chdir(sys.argv[1])
    except:
        print("impossible de trouver le repertoire {} ".format(sys.argv[1]))
        exit()

@verification_root
def creation_archive_tar():
    os.chdir(racine)
    nom_archive = "{}.tpgm".format(sys.argv[2])
    tar = subprocess.Popen("tar -cf {} {}".format(nom_archive,sys.argv[1]), shell=True)
    os.waitpid(tar.pid, 0)
    print("Le dossier {} est transformer en '{}'".format(sys.args[2],nom_archive))

    return nom_archive

@verification_root
def envoie_archive_via_scp(nom_archive):
    try :
        commande = subprocess.Popen("scp {} lorenzo@192.168.1.38:/var/www/backup".format(nom_archive), shell=True)
        os.waitpid(commande.pid, 0)
    except :
        print("erreur dans le transfere de l'archive {}".format(nom_archive))

    print("L'archive : {} a bien étais etais déplacer sur Debian9 ".format(nom_archive))
    
@verification_root
def destruction_archive(nom_archive):
    try :
        os.remove(nom_archive)
    except:
        print("impossible de supprimer {}".format(nom_archive))

################################MAIN#############################################


test_repertoire_existe()
archive = creation_archive_tar()
envoie_archive_via_scp(archive) # <- faire une version avec socket et serveur python 
destruction_archive(archive)
