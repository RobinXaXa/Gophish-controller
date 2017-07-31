# Gophish-controller

Here's a little script I created to take control over gophish via the python API client.

This script is for you if you wish to automate the campaign and groups creation process:

- Groups: There's a group creation mode based on CSV import with a special feature: Localisation mode, with the basic CSV integration you can just bulk import a CSV into gophish. with this script you can add a "location" row into yout csv. By stating how many groups you ant to create, this script will sort the users into all the groups and will try to have the fewer member with the same location in the same groups. The created groups will also be equal in terms of number of members.

- Campaigns: Campaign creation will also be a lot faster with a system of tags which is more detailed on the github wiki !


for instalation: you just have to clone the repo and fill gophish.ini

This script was created to test user awareness in corporations. 
it's not meant to send large spear-phishing campaigns (but it can do that ;) tested and approved with BeEF to handle link clicked and Metasploit or Empire Framwork to handle malicious macros sent with atachments - let the shell rain)

I'm curently working on this project to improove my skills in python so don't hesitate to open an issue if you awnt me to devellop a new feature.

Contributors are also welcomed !
