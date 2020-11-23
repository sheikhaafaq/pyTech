import os,subprocess as sp ,pyfiglet
def lvm(ssh):

	while True :


		os.system("clear")
		os.system("tput setaf 3")
		title = pyfiglet.figlet_format("           LUNIX     LVM\n     PARTITIONING")
		print(title)
		os.system("tput setaf 6")
		menu="""
\t-----------------------------------------------------------------
\t| Press 1 :To see all disks available                           |
\t| Press 2 :To see info of all existing virtual group            |
\t| Press 3 :To see info of a existing virtual group              |
\t| Press 4 :To see info of lv partition                          |
\t| Press 5 :To see existing partitions with their mount points   |
\t| Press 6 :To create virtual group                              |
\t| Press 7 :To create an lv partition                            |
\t| Press 8 :To resize a lv partition                             |
\t| Press 9 :To remove a virtual group                            |
\t| Press 10 :To delete a Partition                               |
\t| Press 11 :To go back to main menu or exit from this menu      |
\t-----------------------------------------------------------------\n"""
		print(menu)
		os.system("tput setaf 7")
		task = input("Enter your choice : ")

		if ssh == "":
			#local system

			if task == '1':
				output = sp.getstatusoutput("fdisk -l")
			elif task == '2':
				output = sp.getstatusoutput("vgdisplay")

			elif task == '3':
				vgname = input("Enter virtual group name : ")
				output = sp.getstatusoutput("vgdisplay {}".format(vgname))

			elif task == '4':
				vgname = input("Enter virtual group name : ")
				lvname = input("Enter logical volume name : ")
				output = sp.getstatusoutput("lvdisplay {}/{}".format(vgname,lvname))

			elif task == '5':
				output = sp.getstatusoutput("df -h")

			elif task == '6':
				vgname=input("Enter virtual group name : ")
				num = input("Enter number of physical volume you want to add : ") 
				num = int(num)
				disks = [input("Enter disk {} name : ".format(i)) for i in range(num)]
				print("disks")
				s = " "
				s = s.join(disks)
				os.system("pvcreate {}".format(s))
				output = sp.getstatusoutput("vgcreate {} {}".format(vgname,s))
				info = sp.getstatusoutput("vgdisplay {}".format(vgname))
				print(info[1])

			elif task == '7':

				vgname =input ("Enter vgname in which you want to create partition : ")
				lvname = input("Enter Logical volume name : ")
				size = input("Enter size of lv [K,M,G,T,P,E] : ")
				mountpt = input("Enter a folder path to which you want to link partition : ")
				output = sp.getstatusoutput("lvcreate -n {} --size {} {} ".format(lvname,size,vgname))
				print(output[1],"\n")
				if(output[0] == 0):
					output = sp.getstatusoutput("mkfs.ext4 /dev/{}/{}".format(vgname,lvname))
					print(output[1],"\n") 
					if(output[0] == 0):
						os.system("mkdir {}".format(mountpt))
						output = sp.getstatusoutput("mount /dev/{}/{} {}".format(vgname,lvname,mountpt))
				info = sp.getstatusoutput("lvdisplay {}/{}".format(vgname,lvname))
				print(info[1])


			elif task == '8':

				vgname =input ("Enter virtual group name in which logicl volume  partition is present : ")
				lvname =input ("Enter logival volume name : ")
				option =input("Enter 'R' to reduce and 'E' to extend size : ")
				size =input ("Enter final size [K,M,G,T,P,E] you want to achieve after extend/reduce : ")
				if option == 'R':
					mountpt = sp.getoutput("findmnt -n -o TARGET /dev/{}/{}".format(vgname,lvname))
					output = sp.getstatusoutput("umount /dev/{}/{}".format(vgname,lvname))
					print(output[1],"\n")
					if(output[0] == 0):
						x = os.system("e2fsck -f /dev/{}/{}".format(vgname,lvname))
						output = sp.getstatusoutput("resize2fs /dev/{}/{} {}".format(vgname,lvname,size))
						print(output[1],"\n")
						if(output[0] == 0):
							print("Enter y if you want to continue else enter n")
							output = sp.getstatusoutput("lvreduce -L {} /dev/{}/{}".format(size,vgname,lvname))
							if(output[0] == 0):
								output=sp.getstatusoutput("mount /dev/{}/{} {}".format(vgname,lvname,mountpt))
									

				elif option == 'E':
					output = sp.getstatusoutput("lvextend -L {} /dev/{}/{}".format(size,vgname,lvname))
					if(output[0] == 0):
						output = sp.getstatusoutput("resize2fs /dev/{}/{}".format(vgname,lvname))
				info = sp.getstatusoutput("lvdisplay {}/{}".format(vgname,lvname))
				print(info[1])

			elif task == '9':
				vgname =input("Enter virtual group name which you wish to delete : ")
				output = sp.getstatusoutput("vgchange -a n {}".format(vgname))
				if(output[0] == 0):
					output = sp.getstatusoutput("vgremove {}".format(vgname))

			elif task == '10':
				vgname =input("Enter virtual group name of which logical volume is a part : ")
				lvname =input("Enter logical volume name which you wish to delete : ")
				output = sp.getstatusoutput("umount /dev/{}/{}".format(vgname,lvname))
				if(output[0] == 0):
					output = sp.getstatusoutput("lvremove -y /dev/{}/{}".format(vgname,lvname))

			elif(task == '11'):
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

		else:
			#remote sys
			if task == '1':
				output = sp.getstatusoutput("{} 'fdisk -l'".format(ssh))
			elif task == '2':
				output = sp.getstatusoutput("{} vgdisplay".format(ssh))

			elif task == '3':
				vgname = input("Enter virtual group name : ")
				output = sp.getstatusoutput("{} 'vgdisplay {}'".format(ssh,vgname))

			elif task == '4':
				vgname = input("Enter virtual group name : ")
				lvname = input("Enter logical volume name : ")
				output = sp.getstatusoutput("{} 'lvdisplay {}/{}'".format(ssh,vgname,lvname))

			elif task == '5':
				output = sp.getstatusoutput("{} 'df -h'".format(ssh))

			elif task == '6':
				vgname=input("Enter virtual group name : ")
				num = input("Enter number of physical volume you want to add : ") 
				num = int(num)
				disks = [input("Enter disk {} name : ".format(i)) for i in range(num)]
				print("disks")
				s = " "
				s = s.join(disks)
				os.system("{} 'pvcreate {}'".format(ssh,s))
				output = sp.getstatusoutput("{} 'vgcreate {} {}' ".format(ssh,vgname,s))
				info = sp.getstatusoutput("{} 'vgdisplay {}' ".format(ssh,vgname))
				print(info[1])

			elif task == '7':

				vgname =input ("Enter vgname in which you want to create partition : ")
				lvname = input("Enter Logical volume name : ")
				size = input("Enter size of lv [K,M,G,T,P,E] : ")
				mountpt = input("Enter a folder path to which you want to link partition : ")
				output = sp.getstatusoutput("{} 'lvcreate -n {} --size {} {}'' ".format(ssh,lvname,size,vgname))
				print(output[1],"\n")
				if(output[0] == 0):
					output = sp.getstatusoutput("{} 'mkfs.ext4 /dev/{}/{}'".format(ssh,vgname,lvname))
					print(output[1],"\n") 
					if(output[0] == 0):
						os.system("{} 'mkdir {}'".format(ssh,mountpt))
						output = sp.getstatusoutput("{} 'mount /dev/{}/{} {}'".format(ssh,vgname,lvname,mountpt))
				info = sp.getstatusoutput("{} 'lvdisplay {}/{}'".format(ssh,vgname,lvname))
				print(info[1])


			elif task == '8':

				vgname =input ("Enter virtual group name in which logicl volume  partition is present : ")
				lvname =input ("Enter logival volume name : ")
				option =input("Enter 'R' to reduce and 'E' to extend size : ")
				size =input ("Enter final size [K,M,G,T,P,E] you want to achieve after extend/reduce : ")
				if option == 'R':
					mountpt = sp.getoutput("{} 'findmnt -n -o TARGET /dev/{}/{}'".format(ssh,vgname,lvname))
					output = sp.getstatusoutput("{} umount /dev/{}/{}'".format(ssh,vgname,lvname))
					print(output[1],"\n")
					if(output[0] == 0):
						x = os.system("{} 'e2fsck -f /dev/{}/{}'".format(ssh,vgname,lvname))
						output = sp.getstatusoutput("{} 'resize2fs /dev/{}/{} {}'".format(ssh,vgname,lvname,size))
						print(output[1],"\n")
						if(output[0] == 0):
							print("Enter y if you want to continue else enter n")
							output = sp.getstatusoutput("{} 'lvreduce -L {} /dev/{}/{}'".format(ssh,size,vgname,lvname))
							if(output[0] == 0):
								output=sp.getstatusoutput("{} 'mount /dev/{}/{} {}'".format(ssh,vgname,lvname,mountpt))
									

				elif option == 'E':
					output = sp.getstatusoutput("{} 'lvextend -L {} /dev/{}/{}'".format(ssh,size,vgname,lvname))
					if(output[0] == 0):
						output = sp.getstatusoutput("{} 'resize2fs /dev/{}/{}'".format(ssh,vgname,lvname))
				info = sp.getstatusoutput("{} 'lvdisplay {}/{}'".format(ssh,vgname,lvname))
				print(info[1])

			elif task == '9':
				vgname =input("Enter virtual group name which you wish to delete : ")
				output = sp.getstatusoutput("{} 'vgchange -a n {}'".format(ssh,vgname))
				if(output[0] == 0):
					output = sp.getstatusoutput("{} 'vgremove {}'".format(ssh,vgname))

			elif task == '10':
				vgname =input("Enter virtual group name of which logical volume is a part : ")
				lvname =input("Enter logical volume name which you wish to delete : ")
				output = sp.getstatusoutput("{} 'umount /dev/{}/{}'".format(ssh,vgname,lvname))
				if(output[0] == 0):
					output = sp.getstatusoutput("{} 'lvremove -y /dev/{}/{}'".format(ssh,vgname,lvname))

			elif(task == '11'):
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
			

			


#main--------------------

def main():
login = input(" \t\t1. Local Login\n\t\t2. Remote Login")
if login ==  '1':
	lvm("")
elif lofin == '2':
	ip = input("\t\t Enter IP address of Remote Machine: ")
	lvm(ip)


# call main function
main()
