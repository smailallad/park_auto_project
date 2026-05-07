def get_headers(user_token: str):
        """Centralise la construction des headers avec le token."""
        return {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json",
        }