# -*- coding: utf-8 -*-
from gophish import Gophish
from gophish.models import *
import csv
import dateutil
from datetime import datetime,timedelta
import random
import base64
import sys
import os

api_key=''
api = Gophish(api_key)



#######################
#Fonctions de Listing #
#######################
def ListeCampagne():
	for campaign in api.campaigns.get():
                print "Id: ", campaign.id, " Nom: ", campaign.name

def ListeGroupe():
	for groups in api.groups.get():
		print "Id: ",groups.id," Nom: ",groups.name

def ListeSender():
	for smtp in api.smtp.get():
		print "Id: ",smtp.id," Nom: ",smtp.name

def ListeTemplate():
	for template in api.templates.get():
		print "Id: ",template.id," Nom: ", template.name

def ListeLanding():
	for page in api.pages.get():
		print "Id: ", page.id," Nom: ", page.name

##########################
#Fonctions de suppression#
##########################
def SupprCamp():
	print " Voici la liste des campagnes existantes:"
	ListeCampagne()
	camp = raw_input("Quel est la campagne à supprimer ? (id) ")
	delete = api.groups.delete(camp)
def SupprGrp():
	print " Voici une liste des groupes existants:"
	ListeGroupe()
	grp = raw_input("Quel est le groupe a supprimer ? (id) ")
	delete = api.groups.delete(grp)

def SupprTempl():
	print " voici une liste des tempaltes existants:"
	ListeTemplate()
	templ = raw_input("Quel est le groupe a supprimer ? (id) ")
	delete = api.templates.delete(templ)

def SupprSMTP():
	print " voici une liste des senders existants:"
	ListeSender()
	snd = raw_input("quel est le sender a supprimer ? (id) ")
	delete = api.smtp.delete(snd)

def SupprAllGrp():
	print "[*] Purge des groupes..."
	for group in api.groups.get():
			api.groups.delete(group.id)
	print "[*] Groupes purgés"

#########################
#    Fonctions d'ajout   #
##########################


##Ne pas utiliser c'est cassé
def Ajout_Template():
	print "Quel nom nouslez-vous donner à votre Template?"
	n = raw_input("Nom: ")
	print "Quel Objet voulez vous choisir pour votre template?"
	o = raw_input("Objet?: ")
	print "utilisez vous du text(0) ou du html(1) pour le corps de votre message?"
	choix = raw_input("Choix: 0 ou 1 ?: ")
	if choix == '0':
		print "veuillez saisir le corps de votre message (format texte)"
		text = raw_input("Texte: ")
		html = ""
	elif choix == '1':
		print "veuillez saisir le corps de votre message (format html)"
		text = ""
		html = raw_input("HTML: ")

### Probleme sur la fonction de parsing interne a Gophish creant un bug
### sur les pieces jointes meme si on en envoie pas

	print "Voulez-vous inserer une piece jointe dans le mail? (0 ou 1)"
	choix = raw_input("0 ou 1")
	Attachments = []
	if choix == '1':
		npj = raw_input("Veuillez saisir le nom de la piece jointe: ")
		tpj = raw_input("veuillez saisir le type du fichier: ")
		cpj = raw_input("veuillez saisir le chemin vers le fichier a attacher: ")   
		with open(cpj, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read())
		objAtt = Attachment(name=npj,type=tpj,content=encoded_string)
		Attachments.append(objAtt)

	template = Template(name=n, subject=o, text=text, html=html,attachments=Attachments)
	template = api.templates.post(template)
				


def Ajout_SMTP():
	print "Quel nom nouslez-vous donner à votre nouvel emmeteur?"
	n = raw_input("Nom: ")
	print "Quelle est l'adresse qui doit envoyer le mail ?"
	f_a = raw_input ("Adresse: ")
	print "Veuillez saisir l'adresse du serveur SMTP d'envoi."
	h = raw_input ("Serveur: ")
	print "votre serveur SMTP demande t'il des i nformations de connexion?"
	resp = raw_input("0 ou 1?: ")
	if resp == 1:
		print "veulliez sasir le login"
		usrn = raw_input ("username?: ")
		print "veuillez saisir le mot de passe"
		pwd = raw_inpur ("password?: ")
	else:
		usrn=""
		pwd=""
		smtp = SMTP(name=n, from_address=f_a, host=h, username=usrn, password=pwd)
	smtp = api.smtp.post(smtp)

def Ajout_Landing():
	print "Quel nom nouslez-vous donner à votr nouvelle page de renvoi?"
	n = raw_input("Nom: ")
	print "Veuillez saisir le code HTML de la page"
	html = raw_input("Code HTML: ")
	page = Page(name=n,html=html)
	page = api.pages.post(page)


def Ajout_Groupe_solo():

	##Reader-normal
	#cr = csv.reader(open("Groupe 0.csv","rb")) Targets = [] for row
	#in cr:
	#		   print "%s %s %s %s" %(row[0],row[1],row[2],row[3]) x =
	#User(first_name=row[0],last_name=row[1],email=row[2],position=row[3])
	#Targets.append(x) 
							
	#dictreader
	inputcsv = raw_input("Veuillez sasir le chemin absolu du fichier CSV à traiter: ")
	print "Veuillez saisir le nom du nouveau groupe, attention, gophish n'accepte pas les doublons dans les noms de groupes "
	grpname = raw_input("Nom?: ")
	cr = csv.DictReader(open(inputcsv,"rb"))
	Targets = []
								
	for row in cr:
		#print "%s %s %s %s" %(row['first_name'],row['last_name'],row['email'],row['position'])
		x = User(first_name=row['first_name'],last_name=row['last_name'],email=row['email'],position=row['position'])
		Targets.append(x)
								
	groups = Group(name=grpname, targets=Targets)
	group = api.groups.post(groups)

def Ajout_Groupe_Pos():

	nb_days = int(raw_input("sur combien de jours ouvrés va se dérouler la camgne ?: "))
	#Nous avions dit deux campagnes par jour
	nb_grp = (nb_days*2)
	print range(nb_grp)


	#initialisation des dicos
	csvinput = raw_input("Sasisez le chemin absolu de votre fichier csv: ")
	
	GrpTargets=[]
	Targets=[]
	Repartition_groupes=[]
	
	cr = csv.DictReader(open(csvinput,"rb"))
	
	##Initialisation des dictionnaires
	for i in range(nb_grp):
		#print ("groupe"+str(i))
		GrpTargets.append("groupe"+str(i))
		GrpTargets[i] = list()
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
								
		groups = []		
	for z in range(nb_grp):
		print ("voici la composition du groupe: ", z)
		print Repartition_groupes[z]
		print "=========================================================================="
		   
		group = Group(name="groupe"+str(z), targets=GrpTargets[z])
		group = api.groups.post(group)
				
		groups.append([Group(name="groupe"+str(z))])
	return groups

def AjouTCampagne_Association_sender_template():
#Initialisation des differents parametres

	#initialisation de la table de dates
	datecamp = []
	f = open('dates','r')
	for i in f.readlines():
		datecamp.append(i.rstrip())

	#Selection de tous les senders
	senders = []
	for smtp in api.smtp.get():
		senders.append(smtp.name)
	
	#Selection de tous les templates
	templates = []
	for template in api.templates.get():
		templates.append(template.name)
	
	#Selection de toutes les pages de garage
	parking = []
	for pages in api.pages.get():
		parking.append(pages.name)

	groups = Ajout_Groupe_Pos() 

	for i in range(len(groups)):
		date = datecamp[i]
		groupe = groups[i]
		emet = senders[i] 
		emetswap = emet.split()
		for template in templates:
			templateswap = template.split()
			
			if templateswap[0] == emetswap[0]:
				templateuse = template
			else:
				continue

		garage = random.choice(parking)
		urplph = 'http://vmprdssiappb1.tf1.fr:8062' 
		finemet = SMTP(name=emet)
		fintemplate = Template(name=templateuse)
		fingarage = Page(name=garage)
		name = date + ' ' + groupe + ' ' +  sender + ' ' + template

		campaign  = Campaign(name=name, groups=groupe, page=fingarage,template=fintemplate, smtp=finemet, url=urlph, launch_date=date) 
		campaign = api.campaigns.post(campaign)
				
def AjoutCampagneFullAuto():
	#Selection des groupes
	print "Nous allons commencer par selectionner les groupes auquels les mails seront envoyés:"
	ch = raw_input("voulez vous utiliser des groupes existants: 0, ou créer automatiquement des groupes: 1 ?")
	if ch == '0':
		groups=[]
		print "voici la liste des groupes existants: "
		ListeGroupe()
		groupselec = []
		nbgrpman = raw_input("combien de groupes voulez-vous selectionner ?: ")
		for i in range(int(nbgrpman)):
			g = raw_input("veuillez entrer le nom du groupe a ajouter: ")
			groupselec.append(g)
								
		for i in range(int(nbgrpman)):
			groups.append([Group(name=groupselec[i])])
						
	elif ch == '1':
		groups = Ajout_Groupe()
	print ""
	print "groupes choisis"
	print "===================================================================================="
		
		
	#initialisation de la table de dates
	datecamp = []
	print ("Veuillez saisir le chemin absolu de votre fichier de dates. pour la campagne en cours votre fichier doit contenir: ",len(groups), " dates.")
	dates = raw_input("fichier?: ")
	f = open(dates,'r')
	for i in f.readlines():
		datecamp.append(i.rstrip())
	datecamp.remove ('')

	#Selection des Senders (tous par default)
	senders = []
	for smtp in api.smtp.get():
		senders.append(smtp.name)
	
	#Selection des Templates (tous par default)
	templates = []
	for template in api.templates.get():
		templates.append(template.name)

	#Selection des pages de parking
	parking = []
	for pages in api.pages.get():
		parking.append(pages.name)
	urlph = raw_input("Veuillez saisir l'adresse du tracker gophish: ")

#Affectation emmeteur/template/pages de parking aléatoire ou manuelle
	automatchoice =  raw_input("voulez-vous affecter les elements de campagne manuellement ou aléatoirement? 0: auto , 1: manuel, 2:semi-auto association sender/template" )
	if automatchoice == '0':
		for i in range(len(groups)):
                	print "Voici les element de la campagne: "

			name = "test" + str(i)
			print "le nom de la campagne est: ",name
			date = datecamp[i]
			print "date: ", date

			groupe = groups[i]
			print "groupe: ",groupe

			sender0 = str(random.choice(senders))
			print "l'emmeteur des mails sera: ",sender0
			sender = SMTP(name=sender0)
			template0 = str(random.choice(templates))
			print "le template utilisé pour cette campagne est: ",  template0
			template = Template(name=template0)

			garage0 = str(random.choice(parking))
			print "la page de parking utilisée pour cette campagne est: ",garage0
			garage = Page(name=garage0)
			print "l'url de tracking est: ",urlph
			print ""
			print ""
	        	campaign  = Campaign(name=name, groups=groupe, page=garage,template=template, smtp=sender, url=urlph, launch_date=date) 
	        	campaign = api.campaigns.post(campaign)
				
	elif automatchoice == '1':
		for i in range(len(groups)):
			print "Saisie les element de la campagne: ", i
			print ""
			groupe = groups[i]
			print "Le groupe utilisé pour cette campage sera: ", groupsele[i]
			print ""
			name = raw_input("veuillez saisir le nom de la campagne: ")
			date = datecamp[i]
			print ""
			print senders
			sender0 = raw_input("veuillez sasir l'expetieur qui sera associé à la campagne: ")
			sender = SMTP(name=sender0)
			print ""
			print templates
			template0 = raw_input("veuillez sasir le template qui sera associé à la campagne: ")
			template = Template(name=template0)
			print""
			print parking
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

        elif automatchoice == '2':
                AjouTCampagne_Association_sender_template()

###########################################################################################################
# Premiere tentative d'automatiqation complete TODO: passer les principaux parametres via un fichier .ini #
###########################################################################################################

def Automation():
	inputcsvs = os.listdir('/data/extracted_users')
	for inputcsv0 in inputcsvs:
		Camp_full_auto(imp_grp_by_pos_auto(inputcsv0))

def Camp_full_auto(groups):
	#Selection des Senders (tous par default)
	senders = []
	for smtp in api.smtp.get():
		senders.append(smtp.name)
		#Selection des Templates (tous par default)
	templates = []
	for template in api.templates.get():
		templates.append(template.name)
	#Selection des pages de parking
	parking = []
	for pages in api.pages.get():
		parking.append(pages.name)
	for i in range(len(groups)):
		name = "grp" + str(i)
		groupe = groups[i]
		urlph = 'http://XXX.XXX.XXX.XXX'
		sender0 = str(random.choice(senders))
		sender = SMTP(name=sender0)
		template0 = str(random.choice(templates))
		template = Template(name=template0)
		garage0 = str(random.choice(parking))
		garage = Page(name=garage0)
		campaign  = Campaign(name=name, groups=groupe, page=garage,template=template, smtp=sender, url=urlph)
		campaign = api.campaigns.post(campaign)

def imp_grp_by_pos_auto(csvinput0):

	nb_grp = 4
	print range(nb_grp)
	#initialisation des dicos
	csvinput = "/data/extracted_users/" + str(csvinput0)
	GrpTargets=[]
	Targets=[]
	Repartition_groupes=[]
	cr = csv.DictReader(open(csvinput,"rb"))
	##Initialisation des dictionnaires
	for i in range(nb_grp):
		#print ("groupe"+str(i))
		GrpTargets.append("groupe"+str(i))
		GrpTargets[i] = list()
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

		Repartition_grpes[grp_to_update][curloc]+=1
		y = User(first_name=row['first_name'],last_name=row['last_name'],email=row['email'],position=row['position'])
		GrpTargets[grp_to_update].append(y)
	groups = []
	for z in range(nb_grp):
		print ("voici la composition du groupe: ", z)
		print Repartition_groupes[z]
		print "=========================================================================="
		group = Group(name="groupe"+str(z), targets=GrpTargets[z])
		group = api.groups.post(group)
		groups.append([Group(name="groupe"+str(z))])

        return groups

#############
# Reporting #
#############
#necessite GoReport dans le répertoire d'execution du script
# https://github.com/chrismaddalena/GoReport

def Report():
	print "voici la liste des campagnes existantes: "
        ListeCampagne()
        idselec = raw_input("Quel est l'id de la campagne dont vous voulez generer le rapport?: ")
        formatselec = raw_input("Quel est le format de sortie désiré?: quick, word, csv: ")
        string = 'python GoReport.py' + ' --id ' + str(idselec) + ' --format ' + str(formatselec)

        print string
        os.system(string)

##################
# Banner et menu #
##################
def banner():
	print"==============================================="
        print"  ____  ___  ____  _   _ ___ ____  _   _       "   
        print" / ___|/ _ \|  _ \| | | |_ _/ ___|| | | |"
        print"| |  _| | | | |_) | |_| || |\___ \| |_| |"
        print"| |_| | |_| |  __/|  _  || | ___) |  _  |"
        print" \____|\___/|_|   |_| |_|___|____/|_| |_|"
        print"                                               "
	print"==============================================="

def menu():
	print ""
	print "1)Gestion des campagnes"
	print "2)Gestion des groupes et utilisateurs"
	print "3)Gestion des modeles d'email"
	print "4)Gestion des pages de parking"
	print "5)Gestion des emmeteurs"
       	print "6)Reporting"
	print "7)Quitter"
	print "======================================================================="
	print ""

	menuChoice = raw_input( "Que voulez-vous faire?(saisir un nombre entre 1 et 5): ")
	return menuChoice

def main():
	if len(sys.argv) <=1:
		while 1:
			banner()
			menuChoice = menu()
			if menuChoice == '1':
				print "1)Lister les campagnes existantes"
				print "2)Creation de campagne"
				print "3)Création de campgne lien emmeteur/tempalte"
				print "4)Supprimmer une campagne"
                                print ""
				menu1Choice = raw_input("Votre choix?: ")
				if menu1Choice == '1':
					ListeCampagne()
				elif menu1Choice == '2':
					AjoutCampagneFullAuto()
                                elif menu1Choice == '3':
                                        SupprCamp()
			        else:
                                        continue
		
			elif menuChoice == '2':
				print "1)Lister les groupes existants"
				print "2)Ajouter un/des groupes"
				print "3)Supprimer un groupe"
				print "4) Purger les groupes"
				print ""
				menu2Choice = raw_input("Votre choix?: ")
				if menu2Choice == '1':
					ListeGroupe()
				elif menu2Choice == '2':
					Ajout_Groupe()
				elif menu2Choice == '3':
					SupprGrp()
				elif menu2Choice == '4':
					SupprAllGrp()
				else:
        		                continue
		
		
			elif menuChoice == '3':
				print "1)Lister les templates de mails existants"
				print "2)Ajouter un template"
				print "3)Supprimer un template"
				print ""
				menu3Choice = raw_input("Votre choix?: ")
				if menu3Choice == '1':
					ListeTemplate()
				elif menu3Choice == '2':
					Ajout_Template()
				elif menu3Choice == '3':
					SupprTeampl()
				else:
					continue
		
			elif menuChoice == '4':
				print "1)Lister les pages de renvoi existantes"
				print "2)Ajouter une page de renvoi"
				print ""
				menu4Choice = raw_input("Votre choix?: ")
				if menu4Choice == '1':
					ListeLanding()
				elif menu4Choice == '2':
					Ajout_Landing()
				else:
					continue
				   		
			elif menuChoice == '5':
				print "1)Lister les emmeteurs de mails existants"
				print "2)Ajouter un emmeteur"
				print "3)Supprimmer un emmeteur"
				print ""
				menu5Choice = raw_input("Votre choix?: ")
				if menu5Choice == '1':
					ListeSender()
				elif menu5Choice == '2':
					Ajout_SMTP()
				elif menu5Choice == '3':
					SupprSMTP()		

                        elif menuChoice == '6':
				Report()
                        elif menuChoice == '7':
                                break
				
			else:
				continue
	elif sys.argv[1] == '-k':
		Automation()
				
main()
