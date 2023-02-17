"""
Fork of arcade.Scene that fixes a bug when adding empty SpriteLists.
See PR: https://github.com/pythonarcade/arcade/pull/1527/files
"""
from typing import Optional

import arcade
from arcade import SpriteList


class Scene(arcade.Scene):
    def __init__(self) -> None:
        super().__init__()

    def add_sprite_list(
        self,
        name: str,
        use_spatial_hash: bool = False,
        sprite_list: Optional[SpriteList] = None,
    ) -> None:
        """
        Add a SpriteList to the scene with the specified name.

        This will add a new SpriteList to the scene at the end of the draw order.

        If no SpriteList is supplied via the `sprite_list` parameter then a new one will be
        created, and the `use_spatial_hash` parameter will be respected for that creation.

        :param str name: The name to give the SpriteList.
        :param bool use_spatial_hash: Wether or not to use spatial hash if creating a new SpriteList.
        :param SpriteList sprite_list: The SpriteList to add, optional.
        """
        if sprite_list is None:
            sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)
        self.name_mapping[name] = sprite_list
        self.sprite_lists.append(sprite_list)

    def add_sprite_list_before(
        self,
        name: str,
        before: str,
        use_spatial_hash: bool = False,
        sprite_list: Optional[SpriteList] = None,
    ) -> None:
        """
        Add a SpriteList to the scene with the specified name before a specific SpriteList.

        This will add a new SpriteList to the scene before the specified SpriteList in the draw order.

        If no SpriteList is supplied via the `sprite_list` parameter then a new one will be
        created, and the `use_spatial_hash` parameter will be respected for that creation.

        :param str name: The name to give the SpriteList.
        :param str before: The name of the SpriteList to place this one before.
        :param bool use_spatial_hash: Wether or not to use spatial hash if creating a new SpriteList.
        :param SpriteList sprite_list: The SpriteList to add, optional.
        """
        if sprite_list is None:
            sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)
        self.name_mapping[name] = sprite_list
        before_list = self.name_mapping[before]
        index = self.sprite_lists.index(before_list)
        self.sprite_lists.insert(index, sprite_list)

    def add_sprite_list_after(
        self,
        name: str,
        after: str,
        use_spatial_hash: bool = False,
        sprite_list: Optional[SpriteList] = None,
    ) -> None:
        """
        Add a SpriteList to the scene with the specified name after a specific SpriteList.

        This will add a new SpriteList to the scene after the specified SpriteList in the draw order.

        If no SpriteList is supplied via the `sprite_list` parameter then a new one will be
        created, and the `use_spatial_hash` parameter will be respected for that creation.

        :param str name: The name to give the SpriteList.
        :param str after: The name of the SpriteList to place this one after.
        :param bool use_spatial_hash: Wether or not to use spatial hash if creating a new SpriteList.
        :param SpriteList sprite_list: The SpriteList to add, optional.
        """
        if sprite_list is None:
            sprite_list = SpriteList(use_spatial_hash=use_spatial_hash)
        self.name_mapping[name] = sprite_list
        after_list = self.name_mapping[after]
        index = self.sprite_lists.index(after_list) + 1
        self.sprite_lists.insert(index, sprite_list)
