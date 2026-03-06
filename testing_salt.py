python3 -c "
import hashlib, os

password = 'mi_password_secreto'

# MAL - nunca hagas esto en produccion
malo = hashlib.sha256(password.encode()).hexdigest()
print('SHA256 sin salt (inseguro):', malo)

# BIEN - siempre usa salt
# Salt es un valor aleatorio unico que se mezcla con el password antes de hashear. Se genera distinto para cada usuario.
# repetido 100,000 veces (hace que un potencial ataque de fuerza bruta sea muy muy lento y costoso para el atacante)

salt = os.urandom(32)
bueno = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
print('PBKDF2 con salt (seguro)  :', bueno.hex())
"
