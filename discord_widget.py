import asyncio
import requests
import tkinter as tk
from io import BytesIO
from PIL import Image, ImageTk
from no_gui_gui import TransparentWin


class DiscordWidget(TransparentWin):
    def __init__(self, loop):
        super().__init__()
        self.image_list = []
        self.user_data = []
        asyncio.ensure_future(self.await_photo_update(), loop=loop)
        asyncio.ensure_future(self.independent_refresh_loop(), loop=loop)

    async def await_photo_update(self):
        while True:
            await asyncio.sleep(1)
            r = requests.get("http://83.26.83.57:2137/status")
            assert r.status_code == 200, print(f"PROBLEM {r.status_code}"); break
            active_users_data = [x for x in r.json()['active']]
            for user in active_users_data:
                if user[0] not in [u[0] for u in self.user_data]:
                    await self.create_icon(user)
                pass
            for user in self.user_data:
                if user[0] not in [u[0] for u in active_users_data]:
                    self.user_data.pop(self.user_data.index(next(u for u in self.user_data if u[0] == user[0])))
                    user[2].destroy()
            self.update()

    async def create_icon(self, user_data):
        w = requests.get(f"https://cdn.discordapp.com/avatars/{user_data[0]}/{user_data[1]}.png")
        image = Image.open(BytesIO(w.content))
        photo = ImageTk.PhotoImage(image)
        my_btn = tk.Button(
            self,
            width=120,
            height=120,
            image=photo
        )
        self.user_data.append([user_data[0], photo, my_btn])
        my_btn.pack(side=tk.LEFT)

    async def independent_refresh_loop(self):
        while True:
            await asyncio.sleep(0.01)
            self.update()


def __run__():
    loop = asyncio.get_event_loop()
    DiscordWidget(loop)
    loop.run_forever()


if __name__ == '__main__':
    __run__()
