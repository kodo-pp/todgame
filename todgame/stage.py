from todgame.sprite import BasicSprite
from todgame.util import robust_list_iter

from typing import List

import pygame as pg  # type: ignore
from coman.coroutine_manager import CoroutineManager


class Stage:
    def __init__(self, surface: pg.Surface) -> None:
        self._surface = surface
        self._coroutine_manager = CoroutineManager()
        self._sprites: List[BasicSprite] = []

    @classmethod
    def from_size(cls, width: int, height: int) -> 'Stage':
        return Stage(surface=pg.Surface((width, height), pg.HWSURFACE | pg.SRCALPHA))

    @property
    def surface(self) -> pg.Surface:
        return self._surface

    @property
    def sprites(self) -> List[BasicSprite]:
        return self._sprites

    @property
    def coroutine_manager(self) -> CoroutineManager:
        return self._coroutine_manager

    def draw_sprites(self) -> None:
        # TODO: zkey-aware drawing
        self.surface.fill(self.clear_color)
        for sprite in self._sprites:
            sprite.draw(destination=self.surface)

    def update(self, time_delta: float) -> None:
        self._coroutine_manager.update(time_delta)
        for sprite in robust_list_iter(self._sprites):
            sprite.update(time_delta)

    clear_color = (0, 0, 0)
