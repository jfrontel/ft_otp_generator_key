# ft_otp_generator_key
ft_otp es un programa que permite registrar una clave inicial, y sea capaz de generar una nueva contraseña cada vez que se solicite.


<h2>Introduccion: Necesidad ft_opt</h2>
<div>
<p>Las 10 peores contraseñas más utilizadas en 2018</p>
<p>1 - 123456 </p>
<p>2 - password </p>
<p>3 - 123456789 </p>
<p>4 - 12345678 </p>
<p>5 - 12345 </p>
<p>6 - 111111 </p>
<p>7 - 1234567</p>
<p>8 - sunshine</p>
<p>9 - qwerty </p>
<p>10 - iloveyou</p>
</div>

<h2> ft_opt: Enunciado </h2>
<p>En el lenguaje de tu elección, debes implementar un programa que permita registrar
una clave inicial, y sea capaz de generar una nueva contraseña cada vez que se solicite.
Puedes utilizar cualquier librería que facilite la implementación del algoritmo, siempre
que no hagan el trabajo sucio, es decir, queda terminantemente prohibido hacer uso de
cualquier librería TOTP. Por supuesto, puedes y debes hacer uso de alguna librería o
función que te permita acceder al tiempo del sistema.</p>
<p>-- El programa deberá llamarse ft_otp.</p>
  
<p>-- Con la opción -g , el programa recibirá como argumento una clave hexadecimal
de al menos 64 caracteres. El programa guardará a buen recaudo esta clave en un
archivo llamado ft_otp.key, que estará cifrado en todo momento.</p>
    
<p>-- Con la opción -k, el programa generará una nueva contraseña temporal y la mos-
trará en la salida estándar.</p>

<h2> Analisis ft_opt</h2>

<h3>Códigos OTP</h3>
<p>Este concepto viene del anglicismo “One-Time Password”, lo que viene a significar una contraseña válida para una autenticación, sesión de inicio
o transacción. Esta una contraseña que se genera dinámicamente y que como su nombre indica sólo puede ser utilizada una vez, a veces durante
un periodo corto de tiempo (minutos o incluso hasta segundos) desde que haya sido generado.</p>

<p>La adopción de las contraseñas de un sólo uso puede ofrecer una alternativa más segura o incluso complementar a una contraseña
estática en un proceso de autenticación multifactor. Su potencial implica que si un atacante llegase a obtener esta contraseña dinámica, no sería
capaz de volverla a utilizar de forma válida en un segundo intento, quedando así el usuario protegido si sus credenciales estáticas hubieran
sido comprometidas por algún mecanismo o ataque.</p>


<h3>Contraseña de un solo uso basada en el tiempo (TOTP)</h3>
<p>La contraseña de un solo uso basada en el tiempo (TOTP) es una forma común de implementar la autenticación de dos factores en las aplicaciones. Funciona solicitando al usuario un token que generalmente se envía en un SMS, correo electrónico o un pase secreto generado al dispositivo del usuario con un tiempo de vencimiento. Compara el token provisto con el token generado real, luego los autentica si los tokens coinciden.</p>

<h3>Cómo funcionan las aplicaciones de autenticación TOTP</h3>
<p>Esencialmente, el proceso de autenticación con autenticadores implica el siguiente procedimiento:</p>

<p>[+]  El sitio web solicita al usuario que proporcione una contraseña de un solo uso generada por la aplicación de autenticación.</p>
<p>[+]  Luego, el sitio web genera otro token utilizando un valor inicial que tanto la aplicación de autenticación como él mismo conocen.</p>
<p>[+]  El sitio web procede a autenticar al usuario si el token recién generado coincide con el token proporcionado por el usuario.</p>

<h3>¿Qué es HMAC (Código de autenticación de mensajes basado en hash)?</h3>

<p>Los HMAC proporcionan al cliente y al servidor una clave privada compartida que solo ellos conocen. El cliente realiza un hash único (HMAC) para cada solicitud. Cuando el cliente solicita el servidor, procesa los datos solicitados con una clave privada y los envía como parte de la solicitud. Tanto el mensaje como la clave se codifican en pasos separados para que sea seguro. Cuando el servidor recibe la solicitud, crea su propio HMAC. Se comparan ambos HMACS y, si ambos son iguales, el cliente se considera legítimo</p>


<h3>Cómo funciona la autenticación de dos factores</h3>
<p>Esencialmente, el proceso de autenticación de dos factores implica el siguiente procedimiento:</p>

<p>[+]__ El usuario se autentica mediante correo electrónico y contraseña (factor de conocimiento).</p>
<p>[+]__ La plataforma confirma la información del usuario y solicita una segunda técnica de autenticación.</p>
<p>[+]__ La plataforma genera una contraseña de un solo uso (OTP) y la envía a un dispositivo al que solo el usuario puede acceder (factor de posesión).</p>
<p>[+]__ El usuario proporciona la OTP recibida a la plataforma, que valida la información y autoriza al usuario.</p>

<p>La clasificación más importante de OTPS puede ser:</p>
<p>• HOPT (HMAC-based One-Time Password), contraseña de un solo uso basada en eventos: está basada en el algoritmo criptográfico
HMAC y depende de dos tipos de información. El primero es la clave secreta llamada “inicialización” la cual solo conoce el token y
el servidor que valida los códigos OTP enviados. el segundo es el factor móvil, que es un contador almacenado en el token y el
servidor. El contador del token incrementa al pulsar el botón del token, mientras que el contador del servicio solo se incrementa
cuando se valida correctamente una OTP.</p>

<p>• TOPT (Time-based One-Time Password), contraseña de un solo uso basada en tiempo: Está inspirada en la anterior, HOTP, pero
su factor móvil es el tiempo en lugar de un contador. TOPT emplea tiempo en incrementos llamado “timestep”, que suele ser
de 30 o 60 segundos. De esta forma, cada OTP será válidamientras dura el “timestep”.</p>

<h3>El algoritmo HTOP</h3>
<p>El algoritmo está basado en un valor de un contador incremental y una clave simétrica estática únicamente conocida por el token (el cual posee
el usuario) y el servicio de validación.</p>
<p>Para generar el valor se usará el algoritmo HMAC-SHA-1, definido por la IETF en el RFC-2104. Normalmente ha sido considerada una función
segura, pero ya en 2004 se dio a conocer un número significante de ataques mediante colisiones contra funciones similares y en 2017
Google anunció [5] que había sido capaz de crear dos ficheros PDF distintos con el mismo resumen SHA-1, lo cual podría considerarse una
vulnerabilidad muy grande.</p>
<p>Como la salida de la función HMAC-SHA-1 genera un resumen de 160 bits (20 bytes) se debe realizar una operación de truncado a “algo” que
sea fácilmente después retornado por el usuario, ya que un código de muchos dígitos dificultaría el acto de autenticación y empeoraría la
experiencia final del usuario. Es importante que los valores generados por el algoritmo HOTP sean tratados como big-endian, es decir,
representar los bytes en el orden natural (desde la izquierda) y evitar así problemas de interpretación</p>

          https://openaccess.uoc.edu/bitstream/10609/99946/6/javgueramTFM0619memoria.pdf
 
