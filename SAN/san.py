import os 

os.system("apt-get update")
os.system("apt-get install iscsitarget iscsitarget-dkms lvm2")

disque=input("entre le nom du disque dur (sdX) : ")
ajout_disque=input("voulez vous ajouter un autre disque ? (oui/non )")

while ajout_disque !="non":
	disque=input("entre le nom du disque dur (dev/sdX) : ")
	ajout_disque=input("voulez vous ajouter un autre disque ? (oui/non )")
	os.system("fdisk /dev/"+disque)
else:
	os.system("fdisk /dev/"+disque)

os.system("pvcreate /dev/"+disque+"1")
partitions=input("quel est le nom de la partitions : ")
os.system("vgcreate "+partitions+" /dev/"+disque+"1")
nomDuSan=input("entre le nom du disque san :  ")
tailleSan=input("entre la taille du san en mo : ")
os.system("lvcreate -n "+nomDuSan+" -L "+tailleSan+"m "+partitions)
nomcible=input("entre le nom de la cible : ")
ietdConf=open("/etc/iet/ietd.conf", "a")
ietdConf.write("Target "+nomDuSan+":"+nomDuSan)
ietdConf.write("LUN 0 Path=/dev/"+partitions+"/"+nomDuSan+",Type=fileio")
os.system("rm -r /etc/default/iscsitarget")
iscsitarget=open("/etc/default/iscsitarget","a")
iscsitarget.write("""
ISCSITARGET_ENABLE=True
ISCSITARGET_MAX_SLEEP=3


# ietd options
# See ietd(8)for details
ISCSITARGET_OPTIONS="" 
""")
os.system("service iscsitarget restart")

