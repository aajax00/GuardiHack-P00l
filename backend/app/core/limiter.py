from slowapi import Limiter
from slowapi.util import get_remote_address

# On utilise l'adresse IP de l'utilisateur pour le limiter
limiter = Limiter(key_func=get_remote_address)