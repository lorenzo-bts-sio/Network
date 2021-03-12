#!/usr/bin/python3 

import os 
import sys 
import subprocess

os.getcw
def verification_root(fonction):
    utilisateur=os.getlogin()

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
    os.system("tar cf " + sys.argv[2] +".tpgm " +sys.argv[2])# <- a remplacer par le module  gzip 
    nom_archive =  sys.argv[2] +".tpgm "
    return nom_archive

@verification_root
def envoie_archive_via_scp(nom_archive):
    commande = subprocess.Popen(["scp", nom_archive, "user@ip:chemin_du_repertoire"])
    os.waitpid(commande.pid, 0)
    
@verification_root
def destruction_archive(nom_archive):
    try :
        os.remove(nom_archive)
    except :
        print("impossible de supprimer {} se trouvant dans {} ".format(nom_archive , sys.argv[1]))



test_repertoire_existe()
archive = creation_archive_tar()
envoie_archive_via_scp(archive) # <- faire une version avec socket et serveur python 
destruction_archive(archive)

