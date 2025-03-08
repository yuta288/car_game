# title: Pyxel Jump
# author: Takashi Kitao
# desc: A Pyxel simple game example
# site: https://github.com/kitao/pyxel
# license: MIT
# version: 1.0

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Car")
        pyxel.load("./assets/car_game.pyxres")
        self.reset_game()
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲームのリセット"""
        self.score = 0
        self.player_x = 72
        self.player_y = 72
        self.is_alive = True
        self.fruit = [
            (i * 60, pyxel.rndi(64, 104), pyxel.rndi(0, 1), True) for i in range(4)
        ]
        self.bomb = [
            (i * 60 + 30, pyxel.rndi(64, 104), 2, True, False) for i in range(4)
        ]

    """def generate_fruit(self):
        # 新しいフルーツを生成する
        return (240, pyxel.rndi(64, 104), pyxel.rndi(0, 1), True)"""

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if not self.is_alive:
            self.handle_game_over()
            return

        self.update_player()
        self.fruit = [self.update_fruit(*v) for v in self.fruit]
        self.bomb = [self.update_bomb(*v) for v in self.bomb]

    def handle_game_over(self):
        """ゲームオーバーの処理"""
        if pyxel.btnp(pyxel.KEY_R) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_START):
            self.reset_game()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player_y = max(self.player_y - 2, 64)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player_y = min(self.player_y + 2, pyxel.height - 16)

    def update_fruit(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.score += (kind + 1) * 100
            pyxel.play(3, 4)

        x = x - 2
        if x < -40:
            x = 240
            y = pyxel.rndi(64, 104)
            kind = pyxel.rndi(0, 1)
            is_alive = True

        return (x, y, kind, is_alive)

    def update_bomb(self, x, y, kind, is_alive, exploded):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            exploded = True
            self.is_alive = False
            pyxel.play(3, 6)

        x = x - 2
        if x < -40 and not exploded:
            x = 240
            y = pyxel.rndi(64, 104)
            kind = 2
            is_alive = True
            exploded = False

        return (x, y, kind, is_alive, exploded)

    def draw(self):
        pyxel.cls(12)
        self.draw_road()
        self.draw_clouds()
        self.draw_objects()
        self.draw_score()
        if not self.is_alive:
            self.draw_game_over()

    def draw_road(self):
        pyxel.blt(0, 72, 0, 0, 104, 160, 32)
        pyxel.blt(0, 104, 0, 0, 104, 160, 32)
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 88, 0, 0, 48, 160, 16, 12)
            pyxel.blt(i * 160 - offset, 56, 0, 0, 88, 160, 16, 12)

    def draw_clouds(self):
        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in [(10, 25), (70, 35), (120, 15)]:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

    def draw_objects(self):
        for x, y, kind, is_alive in self.fruit:
            if is_alive:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)
        for x, y, kind, is_alive, exploded in self.bomb:
            if exploded:
                pyxel.blt(x, y, 0, 32 + (kind + 1) * 16, 0, 16, 16, 12)
            elif is_alive:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)
        if self.is_alive:
            pyxel.blt(self.player_x, self.player_y, 0, 0, 0, 16, 16, 12)

    def draw_score(self):
        s = f"SCORE {self.score:>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

    def draw_game_over(self):
        pyxel.text(60, 50, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(45, 65, "PRESS R OR START", 7)


App()


'''
import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Car")
        pyxel.load("./assets/car_game.pyxres")
        self.score = 0
        self.player_x = 72
        self.player_y = -16
        self.player_dy = 0
        self.is_alive = True
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.floor = [(i * 60, pyxel.rndi(8, 104), True) for i in range(4)]
        self.fruit = [
            (i * 60, pyxel.rndi(0, 104), pyxel.rndi(0, 2), True) for i in range(4)
        ]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()
        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)
        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
        self.player_y += self.player_dy
        self.player_dy = min(self.player_dy + 1, 8)

        if self.player_y > pyxel.height:
            if self.is_alive:
                self.is_alive = False
                pyxel.play(3, 5)
            if self.player_y > 600:
                self.score = 0
                self.player_x = 72
                self.player_y = -16
                self.player_dy = 0
                self.is_alive = True

    def update_floor(self, x, y, is_alive):
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_dy > 0
            ):
                is_alive = False
                self.score += 10
                self.player_dy = -12
                pyxel.play(3, 3)
        else:
            y += 6
        x -= 4
        if x < -40:
            x += 240
            y = pyxel.rndi(8, 104)
            is_alive = True
        return x, y, is_alive

    def update_fruit(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.score += (kind + 1) * 100
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(3, 4)
        x -= 2
        if x < -40:
            x += 240
            y = pyxel.rndi(0, 104)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)

    def draw(self):
        pyxel.cls(12)

        # Draw sky
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # Draw mountain
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        # Draw trees
        # #for文で2回繰り返してる。iがオフセットになっており、x座標を変えて2回描写
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # Draw clouds
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)
        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # Draw floors
        for x, y, is_alive in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # Draw fruits
        for x, y, kind, is_alive in self.fruit:
            if is_alive:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

        # Draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_dy > 0 else 0,
            0,
            16,
            16,
            12,
        )

        # Draw score
        s = f"SCORE {self.score:>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()

'''
'''
import pyxel

pyxel.init(160, 120, title="キー入力")
pyxel.load("mygame.pyxres")

x = 80
y = 60
status = 0


def update():
    global x, y

    if pyxel.btn(pyxel.KEY_LEFT):
        x = max(x - 2, 0)
    if pyxel.btn(pyxel.KEY_RIGHT):
        x = min(x + 2, pyxel.width - 16)
    if pyxel.btn(pyxel.KEY_UP):
        y = max(y - 2, 0)
    if pyxel.btn(pyxel.KEY_DOWN):
        y = min(y + 2, pyxel.height - 16)

    if pyxel.btnp(pyxel.KEY_Q):
        pyxe.quit()

    return


def draw():
    pyxel.cls(0)
    pyxel.blt(x, y, 0, 0, 0, 15, 15, 0)

    return


pyxel.run(update, draw)
'''
