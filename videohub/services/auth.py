class AuthService:

    def __init__(self, http):
        self.http = http

    async def login(self, login: str, password: str):

        return await self.http.post(
            "/auth/login",
            {
                "login": login,
                "password": password
            },
            auth_required=False
        )