# -*- coding: utf-8 -*-
from gophish import Gophish
from gophish.models import *
import csv
import dateutil
from datetime import date,datetime,timedelta
import random
import base64
import sys
import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('Gophish.ini')

api_key=config.get('Gophish','api_key')
gp_host=config.get('Gophish','gp_host')
api = Gophish(api_key,gp_host,verify=False)

urlph = config.get('Campaigns','urlph')

#######################
#Fonctions de Listing #
#######################
def ListeCampagne():
	for campaign in api.campaigns.get():
		print "Id: ", campaign.id, " Name: ", campaign.name

def ListeGroupe():
	for groups in api.groups.get():
		print "Id: ",groups.id," Name: ",groups.name

def ListeSender():
	for smtp in api.smtp.get():
		print "Id: ",smtp.id," Name: ",smtp.name

def ListeTemplate():
	for template in api.templates.get():
		print "Id: ",template.id," Name: ", template.name

def ListeLanding():
	for page in api.pages.get():
		print "Id: ", page.id," Name: ", page.name

##########################
#Fonctions de suppression#
##########################
def SupprCamp():
	print "Existing campign list: "
	ListeCampagne()
	camp = raw_input("Input the campign ID to delete: ")
	delete = api.groups.delete(camp)
def SupprGrp():
	print "Existing group list: "
	ListeGroupe()
	grp = raw_input("Input the group ID to delete: ")
	delete = api.groups.delete(grp)

def SupprTempl():
	print "Existing tempalte list: "
	ListeTemplate()
	templ = raw_input("Input the templte ID to delete")
	delete = api.templates.delete(templ)

def SupprSMTP():
	print "Existing sender list: "
	ListeSender()
	snd = raw_input("Input the sender ID to delete")
	delete = api.smtp.delete(snd)

def SupprAllGrp():
	print "[*] deleting all groups ..."
	for group in api.groups.get():
		api.groups.delete(group.id)
	print "[*] Groups deleted"


##########################
#    Fonctions d'ajout   #
##########################


def Ajout_Template():
##Broken function, will be fixed soon
	print "Tempalte name: "
	n = raw_input("Name: ")
	print "Email Object: "
	o = raw_input("Objet?: ")
	print "Will you use plaintext (0) or html (1) for the mail body?"
	choice = raw_input("choice: 0 or 1 ?: ")
	if choice == '0':
		print "Input the email's body (plaintext): "
		text = raw_input("plaintext: ")
		html = ""
	elif choice == '1':
		print "Input the email's body (HTML)"
		text = ""
		html = raw_input("HTML: ")

### Probleme sur la fonction de parsing interne a Gophish creant un bug
### sur les pieces jointes meme si on en envoie pas

	print "Do you wish to add an attachment ? (0 or 1)"
	choice = raw_input("0 or 1")
	Attachments = []
	if choice == '1':
		npj = raw_input("Attachment name: ")
		tpj = raw_input("File type: ")
		cpj = raw_input("Absolute path to the file: ")   
		with open(cpj, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
		objAtt = Attachment(name=npj,type=tpj,content=encoded_string)
		Attachments.append(objAtt)

	template = Template(name=n, subject=o, text=text, html=html,attachments=Attachments)
	template = api.templates.post(template)
				


def Ajout_SMTP():
	n = raw_input("Sender name: ")
	f_a = raw_input ("Sender email: ")
	h = raw_input ("SMTP host: ")
	print "Does your SMTP server requires login ? (0 or 1)"
	resp = raw_input("Choice 0 or 1?: ")
	if resp == 1:
		usrn = raw_input ("Login: ")
		pwd = raw_inpur ("password: ")
	else:
		usrn=""
		pwd=""
	smtp = SMTP(name=n, from_address=f_a, host=h, username=usrn, password=pwd)
	smtp = api.smtp.post(smtp)

def Ajout_Landing():

	n = raw_input("Landing page name: ")
	html = raw_input("Input page HTML code: ")
	
	page = Page(name=n,html=html)
	page = api.pages.post(page)


def Ajout_Groupe_Random():
        nb_grp = int(config.get('Groups','Nb_groups'))
        inputcsv = config.get('Groups','csvinput')
	
	Grps_solo = []
        Grp_Targets = []
        totalgrps = {}
        for i in range(nb_grp):
                grpname = 'Groupe ' + str(i)
		Grps_solo.append(grpname)
                Grp_Targets.append([])
                totalgrps[i] = 0
        cr = csv.DictReader(open(inputcsv,"rb"))
       # print 'totalgrps initialisé: ' ,totalgrps
        for row in cr:
                x = User(first_name=row['first_name'],last_name=row['last_name'],email=row['email'],position=row['position'])
                swap = []

                for value in totalgrps.values():
                  #      print value
                        swap.append(value)

              #  print "swap: ",swap
                nbmin = min(swap)

                grpkeymin = totalgrps.keys()[totalgrps.values().index(nbmin)]
              #  print "la clef minimale est : ", grpkeymin
                grp_to_update = grpkeymin
                Grp_Targets[grp_to_update].append(x)

              #  print "grptoupdate", grp_to_update
              #  print "totalgrps avant incrm: ", totalgrps
                totalgrps[grp_to_update]+=1
              #  print 'apres increm', totalgrps
        for i in range(nb_grp):
                groups = Group(name=Grps_solo[i], targets=Grp_Targets[i])
                group = api.groups.post(groups)


def Ajout_Groupe_Pos():
	nb_grp = int(config.get('Groups','Nb_groups'))
	print range(nb_grp)


	#initialisation des dicos
	csvinput =  config.get('Groups','csvinput')
		
	GrpTargets=[]
	Targets=[]
	Repartition_groupes=[]
	Repartition_users = []	
	
	cr = csv.DictReader(open(csvinput,"rb"))
		
	##Initialisation des dictionnaires
	for i in range(nb_grp):
		#print ("groupe"+str(i))
		GrpTargets.append("groupe"+str(i))
		GrpTargets[i] = list()
		Repartition_users.append("groupe"+str(i))
		Repartition_users[i] = list()
		
		print GrpTargets
		Repartition_groupes.append("groupe"+str(i))
		Repartition_groupes[i] = dict()
		print Repartition_groupes
		
	## Initialisation des dictionnaires de localisation à 0
	location=[]
	for row in cr:
		location.append(row["location"])
		
	for j in Repartition_groupes:
		for i in location:
			j.update({i:0})
	#print Repartition_groupes
	
	## Pour chaque ligne du csv
	##		  on defini curloc = la Localisation dans la ligne entrain d'être lue
	##
	cr = csv.DictReader(open(csvinput,"rb"))
	for row in cr:

		curloc = (row["location"])
		x = {}
		totalgrp = {}

		for i in range(nb_grp):
			x[i] = Repartition_groupes[i].get(curloc)

			for i in range(nb_grp):
				total = 0

				for value in Repartition_groupes[i].values():
					total = total+value

				totalgrp[i] = total

		candidats = []
		SrchMinLoc = []
		for valeur in x.values():
			SrchMinLoc.append(valeur)

		nbmin = min(SrchMinLoc)
		lockeymin = x.keys()[x.values().index(nbmin)]
		locvalmin = x.get(lockeymin)

		for cle,valeur in x.items():
			if valeur == locvalmin:
				candidats.append(cle)
			else:
				continue


		SrchMinGrpPop = []
		for valeur in totalgrp.values():
			SrchMinGrpPop.append(valeur)

		nbmin = min(SrchMinGrpPop)
		grpkeymin = totalgrp.keys()[totalgrp.values().index(nbmin)]

		for candidat in candidats:
										
			if candidat == grpkeymin:
				grp_to_update = candidat
				break
			else:
				grp_to_update = random.choice(candidats)



		Repartition_groupes[grp_to_update][curloc]+=1
		
		
		y = User(first_name=row['first_name'],last_name=row['last_name'],email=row['email'],position=row['position'])
		GrpTargets[grp_to_update].append(y)
		u= row['first_name'] + " " + row['last_name']+" "+row['email']
                Repartition_users[grp_to_update].append(u)

        f = open("repartition_grp.txt","a")
        for i in range(nb_grp):
                f.write("groupe: " + str(i)+": ")
                f.write(str(Repartition_users[i]))
                f.write("\n")

		
		
		groups = []
	print Repartition_users
	for z in range(nb_grp):
		print ("voici la composition du groupe: ", z)
		print Repartition_groupes[z]
		print "=========================================================================="
				   
		group = Group(name="groupe"+str(z), targets=GrpTargets[z])
		group = api.groups.post(group)
				
		groups.append([Group(name="groupe"+str(z))])
	return groups


def select_campaign_options():
#Initialisation des differents parametres

	#date table initialisation
	datecamp = []
	f = open('dates','r')
	for i in f.readlines():
		datecamp.append(i.rstrip())

	#Selecting all senders
	senders = []
	for smtp in api.smtp.get():
		senders.append(str(smtp.name))
		
	#Selecting all templates
	templates = []
	for template in api.templates.get():
		templates.append(str(template.name))

	#Selecting all landing pages
	parking = []
	for pages in api.pages.get():
		parking.append(str(pages.name))

	#Selecting all groups
	groupselect = []
	for groups in api.groups.get():
		groupselect.append(str(groups.name))

	options = [datecamp,senders,templates,parking,groupselect]
	return options

def AjouTCampagne_Association_sender_template(options):
#Initialisation des differents parametres
	urlph = config.get('Campaigns','urlph')
	lastusedtemplate = ""
	
	for i in range(len(options[4])):
		TemplatePanel = []
		EmetPanel = []
		
		date = options[0][i]
		groupe = [Group(name=options[4][i])]
		
		grpswap = options[4][i].split()
		grptag = grpswap[0]
		
	#Récupération des templates et emmeteurs liés au tag du groupe
		for emet in options[1]:
			emetswap = emet.split()
			if emetswap[0] == grptag:
				EmetPanel.append(emet)
			else:
				continue
	
		for template in options[2]:
			templateswap = template.split()
			if templateswap[0] == grptag:
				TemplatePanel.append(template)
			else:
				continue
	#Choix du template aléatoire et non répétitif et association avec le bon emmeteur
		
		templateuse = random.choice(TemplatePanel)
		#debug
		#print "template utilisé: ", templateuse
		#print "dernier template utilisé: ", lastusedtemplate
		while 1:
			if templateuse == lastusedtemplate:
				#print "Template déja utilisé pour la campagne precedente -- choice d'un autre template"
				templateuse = random.choice(TemplatePanel)
			else:
				break
		#mise a jour du dernier template utilisé
		lastusedtemplate = templateuse
		
		#Recupération du tag emmeteur dans le template utilisé
		
		TemplateSenderSwap = templateuse.split()
		
		templateSenderTag = TemplateSenderSwap[1]
		templatesenderfirsttag = TemplateSenderSwap[0]
		#Affiliation de l'ammeteur au template
		
		for emet in EmetPanel:	
			EmetTemplateSwap = emet.split()
			EmetTemplateTag = EmetTemplateSwap[1]
			EmetTemplateFirstTag = EmetTemplateSwap[0]
			#debug
			#print "1 tag emet: ",EmetTemplateFirstTag
			#print "1 tag template ",templatesenderfirsttag
			#print "2 tag emet ", templateSenderTag
			#print "2 tag template ", EmetTemplateTag
		
			if EmetTemplateTag == templateSenderTag and templatesenderfirsttag == EmetTemplateFirstTag :
				emetuse = emet
			else:
				print "Emmeteur imcompatible, on continue"
				continue

		garage = random.choice(options[3])
			

		finemet = SMTP(name=emetuse)
		fintemplate = Template(name=templateuse)
		fingarage = Page(name=garage)
		name = options[0][i] + ' ' + options[4][i] + ' ' +  emetuse + ' ' + templateuse
		
		
		print "la campagnes va etre créée avec les elements suivants: "
		print "Name: ",name
		print "Groupe: ",options[4][i]
		print "Page de garage: ", garage
		print "Template: ",templateuse
		print "Emmeteur: ",emetuse
		print "URL de renvoi: ", urlph
		print "Date de lancement: ",options[0][i]
		
		confirmation = raw_input("Confirmer? (o ou n): ")
		if confirmation == 'o':
			campaign  = Campaign(name=name, groups=groupe, page=fingarage,template=fintemplate, smtp=finemet, url=urlph, launch_date=date) 
			campaign = api.campaigns.post(campaign)
			try:
				print campaign.name, ' id: ', campaign.id
			except:
				print campaign.message
		else:
			break

def Ajout_campagne_random_association(options):
	urlph = config.get('Campaigns','urlph')
	for i in range(len(options[4])):
		print "Voici les element de la campagne: "
		
		name = "test" + str(i)
		print "le nom de la campagne est: ",name

		date = options[0][i]
		print "date: ", date

		groupe = [Group(name=options[4][i])]
		print "groupe: ",groupe

		sender0 = str(random.choice(options[1]))
		print "l'emmeteur des mails sera: ",sender0
		sender = SMTP(name=sender0)

		template0 = str(random.choice(options[2]))
		print "le template utilisé pour cette campagne est: ",  template0
		template = Template(name=template0)

		garage0 = str(random.choice(options[3]))
		print "la page de parking utilisée pour cette campagne est: ",garage0
		garage = Page(name=garage0)
		print "l'url de tracking est: ",urlph
		print ""
		print ""

		campaign  = Campaign(name=name, groups=groupe, page=garage,template=template, smtp=sender, url=urlph, launch_date=date) 
		campaign = api.campaigns.post(campaign)
		try:
			print campaign.name, ' id: ', campaign.id
		except:
			print campaign.message

def Ajout_Campagne_Manuel(options):
	urlph = config.get('Campaigns','urlph')
	for i in range(len(options[4])):
		print "Saisie les element de la campagne: ", i
		print ""
		groupe = [Group(name=options[4][i])]
		print "Le groupe utilisé pour cette campage sera: ", options[4][i]
		print ""
		name = raw_input("veuillez saisir le nom de la campagne: ")
		date = options[0][i]
		print ""
		print options[1]
		sender0 = raw_input("veuillez sasir l'expetieur qui sera associé à la campagne: ")
		sender = SMTP(name=sender0)
		print ""
		print options[2]
		template0 = raw_input("veuillez sasir le template qui sera associé à la campagne: ")
		template = Template(name=template0)
		print""
		print options[3]
		garage0 = raw_input("veuillez sasir la page de garage qui sera associé à la campagne: ")
		garage = Page(name=garage0)
		print ""
		print "le nom de la campagne est: ",name
		print "La date de lancement de la campagne est:: ", date
		print "L'emmeteur associé à la campagne est: ",sender0
		print "le template utilisé pour cette campagne est: ",  template0
		print "la page de garage utilisee pour cette campagne est: ",  garage0
		print "l'url de tracking est: ",urlph
		print ""
		print ""
		campaign  = Campaign(name=name, groups=groupe, page=garage,template=template, smtp=sender, url=urlph, launch_date=date)
		campaign = api.campaigns.post(campaign)
		try:
			print campaign.name, ' id: ', campaign.id
		except:
			print campaign.message
#############
# Reporting #
#############
#necessite GoReport dans le répertoire d'execution du script
# https://github.com/chrismaddalena/GoReport

def Report():
	gorepath= config.get('Goreport','goreport_path')
	print "Existing campaigns: "
	ListeCampagne()
	idselec = raw_input("Slect the campaign ID you wish to report: ")
	formatselec = raw_input("Desired output?: quick, word, csv: ")
	string = 'python '+ gorepath + ' --id ' + str(idselec) + ' --format ' + str(formatselec)

	print string
	os.system(string)
	
def date_creation():
	# TODO: gestion des jours ouvrés
        year=int(config.get('Dates','year'))
        month=int(config.get('Dates','month'))
        day=int(config.get('Dates','day'))
        nb_cmp=config.get('Dates','nb_cmp')
        morning_wave = config.get('Dates','morning_wave').strip("'")
        afternoon_wave = config.get('Dates','afternoon_wave').strip("'")
        date_file = config.get('Dates','date_file')
        delete_old_datefile = 'rm -f ' + date_file
        os.system(delete_old_datefile)
        f = open(date_file,'a')
        for i in range(int(nb_cmp)/2):
                dayselect = date(year,month,day)
                f.write(str(dayselect) + 'T' + morning_wave + '+02:00'+'\n')
                f.write(str(dayselect)+'T'+afternoon_wave+'+02:00'+'\n')
                day += 1
        print "[*] fichier créé."
        f.close
	
##################
# Banner et menu #
##################
def banner():

	print'============================================================================================================'	
	print'  ____  ___  ____  _   _ ___ ____  _   _        ____ ___  _   _ _____ ____   ___  _     _     _____ ____    '
	print' / ___|/ _ \|  _ \| | | |_ _/ ___|| | | |      / ___/ _ \| \ | |_   _|  _ \ / _ \| |   | |   | ____|  _ \   '
	print'| |  _| | | | |_) | |_| || |\___ \| |_| |_____| |  | | | |  \| | | | | |_) | | | | |   | |   |  _| | |_) |  '
	print'| |_| | |_| |  __/|  _  || | ___) |  _  |_____| |__| |_| | |\  | | | |  _ <  |_| | |___| |___| |___|  _ <   '
	print' \____|\___/|_|   |_| |_|___|____/|_| |_|      \____\___/|_| \_| |_| |_| \_|\___/|_____|_____|_____|_| \_\  '
	print'														  '
	print'============================================================================================================'	



def menu():
	print ""
	print "1) Campaign managment"
	print "2) Groups and users managment"
	print "3) Template managment"
	print "4) Landing pages managment"
	print "5) Sender managment"
	print "6) Reporting"
	print "7) Exit"
	print "======================================================================="
	print ""

	menuChoice = raw_input( "What do you want to do ?: ")
	return menuChoice

def main():
	attr_mod = config.get('Campaigns','Attr_mod')	
	ch = config.get('Groups','attr_grp')
	while 1:
		banner()
		menuChoice = menu()
		if menuChoice == '1':
			print "1) List campaigns"
			print "2) Campaign managment"
			print "3) Delete a campaign"
			print "4) Create a date file"
			print ""
			menu1Choice = raw_input("Your choice?: ")
			if menu1Choice == '1':
				ListeCampagne()
			elif menu1Choice == '2':
				if attr_mod == 'manuel':
					Ajout_Campagne_Manuel(select_campaign_options())

				elif attr_mod == 'auto':
					Ajout_campagne_random_association(select_campaign_options())

				elif attr_mod == 'tag':
					AjouTCampagne_Association_sender_template(select_campaign_options())

			elif menu1Choice == '3':
				SupprCamp()
			elif menu1Choice == '4':
				date_creation()
			else:
				continue

		elif menuChoice == '2':
			print "1) List groups"
			print "2) Add Groups"
			print "3) Delete one group"
			print "4) Delete all groups"
			print ""
			menu2Choice = raw_input("Your choice?: ")
			if menu2Choice == '1':
				ListeGroupe()
				raw_input("press enter to continue")
			elif menu2Choice == '2':
				if ch == 'random':
					Ajout_Groupe_Random()
					raw_input("press enter to continue")

				if ch =='localisation':
					Ajout_Groupe_Pos()
					raw_input("press enter to continue")


			elif menu2Choice == '3':
				SupprGrp()
				raw_input("press enter to continue")
			elif menu2Choice == '4':
				SupprAllGrp()
				raw_input("press enter to continue")
			else:
				continue


		elif menuChoice == '3':
			print "1) List templates"
			print "2) Add templates"
			print "3) Delete template"
			print ""
			menu3Choice = raw_input("Your choice?: ")
			if menu3Choice == '1':
				ListeTemplate()
				raw_input("press enter to continue")
			elif menu3Choice == '2':
				print " Broken function-fix soon"
				#Ajout_Template()
				continue
			elif menu3Choice == '3':
				SupprTeampl()
				raw_input("press enter to continue")
			else:
					continue

		elif menuChoice == '4':
			print "1) List landing pages"
			print "2) Add a landing page"
			print ""
			menu4Choice = raw_input("Your choice?: ")
			if menu4Choice == '1':
				ListeLanding()
				raw_input("press enter to continue")
			elif menu4Choice == '2':
				Ajout_Landing()
				raw_input("press enter to continue")
			else:
				continue
		   		
		elif menuChoice == '5':
			print "1) List sender"
			print "2) Add sender"
			print "3) Delete sender"
			print ""
			menu5Choice = raw_input("Your choice?: ")
			if menu5Choice == '1':
				ListeSender()
				raw_input("press enter to continue")
			elif menu5Choice == '2':
				Ajout_SMTP()
				raw_input("press enter to continue")
			elif menu5Choice == '3':
				SupprSMTP()
				raw_input("press enter to continue")
			else:
				continue

		elif menuChoice == '6':
			Report()
			raw_input("press enter to continue")
		elif menuChoice == '7':
			break
	
		else:
			continue


main()
