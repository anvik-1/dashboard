import datetime
import random
import secrets

class ad_functions:
   
    def get_properties(self, ucnetid):
        '''Retrieve AD user property'''
        command = f'Get-ADUser -Identity "{ucnetid}" -Properties *'
        return (command)
    
    def enable_user(self, ucnetid, action="Enable"):
        """'Enable' to enable the user account,'Disable' to disable the user account"""
        command = f"{action}-ADAccount -Identity {ucnetid}"
        status = f"Get-ADUser -Identity {ucnetid}"
        return (command, status)
    
    def random_password(self):
        password_length = random.randint(8, 15)
        password = secrets.token_urlsafe(password_length)
        return password
    
    def create_user(self, usercreation):
        global domaincontroller 
        domaincontroller = "DC=uci,DC=edu"
        ou = f"OU={usercreation["OU"]},OU=Users"
        password = self.random_password()
        command = f"new-aduser -givenname '{usercreation["firstname"]}' -surname {usercreation["lastname"]} -SamAccountName {usercreation["ucnetid"]} -userprincipalname {usercreation["ucnetid"]} -path '{ou},{domaincontroller}'-desc 'account created on {datetime.datetime.now()} {usercreation["description"]}' -AccountPassword (ConvertTo-SecureString {password} -AsPlainText -force) -passThru -name '{usercreation["firstname"]} {usercreation["lastname"]}' -Enabled $True"
        status = f"Get-ADUser -Identity {usercreation["ucnetid"]}"
        return (command, status)
    
    def kerberos_name_mapping(self, usercreation):
        command = f"Set-ADUser '{usercreation["ucnetid"]}' -Add @{{'altSecurityIdentities'='Kerberos:{usercreation["ucnetid"]}@UCI.EDU'}}"
        status = f"Get-ADUser -Identity {usercreation["ucnetid"]}"
        return (command, status)
    
    def create_computer(self, computer_name, computer_type):
        laptop_ou = 'OU=Laptops'
        computer_ou = 'OU=Computers'
        if computer_type == 'Laptop':
            computer_type = laptop_ou
        else:
            computer_type = computer_ou
        command = f"New-ADComputer -Name '{computer_name}' -SamAccountName '{computer_name}' -Path '{computer_type}'"
        status = f"Get-ADComputer -Identity '{computer_name}' -Properties *"
        return (command, status)

    def get_computer_properties(self, computer_name):
        '''Retrieve computer property'''
        command = f"Get-ADComputer -Identity '{computer_name}' -Properties *"
        return (command)
    
    def wildcard(self, filter_string):
        command = f"Get-ADComputer -Filter \"Name -like '*{filter_string}*'\" | select -expand Name"
        return command
