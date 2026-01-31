from dataclasses import dataclass


@dataclass(slots=True)
class Permission:
    permission_str: str


class AuthMiddleware:
    @staticmethod
    async def has_permission(permission: Permission, scopes: list[int]):
        pass
