# frontend/exceptions.py

class APIError(Exception):
    """Classe de base pour toutes les exceptions de notre API."""
    pass

class AuthenticationError(APIError):
    """Levée quand le token est invalide ou expiré (Erreur 401)."""
    pass

class NetworkError(APIError):
    """Levée en cas de problème de connexion internet ou serveur HS."""
    pass

class ValidatorError(APIError):
    """Levée en cas de problème de connexion internet ou serveur HS."""
    pass