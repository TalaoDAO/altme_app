import socket

class currentMode() :
	def __init__(self, myenv):
		self.admin = 'thierry.thevenet@talao.io'
		self.myenv = myenv
	
		# En Prod chez AWS 
		if self.myenv == 'aws':
			self.sys_path = '/home/admin'
			self.server = 'https://app.altme.io/'
			self.IP = '18.190.21.227' 
		elif self.myenv == 'local' :
			self.sys_path = '/home/thierry'
			self.server = 'http://' + extract_ip() + ':15000/'
			self.IP = extract_ip()
			self.port = 15000
		else :
			print('environment variable problem')
			exit()
		print('mode server = ', self.server)
		self.help_path = self.sys_path + '/altme/templates/'


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP
