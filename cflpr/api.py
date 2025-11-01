from typing import Callable
from datetime import datetime, timezone
import aiohttp
import base64
import json

from .models import PR, Ticket

BASE_URL = "https://pr-mobile-a.cfl.lu"


class CFLPRAPIAuthException(Exception):
    """"""


class CFLPRAPI:
    def __init__(
        self,
        refresh_token: str | None = None,
        refresh_token_listener: Callable[[str], None] | None = None,
    ) -> None:
        self.__session = aiohttp.ClientSession(raise_for_status=True)
        self.__refresh_token: str | None = refresh_token
        self.__access_token: str | None = None
        self.__token_listener = refresh_token_listener

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.__close()

    async def authenticate(self, email: str, password: str) -> bool:
        async with self.__session.post(
            f"{BASE_URL}/AppUser/UserLogin",
            json={"email": email, "password": password},
        ) as resp:
            data = await resp.json()
            self.__access_token = data["accessToken"]
            self.__refresh_token = data["refreshToken"]
            self.__notify_listener()
            return True

    async def get_all_pr(self) -> list[PR]:
        async with self.__session.get(f"{BASE_URL}/ParkAndRide") as resp:
            data = await resp.json()
            return list(
                map(
                    PR.from_json,
                    data,
                )
            )

    async def get_pr(self, id: str) -> PR:
        async with self.__session.get(f"{BASE_URL}/ParkAndRide/{id}") as resp:
            data = await resp.json()
            return PR.from_json(data)

    async def get_subscription_available_spots(self, id: str) -> int:
        auth = await self.__get_auth_headers()
        async with self.__session.get(
            f"{BASE_URL}/Subscription/getAvailableSpots?parkAndRideId={id}",
            headers=auth,
        ) as resp:
            data = await resp.json()
            return data["availableSpots"]

    async def get_closed_tickets(self) -> list[Ticket]:
        auth = await self.__get_auth_headers()
        async with self.__session.get(
            f"{BASE_URL}/AppUser/GetClosedTickets",
            headers=auth,
        ) as resp:
            data = await resp.json()
            return list(
                map(
                    Ticket.from_json,
                    data,
                )
            )

    async def get_tickets(self) -> list[Ticket]:
        auth = await self.__get_auth_headers()
        async with self.__session.get(
            f"{BASE_URL}/AppUser/GetTickets",
            headers=auth,
        ) as resp:
            data = await resp.json()
            return list(
                map(
                    Ticket.from_json,
                    data,
                )
            )

    async def refresh_tokens(self) -> None:
        if self.__refresh_token is None:
            raise CFLPRAPIAuthException()
        async with self.__session.post(
            f"{BASE_URL}/AppUser/Refresh",
            json={"refreshToken": self.__refresh_token},
            raise_for_status=False,
        ) as resp:
            if resp.status != 200:
                if resp.status == 401:
                    raise CFLPRAPIAuthException()
                raise Exception(f"Cannot refresh tokens: http status {resp.status}")
            data = await resp.json()
            self.__access_token = data["accessToken"]
            self.__refresh_token = data["refreshToken"]
            self.__notify_listener()

    async def __close(self) -> None:
        if not self.__session.closed:
            await self.__session.close()

    def __notify_listener(self) -> None:
        if self.__token_listener is not None:
            self.__token_listener(str(self.__refresh_token))

    async def __get_auth_headers(self) -> dict[str, str]:
        need_refresh = False
        if self.__access_token is None:
            need_refresh = True
        else:
            payload = self.__access_token.split(".")[1]
            payload = payload.encode("ascii")
            rem = len(payload) % 4
            if rem:
                payload += b"=" * (4 - rem)
            decoded = base64.urlsafe_b64decode(payload)
            parsed = json.loads(decoded)
            exp = parsed["exp"]
            exp_utc = datetime.fromtimestamp(int(exp), tz=timezone.utc)
            now_utc = datetime.now(timezone.utc)
            delta = exp_utc - now_utc
            if int(delta.total_seconds()) <= 60:
                need_refresh = True
        if need_refresh:
            await self.refresh_tokens()

        return {"Authorization": str(self.__access_token)}
