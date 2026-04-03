from flask_jwt_extended import get_jwt


def is_admin():
    """Return True if the current JWT belongs to an admin user."""
    claims = get_jwt()
    return claims.get("is_admin", False)