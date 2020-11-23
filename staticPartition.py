import os ,subprocess as sp ,pyfiglet

def staticPartition(ssh):
	
	while True :
	
		os.system("clear")
		os.system("tput setaf 3")
		title = pyfiglet.figlet_format("\t\t  LUNIX       STATIC  \n   PARTITIONING")
		print(title)
		os.system("tput setaf 5")
		menu="""
\t|--------------------------------------------------------------|
\t| Press 1 :To see all disks available                          |
\t| Press 2 :To see existing partitions and their mount points   |
\t| Press 3 :To create a static partition                        |
\t| Press 4 :To delete a Partition                               |
\t| Press 5 :To go back to main menu or exit from this menu      |
\t|--------------------------------------------------------------|\n"""
		print(menu)
		os.system("tput setaf 7")
		task = input("Enter your choice : ")

		if(ssh == ""):
			#local system

			if task == '1':
				output = sp.getstatusoutput("fdisk -l")
			elif task == '2':
				output =sp.getstatusoutput("lsblk")
				print(output[1])
				output =sp.getstatusoutput("df -h")
			elif task == '3':
				dname =input ("Enter disk name in which you want to create partition : ")
				mountpt = input("Enter a folder path to which you want to link partition : ")
				os.system("tput setaf 3")
				print("Enter 'n'  to create new partition")
				print(" Select Partition type as ['p' for primary / 'e' for extended] : ")
				print("Enter 'w' to save changes after creating partition.")
				os.system("tput setaf 7")
				os.system("fdisk {}".format(dname))
				print(os.system("lsblk"))
				pname = input("Enter partition name created : ")
				output = sp.getstatusoutput("mkfs.ext4 {}".format(pname))
				print(output[1],"\n") 
				if(output[0] == 0):
					os.system("mkdir {}".format(mountpt))
					output = sp.getstatusoutput("mount {} {}".format(pname,mountpt))
				info = sp.getstatusoutput("df -h")
				print(info[1])
				
			
			elif task == '4':
				dname =input ("Enter disk name in which you want to delete partition : ")
				pname = input("Enter partition name to be deleted : ")
				output = sp.getstatusoutput("umount {}".format(pname))
				os.system("tput setaf 3")
				print("Enter 'd' to delete partition")
				print("Enter 'w' to save changes after deleting partition.")
				os.system("tput setaf 7")
				if(output[0] == 0):
					os.system("fdisk {}".format(dname))
				output = sp.getstatusoutput("lsblk")

			elif task == '5':
				break;
			else:
				print("Invalid Choice!!! Try Again")
				os.system("sleep 1")
				continue

		else:
			#Remote system
			if task == '1':
				output = sp.getstatusoutput("{} 'fdisk -l'".format(ssh))
			elif task == '2':
				output =sp.getstatusoutput("{} lsblk".format(ssh))
				print(output[1])
				output =sp.getstatusoutput("{} 'df -h'".format(ssh))
			elif task == '3':
				dname =input ("Enter disk name in which you want to create partition : ")
				mountpt = input("Enter a folder path to which you want to link partition : ")
				os.system("tput setaf 3")
				print("Enter 'n'  to create new partition")
				print(" Select Partition type as ['p' for primary / 'e' for extended] : ")
				print("Enter 'w' to save changes after creating partition.")
				os.system("tput setaf 7")
				os.system("{} 'fdisk {}'".format(sshdname))
				print(os.system("{} lsblk".format(ssh)))
				pname = input("Enter partition name created : ")
				output = sp.getstatusoutput("{} 'mkfs.ext4 {}'".format(ssh,pname))
				print(output[1],"\n") 
				if(output[0] == 0):
					os.system("{} 'mkdir {}'".format(ssh,mountpt))
					output = sp.getstatusoutput("{} 'mount {} {}'".format(ssh,pname,mountpt))
				info = sp.getstatusoutput("{} 'df -h'".format(ssh))
				print(info[1])
				
			
			elif task == '4':
				dname =input ("Enter disk name in which you want to delete partition : ")
				pname = input("Enter partition name to be deleted : ")
				output = sp.getstatusoutput("{} 'umount {}'".format(ssh,pname))
				os.system("tput setaf 3")
				print("Enter 'd' to delete partition")
				print("Enter 'w' to save changes after deleting partition.")
				os.system("tput setaf 7")
				if(output[0] == 0):
					os.system("{} 'fdisk {}'".format(ssh,dname))
				output = sp.getstatusoutput("{} lsblk".format(ssh))

			elif task == '5':
				break;
			else:
				print("Invalid Choice!!! Try Again")
				os.system("sleep 1")
				continue

		if output[0] == 0:
			os.system("tput setaf 2")
			print("Task successfully completed !!")
			os.system("tput setaf 7")
			print(output[1])
		else:
			os.system("tput setaf 5")
			print("Oops !! Some error occurred : {}".format(output[1]))

		os.system("tput setaf 6")
		input("'Press enter' to continue :")
os.system("tput setaf 7")


#--------main
def main():
login = input(" \t\t1. Local Login\n\t\t2. Remote Login")
if login ==  '1':
	staticPartition("")
elif lofin == '2':
	ip = input("\t\t Enter IP address of Remote Machine: ")
	staticPartition(ip)


# call main function
main()