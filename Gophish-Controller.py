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


##########################
#    Fonctions d'ajout   #
##########################



def Ajout_Template():
##Ne pas utiliser c'est cassé
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
	nb_grp = int(config.get('Groups','Nb_groups'))
	inputcsv = config.get('Groups','csvinput')
	print "Veuillez saisir le nom du nouveau groupe, attention, gophish n'accepte pas les doublons dans les noms de groupes "
	
	Grps_solo = []
	Grp_Targets = []
	for i in range(nb_grp):
		grpname = 'Groupe ' + 'i'
		Grps_solo.append(grpname)
		Grp_Targets.append([])
		
	cr = csv.DictReader(open(inputcsv,"rb"))
						
	for row in cr:
		x = User(first_name=row['first_name'],last_name=row['last_name'],email=row['email'],position=row['position'])
		grp_to_update = random.choice(range(nb_grp))
		Grp_Targets[grp_to_update].append(x)
		
	for i in range(nb_grp)					
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


def select_campaign_options():
#Initialisation des differents parametres

	#initialisation de la table de dates
	datecamp = []
	f = open('dates','r')
	for i in f.readlines():
		datecamp.append(i.rstrip())

	#Selection de tous les senders
	senders = []
	for smtp in api.smtp.get():
		senders.append(str(smtp.name))
		
	#Selection de tous les templates
	templates = []
	for template in api.templates.get():
		templates.append(str(template.name))

	#Selection de toutes les pages de garage
	parking = []
	for pages in api.pages.get():
		parking.append(str(pages.name))

	groupselect = []
	for groups in api.groups.get():
		groupselect.append(str(groups.name))

	options = [datecamp,senders,templates,parking,groupselect]
	print options
	return options

def AjouTCampagne_Association_sender_template(options):
#Initialisation des differents parametres
	urlph = config.get('Campaigns','urlph')

	for i in range(len(options[4])):
		date = options[0][i]
		groupe = [Group(name=options[4][i])]

		emet = random.choice(options[1])
		  
		emetswap = emet.split()

		for template in options[2]:
			templateswap = template.split()
			if templateswap[0] == emetswap[0]:
				templateuse = template
			else:
				continue

		garage = random.choice(options[3])
			

		finemet = SMTP(name=emet)
		fintemplate = Template(name=templateuse)
		fingarage = Page(name=garage)
		name = date + ' ' + groupe + ' ' +  sender + ' ' + template

		campaign  = Campaign(name=name, groups=groupe, page=fingarage,template=fintemplate, smtp=finemet, url=urlph, launch_date=date) 
		campaign = api.campaigns.post(campaign)

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

	print'============================================================================================================'	
	print'  ____  ___  ____  _   _ ___ ____  _   _        ____ ___  _   _ _____ ____   ___  _     _     _____ ____    '
	print' / ___|/ _ \|  _ \| | | |_ _/ ___|| | | |      / ___/ _ \| \ | |_   _|  _ \ / _ \| |   | |   | ____|  _ \   '
	print'| |  _| | | | |_) | |_| || |\___ \| |_| |_____| |  | | | |  \| | | | | |_) | | | | |   | |   |  _| | |_) |  '
	print'| |_| | |_| |  __/|  _  || | ___) |  _  |_____| |__| |_| | |\  | | | |  _ <  |_| | |___| |___| |___|  _ <   '
	print' \____|\___/|_|   |_| |_|___|____/|_| |_|      \____\___/|_| \_| |_| |_| \_|\___/|_____|_____|_____|_| \_\  '
	print''
	print'============================================================================================================'	



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

	menuChoice = raw_input( "Que voulez-vous faire? ")
	return menuChoice

def main():
	attr_mod = config.get('Campaigns','Attr_mod')	
	ch = config.get('Groups','attr_grp')
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
				if attr_mod == 'manuel':
					Ajout_Campagne_Manuel(select_campaign_options())

				elif attr_mod == 'auto':
					Ajout_campagne_random_association(select_campaign_options())

				elif attr_mod == 'tag':
					AjouTCampagne_Association_sender_template(select_campaign_options())

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
				if ch == 'random':
					Ajout_Groupe_Random()
				if ch =='localisation':
					Ajout_Groupe_Pos()

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
				print "fonction cassée fix soon"
				#Ajout_Template()
				continue
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
			else:
				continue

		elif menuChoice == '6':
			Report()

		elif menuChoice == '7':
			break
	
		else:
			continue


main()
