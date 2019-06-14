#Take UF credentials and navigate to one UF > register/schedule > {semester} > download to my calendar
import mechanize


USERNAME = ""
PASSWORD = ""
URL = 'https://login.ufl.edu/idp/profile/SAML2/Redirect/SSO?execution=e1s1'


br = mechanize.Browser()
 
br.set_handle_robots(False)   
br.set_handle_refresh(False)

br.addheaders = [('User-agent', 'Firefox')]

response = br.open(URL)

print(response)
