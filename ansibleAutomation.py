import os,subprocess as sp,pyfiglet
 


def menu():
	board="\t\t1. Download Basic Ansible Setup\n\t\t2. Ping\n\t\t3. Show Target Node List\n\t\t4. Package Operations\n\t\t5. Service Operions\n"
	title = pyfiglet.figlet_format("        A N S I B L E\n     AUTOMATION")
	print("{}\n{}".format(title,board))
	choice= int(input("\t\t>>"))
	return choice

#--main
def main():
	while True:
		os.system("clear")
		task = menu()
		if task == 1:
			setup()	
		elif task == 2:
			while True:
				
				op = int(input("\t\t1. Ping All\n\t\t2. Ping one Target Node\n\t\t3. Back to main menu \n\n\t\t>>"))
				
				if op == 1:
					#ping all
					output = sp.getstatusoutput("ansible all -m ping")
					print(output[1])
				elif op == 2:
					#ping to target node
					output = sp.getstatusoutput("ansible {} -m ping".format(input("\t\tEnter the Target Node IP Address: ")))
					print(output[1])
				elif op == 3:
					break
				else:
					print("\t\tOption not found! Try Again..")

		elif task == 3:
				#check target list
				output = sp.getstatusoutput("ansible all --list-hosts")
				print(output[1])
		elif task == 4:
			op = int(input("""\t\t1. Install the Software\n\t\t2. Remove the Software\n\n\t\t>>"""))
			#install any package
			if op == 1:
				output = sp.getstatusoutput("ansible {0} -m package -a \"name={1} state=present\"".format(input("\t\tEnter IP of Target Node or type all: "),input("\t\tEnter Service Name: ")))
				print(output[1])
			
			#remove any package
			elif op == 2:
				output = sp.getstatusoutput("ansible {0} -m package -a \"name={1} state=absent\"".format(input("\t\tEnter IP of Target Node or type all: "),input("\t\tEnter Service Name: ")))
				print(output[1])
		elif task == 5:
			op = int(input("""\t\t1. Start Services\n\t\t2. Stop Services\n\n\t\t>>"""))
			#Start services
			if op == 1:
				output = sp.getstatusoutput("ansible {0} -m service -a \"name={1} state=started\"".format(input("\t\tEnter IP of Target Node or type all: "),input("\t\tEnter Service Name: ")))
				print(output[1])
			
			#stop services
			elif op == 2:
				output = sp.getstatusoutput("ansible {0} -m service -a \"name={1} state=stopped\"".format(input("\t\tEnter IP of Target Node or type all: "),input("\t\tEnter Service Name: ")))
				print(output[1])
		elif task == 6:
			break
		else:
			print("\t\tInvalid Option! Try Again...")
		input("Press Enter to continue...")

	

			
def setup():
	op= input("\t\t1. Install Ansible software\n\t\t2. Install sshPass software\n\t\t3. Add new Target Node\n\t\t4. Set inventory path\n\t\t>>")
	if op == '1':
		print("\t\tplease wait! It will take a minute...")
		ansibleOutput=sp.getstatusoutput("yum install ansible")
		print(ansibleOutput[1])
		if ansibleOutput[0] == 0:
			versionOutput=sp.getstatusoutput("ansible --version")
			print(versionOutput[1])
	elif op == '2':
		print("\t\tplease wait! It will take a minute...")
		sshpassOutput=sp.getstatusoutput("yum install sshpass")
		print(sshpassOutput[1])
	elif op == '3':
		updateInventory()
	elif op == '4':
		setInventoryPath()
	else:
		print("\t\tInvalid Option! Try Again...")	


def updateInventory():
	with open("ansibleInventory.txt" , 'a') as file:
		IPaddress = input("\t\tEnter IP of tarrget Node: ")
		user = input("\t\tUsername: ")
		sshPass = input("\t\tEnter Password: ")
		connection = input("\t\tConnection Type: ")
		file.write("{}  ansible_user={}  ansible_ssh_pass={}  ansible_connection={}\n".format(IPaddress,user,sshPass,connection))
	output = sp.getstatusoutput("")

		

#updateInventory()	
def setInventoryPath():

	output = sp.getstatusoutput("pwd")
	s = "[default]\ninventory = {}/ansibleInventory.txt\nhost_key_checking = false".format(output[1])
	ansiblecfg = sp.getstatusoutput("echo \"{}\"| cat >> /etc/ansible/ansible.cfg".format(s))
	if ansiblecfg[0] == 0:
		print("Ansible Inventory successfully configured...")
	else:
		print("oops! error ")



main()
