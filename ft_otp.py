print('''
--------------------------------------------------------------------------------------------------------------
==============================================================================================================                           
							FT_OTP              	                   by jfrontel
==============================================================================================================
--------------------------------------------------------------------------------------------------------------
''')

# ____________________________________________ DESCRIPCION ____________________________________________________ #

'''ft_opt permite registrar una clave inicial, y es capaz de generar una nueva contraseña cada vez que se solicite. 
-- Con la opción -g , el programa recibirá como argumento una clave hexadecimal de al menos 64 caracteres. 
	El programa guardará a buen recaudo esta clave en un archivo llamado ft_otp.key, que estará cifrado en todo momento.
-- Con la opción -k, el programa generará una nueva contraseña temporal y la mos- trará en la salida estándar. ...]'''


# ____________________________________________ LIBRERIAS ____________________________________________________ #

import hmac, base64, struct, hashlib, time
import argparse
import sys, os, re
from cryptography.fernet import Fernet

# ________________________________________  MENÚ DE ARGUMENTOS  _______________________________________________ #
# ft_get_argument() tomará los argumentos de entrada del programa ft_otp

def process_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--opt_g', type=str, default=None)
	parser.add_argument('-k', '--opt_k', type=str, default=None)
	args = parser.parse_args()
	return args
# ______________________________________________  HOPT y TOTP  _________________________________________________ #
# HOPT (HMAC-based One-Time Password), contraseña de un solo uso basada en eventos: basada en el algoritmo criptográfico HMAC 
# y depende de dos tipos de información. El primero es la clave secreta llamada “inicialización” la cual solo conoce el token y el 
# servidor que valida los códigos OTP enviados. el segundo es el factor móvil, que es un contador almacenado en el token y el servidor. 
# El contador del token incrementa al pulsar el botón del token, mientras que el contador del servicio solo se incrementa cuando se valida correctamente una OTP.

# TOPT (Time-based One-Time Password), contraseña de un solo uso basada en tiempo: Está inspirada en la anterior, HOTP, 
# pero su factor móvil es el tiempo en lugar de un contador. TOPT emplea tiempo en incrementos llamado “timestep” (30 seg). 
# De esta forma, cada OTP será válida mientras dura el “timestep”

def get_hotp_token(secret, timestep):
	key = base64.b32encode(secret)
	print(f'Introducir en checker: {str(key.decode())}')
	msg = struct.pack(">Q", timestep)
	h = hmac.new(key, msg, hashlib.sha1).digest() #Generar hash a partir de clave secreta y timestep
	o = o = h[19] & 15  # Operación AND entre '0b????' y '0b1111'
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000  # '[0]' porque 'struct.unpack' devuelve una lista
	return h

def get_totp_token(secret):

	timestep = int((time.time())//30) 	# Obtener tiempo cada intervalo de 30 segudos
	pass_temp = str(get_hotp_token(secret, timestep))
	pass_temp = pass_temp.zfill(6) # coloca ceros delante del numero si este no tiene seis cifras
	return pass_temp


# __________________________________________  VALIDACION DE ARCHIVO  _____________________________________________ #
# Comprueba que el fichero existe y es legible con permiso de lectura

def ft_file_ok():
	file = args.opt_g
	if not (os.path.isfile(file) or os.access(file, os.R_OK)):
		return 0
	return 1

# ___________________________________________  LOGICA DEL PROGRAMA  ______________________________________________ #

def opt_g():
	with open(sys.argv[2], 'r') as file:
		key_hex_str = file.read()
	if ft_file_ok() == 0:
		print("ERROR: el fichero dado no existe o no tiene permiso de lectura.")

	if not re.match(r'^[0-9a-fA-F]{64,}$', key_hex_str):
		print("Error, you must set an hexadecimal password of 64 characters or more")
		exit()
	hex_key_bytes = bytes.fromhex(key_hex_str)
	key = Fernet.generate_key()
	with open("key.key", "wb") as a:
		a.write(key)
	key = Fernet(key)
	with open("ft_otp.key", "wb") as f:
		f.write(key.encrypt(hex_key_bytes))
	print("La clave fue encryptada con exito en ft_otp.key")
		
def opt_k():
	try:
		with open("key.key", "rb") as f:
			key = f.read()
		key = Fernet(key)
		with open(sys.argv[2], "rb") as f:
			master_key = f.read()
		master_key = key.decrypt(master_key)	
	except:
		print("Error: (open) can't obtain master key")
		return
	pass_temp = get_totp_token(master_key)
	print(pass_temp)


# __________________________________________________  MAIN  _______________________________________________________ #

if __name__ == "__main__":
	args = process_arguments()
	if args.opt_g == None and args.opt_k  == None or args.opt_g != None and args.opt_k != None:
		print("ERROR. Introduzca <./ft_otp [-gk]> o -help para más ayuda")
		exit()	
	if args.opt_g != None:
		opt_g()
	elif args.opt_k != None:
		opt_k()
