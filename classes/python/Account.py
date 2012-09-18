## This class holds account information 
class Account():
	## initializer for account class
	def __init__(self, username, apikey, catalog):
		self.username = username
		self.apikey = apikey

	## returns information about the account
	def info():
		return (self.username, self.apikey)
	
	## print information about the account
	def __str__():
		print "Username: %s, apikey: %s" % (self.username, self.apikey)