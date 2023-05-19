print('''
---------------------------------------------------------------------------------------------------------
=========================================================================================================                           
					FT_OTP              	                   	    by jfrontel
=========================================================================================================
---------------------------------------------------------------------------------------------------------
''')

# __________________________________________ DESCRIPCION ________________________________________________ #
'''
ft_opt permite registrar una clave inicial, y es capaz de generar una nueva contraseña cada vez que se solicite. 
 ** Con la opción -g , el programa recibirá como argumento una clave hexadecimal de al menos 64 caracteres. El 
	programa guardará a buen recaudo esta clave en un archivo llamado ft_otp.key, que estará cifrado.
 ** Con la opción -k, el programa generará una nueva contraseña temporal y se mostrará en la salida estándar
'''
# ___________________________________________ LIBRERIAS _________________________________________________ #

import hmac, base64, struct, hashlib, time
import argparse
import sys
from cryptography.fernet import Fernet

# _______________________________________  MENÚ DE ARGUMENTOS  ___________________________________________ #
# ft_get_argument() tomará los argumentos de entrada del programa ft_otp

def process_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--opt_g', type=str, default=None)
	parser.add_argument('-k', '--opt_k', type=str, default=None)
	args = parser.parse_args()
	return args
# ___________________________________________  HOPT y TOTP  ______________________________________________ #
# HOPT (HMAC-based One-Time Password), contraseña de un solo uso basada en eventos: basada en el algoritmo criptográfico HMAC 
# y depende de dos tipos de información. El primero es la clave secreta llamada “inicialización” la cual solo conoce el token y el 
# servidor que valida los códigos OTP enviados. el segundo es el factor móvil, que es un contador almacenado en el token y el servidor. 
# El contador del token incrementa al pulsar el botón del token, mientras que el contador del servicio solo se incrementa cuando se valida correctamente una OTP.

# TOPT (Time-based One-Time Password), contraseña de un solo uso basada en tiempo: Está inspirada en la anterior, HOTP, 
# pero su factor móvil es el tiempo en lugar de un contador. TOPT emplea tiempo en incrementos llamado “timestep” (30 seg). 
# De esta forma, cada OTP será válida mientras dura el “timestep”

def get_hotp_token(secret, timestep):
	'''Con la ayuda del base64.b16decode() método, podemos decodificar la cadena binaria usando alfabetos base16 en forma normal.
		Sintaxis: base64.b32decode(b_string). Retorno: Devuelve la cadena decodificada.'''
	key = base64.b32encode(secret)
	#decoding our key:
	print(f'key = {key}')
	'''Este módulo convierte entre valores de Python y estructuras C representadas como bytesobjetos de Python. 
Las cadenas de formato compacto describen las conversiones previstas a/desde valores de Python. 
struct.pack(format, v1, v2, ...) Devuelve un objeto de bytes que contiene los valores v1 , v2... empaquetados de acuerdo con el formato de cadena de formato. 
Los argumentos deben coincidir exactamente con los valores requeridos por el formato. >Q - entero largo largo; >I entero''' 
	msg = struct.pack(">Q", timestep)
	print(f'msg = {msg}')
	h = hmac.new(key, msg, hashlib.sha1).digest()
	print(f'hmac_new = {h}')
	o = o = h[19] & 15  # Operación AND entre '0b????' y '0b1111'
	print(f'o = {o}')
	#Generate a hash using both of these. Hashing algorithm is HMAC
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000  # '[0]' porque 'struct.unpack' devuelve una lista
	print(f'h = {h}')
	#unpacking
	return h

def get_totp_token(secret):
# Obtener tiempo cada intervalo de 30 segudos
	timestep = int((time.time())//30)
	pass_temp = str(get_hotp_token(secret, timestep))
# Bucle: colocar ceros delante del numero si este no tiene seis cifras
	while len(pass_temp)!=6:
		pass_temp +='0'
	return pass_temp

def opt_g():
	with open(sys.argv[2], 'rb') as file:
		init_key = file.read()
	hex_key = int(init_key, 16)
	hex_key = str(init_key)
	if len(hex_key) < 64:
		print("./ft_otp: error: key must be 64 hexadecimal characters.")
		return
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
		print(master_key)		
	except:
		print("Error: no se ha podido obtener la master_key")
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