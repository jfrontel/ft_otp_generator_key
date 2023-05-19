print('''
--------------------------------------------------------------------------------------------------------------
==============================================================================================================                           
							FT_OTP              	                   by jfrontel
==============================================================================================================
--------------------------------------------------------------------------------------------------------------
''')

# __________________________________________ DESCRIPCION ____________________________________________________ #

'''ft_opt permite registrar una clave inicial, y es capaz de generar una nueva contraseña cada vez que se solicite. 
-- Con la opción -g , el programa recibirá como argumento una clave hexadecimal de al menos 64 caracteres. 
	El programa guardará a buen recaudo esta clave en un archivo llamado ft_otp.key, que estará cifrado en todo momento.
-- Con la opción -k, el programa generará una nueva contraseña temporal y la mos- trará en la salida estándar. ...]'''


# ____________________________________________ LIBRERIAS ___________________________________________________ #

import hmac, base64, struct, hashlib, time
import argparse
import sys, os, re
from cryptography.fernet import Fernet

# _______________________________________  MENÚ DE ARGUMENTOS  _____________________________________________ #
# ft_get_argument() tomará los argumentos de entrada del programa ft_otp

def process_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--opt_g', type=str, default=None)
	parser.add_argument('-k', '--opt_k', type=str, default=None)
	args = parser.parse_args()
	return args
# __________________________________________  HOPT y TOTP  _________________________________________________ #
# HOPT (HMAC-based One-Time Password), contraseña de un solo uso basada en eventos: basada en el algoritmo criptográfico HMAC 
# y depende de dos tipos de información. El primero es la clave secreta llamada “inicialización” la cual solo conoce el token y el 
# servidor que valida los códigos OTP enviados. el segundo es el factor móvil, que es un contador almacenado en el token y el servidor. 
# El contador del token incrementa al pulsar el botón del token, mientras que el contador del servicio solo se incrementa cuando se valida correctamente una OTP.

# TOPT (Time-based One-Time Password), contraseña de un solo uso basada en tiempo: Está inspirada en la anterior, HOTP, 
# pero su factor móvil es el tiempo en lugar de un contador. TOPT emplea tiempo en incrementos llamado “timestep” (30 seg). 
# De esta forma, cada OTP será válida mientras dura el “timestep”

def get_hotp_token(master_key, timestep):
	hmac_sha1 = hmac.new(master_key, timestep.encode(), "sha1")
	hmac_sha1 = hmac_sha1.hexdigest()
	offset = int(hmac_sha1[39], 16)
	pass_temp = hmac_sha1[offset*2:offset*2 + 8]
	pass_temp = str(int(pass_temp[0], 16) & 0x7) + pass_temp[1:]
	pass_temp = int(pass_temp, 16)
	pass_temp = str(pass_temp%(10**6))
	while len(pass_temp)!=6:
		pass_temp +='0'
	return pass_temp

def get_totp_token(master_key):
	timestep = str(time.time() // 30) # Obtener timestep cada periodo de 30 segundos
	pass_temp = str(get_hotp_token(master_key, timestep))
	while len(pass_temp) != 6: #Coloca ceros delante hasta que el numero tenga 6 cifras
		pass_temp += '0'
	return pass_temp

def opt_g():
	with open(sys.argv[2], 'rb') as file:
		init_key = file.read()
	hex_key = int(init_key, 16)
	hex_key = str(init_key)
	key = Fernet.generate_key()
	with open("key.key", "wb") as a:
		a.write(key)
	key = Fernet(key)
	with open("ft_otp.key", "wb") as f:
		f.write(key.encrypt(hex_key.encode()))
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


if __name__ == "__main__":
	args = process_arguments()
	if args.opt_g == None and args.opt_k  == None or args.opt_g != None and args.opt_k != None:
		print("ERROR. Introduzca <./ft_otp [-gk]> o -help para más ayuda")
		exit()	
	if args.opt_g != None:
		opt_g()
	elif args.opt_k != None:
		opt_k()
