from app.schemas.chat import UserIdentity


def can_access(visibility: str, user: UserIdentity) -> bool:
    # visibility format examples:
    # employee:all | employee:dept:finance | admin:all
    parts = visibility.split(":")
    if len(parts) < 2:
        return False

    role_rule = parts[0]
    scope = parts[1]

    if role_rule == "admin" and user.role != "admin":
        return False
    if role_rule == "employee" and user.role not in {"employee", "admin"}:
        return False

    if scope == "all":
        return True

    if scope == "dept" and len(parts) == 3:
        return user.dept == parts[2] or user.role == "admin"

    return False
