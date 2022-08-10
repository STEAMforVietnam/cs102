# Bài 9: Tìm Kiếm Sức Mạnh

> Đây là phần ghi chú và hướng dẫn cho bài học. Bạn có thể dùng nó để ôn và luyện tập sau giờ lên lớp.
> Chúc bạn thành công! 

## 1. Bảng tùy chọn (Menu)

>Nhiệm vụ: Tạo menu tùy chỉnh các level, pause, resume, và restart game

B1: khởi tạo thêm một class mới tên `menu.py` trong thư mục `src/worlds/` với nội dung sau đây để hiển thị giao diện trong trang menu

```python
class Menu(BaseWorld):
    """The menu page."""

    def __init__(self, screen: Surface, can_resume: bool) -> None:
        super().__init__(screen)
        self.can_resume = can_resume
        self.menu = pygame_menu.Menu(
            GameConfig.NAME,
            GameConfig.WIDTH,
            GameConfig.HEIGHT,
            theme=pygame_menu.themes.THEME_SOLARIZED,
        )

        frame = self.menu.add.frame_v(GameConfig.WIDTH - 700, GameConfig.HEIGHT - 400)
        if not self.can_resume:
            frame.pack(self.menu.add.button("Play", partial(start_game, level_id=1)))
        else:
            frame.pack(self.menu.add.button("Resume", GameEvent(EventType.RESUME_GAME).post))
            frame.pack(
                self.menu.add.button("Restart Level", GameEvent(EventType.RESTART_LEVEL).post)
            )

        frame.pack(self.menu.add.button("Quit", lambda: GameEvent(pygame.QUIT).post()))

    def tick(self, events: Sequence[GameEvent]) -> bool:
        if self.menu.is_enabled():
            self.menu.update([e.event for e in events])
            self.menu.draw(self.screen)
        return True
```
B2: Truy cập `src/worlds/world_manager.py` để hiện thực các sự kiện trong trang menu với hàm `start_or_resume_game`: 

```python
def start_or_resume_game(self, level_id: int, force_start: bool):
    self.active_world = self.WORLD_GAME
    if force_start or not self.worlds[self.active_world] or level_id != self.level_id:
        logger.info(f"Current level: {self.level_id} -> (Re)starting level: {level_id}")
        self.level_id = level_id
        self.worlds[self.active_world] = World(self.screen, level_id=level_id)

        # TODO: this could be optimized instead of initiating a new Menu instance somehow?
        self.worlds[self.WORLD_MENU] = Menu(self.screen, can_resume=True)
```
B3: Trong hàm `tick`, thêm `for` loop như sau để handle các thao tác người dùng:
```python
for e in events:
    if e.is_type(EventType.START_GAME):
        self.start_or_resume_game(level_id=e.event.level_id, force_start=True)
    elif e.is_type(EventType.RESTART_LEVEL):
        self.start_or_resume_game(level_id=self.level_id, force_start=True)
    elif e.is_type(EventType.RESUME_GAME):
        self.start_or_resume_game(level_id=self.level_id, force_start=False)
    elif e.is_type(EventType.LEVEL_END):
        self.start_or_resume_game(level_id=self.level_id + 1)
    elif e.is_key_up(pygame.K_ESCAPE) and self.active_world == self.WORLD_GAME:
        self.active_world = self.WORLD_MENU

```

## 2. Túi vật phẩm (Inventory)

>Nhiệm vụ: Người chơi nhặt vật phẩm và hiện trên màn hình số lượng vật phẩm đã nhặt được

Miêu tả: Khi `Player` đến gần `item` thì vật phẩm sẽ mất đi, đồng thời túi vật phẩm của `Player` sẽ nhận thêm vật phẩm mới.

B1: Trong `src/entities/`, thêm file `player_inventory.py` với nội dung như sau

```python
class PlayerInventory(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inventory: List = []
        self.rect.centery = self.rect.y + PlayerInventoryConfig.TILE_SIZE // 2

    def set_inventory(self, inventory: List):
        """Set the backend data, called by Player."""
        self.inventory = inventory

    def render(
        self,
        screen: pygame.Surface,
        *args,
        **kwargs,
    ) -> None:
        super().render(screen, *args, **kwargs)

        # Render the collected items, each with a count.
        # This computation could be optimized more for performance.
        counter = Counter([item.entity_type for item in self.inventory])
        inventory_dict = {item.entity_type: item for item in self.inventory}
        x = PlayerInventoryConfig.X
        y = PlayerInventoryConfig.Y
        for entity_type, cnt in counter.items():
            x += PlayerInventoryConfig.X_STEP
            inventory_dict[entity_type].render(
                screen,
                x_y=(x, y),
                scale=(PlayerInventoryConfig.TILE_SIZE, PlayerInventoryConfig.TILE_SIZE),
            )
            util.display_text(
                screen,
                text=str(cnt),
                x=x + PlayerInventoryConfig.TILE_SIZE - 2,
                y=y + PlayerInventoryConfig.TILE_SIZE - 2,
                color=Color.TEXT_INVENTORY_CNT,
            )
```
B2: Trong file `config.py`, thêm thiết lập `PlayerInventoryConfig`, để giúp tạo thêm entity mới trong `entity_factory`: 

```python
class PlayerInventoryConfig:
    X: int = 290
    Y: int = 30
    X_STEP: int = 60  # distance between 2 consecutive items

    # the simple vertical divider
    SPRITE_PATH: Path = ASSET_DIR / "items" / "player_inventory.png"
    SCALE: int = 1

    TILE_SIZE: int = 34
```

B3: Truy cập vào file `src/entities/entity_factory.py`, khai báo entity mới bằng cách thêm đoạn code sau vào hàm `create`:
```python
elif entity_type == EntityType.PLAYER_INVENTORY:
    return PlayerInventory(
        entity_type=entity_type,
        x=PlayerInventoryConfig.X,
        y=PlayerInventoryConfig.Y,
        sprite_path=PlayerInventoryConfig.SPRITE_PATH,
        scale=PlayerInventoryConfig.SCALE,
    )
```

B4: Trong file `src/entities/player.py`, thêm hàm `_pick_item_near_by` vào class `Player` như sau:
```python
def _pick_item_near_by(self):
    """
    If Player collides with a collectable entity, remove that entity from World,
    while adding that entity to the self.inventory list.
    """
    for entity in self.world.get_collectable_tiles():
        if self.collide(entity):
            self.world.remove_entity(entity.id)
            self.inventory.append(entity)
            logger.info(f"Player picked up 1 {entity.entity_type}")
```

B5: Trong file `src/entities/player.py`, thêm hàm `_update_inventory_entity` vào class `Player` như sau:
```python
def _update_inventory_entity(self):
    """
    This Player entity directly manages a PlayerInventory entity.
    """
    if not self.inventory_entity_id:
        self.inventory_entity_id = self.world.add_entity(EntityType.PLAYER_INVENTORY)
    self.world.get_entity(self.inventory_entity_id).set_inventory(self.inventory)
```

## 3. Nhiệm vụ bắt đầu và hiển thị Trampoline parts (Start quest and trampoline parts)

>Nhiệm vụ: Khi `Player` đứng gần `NPC_chu_Nam`, sau khi trò chuyện, người chơi được nhận nhiệm vụ thu thập các phần của bậc bênh, đồng thời các vật phẩm mới sẽ xuất hiện

B1: Thêm các item code vào file data/levels/1/cvs phù hợp với code trong file src/common/types:
```python
TRAMPOLINE_PART_SPRING = 31
TRAMPOLINE_PART_FRAME = 32
```
B2: Thêm `QuestToStart` vào `data/dialogues/npc_chu_nam.json`:

```json
{
    "Subject": "Táy Máy",
    "Line": "Được ạ!",
    "QuestToStart": "TRAMPOLINE"
}
```
B3: Tiếp theo chúng ta cần khai báo thêm các `custom events` trong file `src/common/events.py`:

```python
QUEST_START = pygame.event.custom_type()
QUEST_END = pygame.event.custom_type()
BOSS_DIE = pygame.event.custom_type()
```
B4: Việc thêm các `custom events` mới sẽ giúp chúng ta điều khiển được các item đang ẩn hiện ra khi một event cụ thể nào đó được kích hoạt. Tạo file mới `src/entities/trampoline_part.py` để hiện thực được điều này:

```python
class TrampolinePart(BaseEntity):
    """
    Trampoline parts that can be picked up to give to an NPC.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_active(False)

    def update(self, events: Sequence[GameEvent], world: World):
        """
        Turn on sprite visibility when the TRAMPOLINE quest starts.
        """
        super().update(events, world)
        for e in self.events:
            if e.is_type(EventType.QUEST_START) and e.event.quest_name == QuestName.TRAMPOLINE:
                self.set_active(True)
```
B5: Thêm entity `TrampolinePart` vào `entity_factory` trong hàm `create`
```python
elif entity_type in TRAMPOLINE_PART_TYPES:
    return TrampolinePart(
        entity_type=entity_type,
        x=x,
        y=y,
        sprite_path=ASSET_DIR / "items" / f"{entity_type.name.lower()}.png",
        scale=(GameConfig.TILE_SIZE, GameConfig.TILE_SIZE),
    )
```
B6: Trong file `src/entities/friendly_npc.py`, kích hoạt `TRAMPOLINE` event khi kết thúc cuộc hội thoại. Sau khi kích hoạt `TRAMPOLINE` event, các `Trampoline_part` sẽ được hiện ra. Sửa hàm `_activate` với nội dung như sau:
```python
str_quest_name = next_dialogue_item.get("QuestToStart")
if str_quest_name:
    quest_name = QuestName[str_quest_name]
    logger.info(f"Starting Quest: {quest_name}")
    self.should_loop_last_dialogue = True
    GameEvent(EventType.QUEST_START, sender_id=self.id, quest_name=quest_name).post()
```
## 4. Trampoline

>Nhiệm vụ: Hiện thực chức năng của một trampoline để có thể giúp bạn Táy Máy nhảy cao hơn khi bước lên nó.

B1: Thêm file mới `trampoline.py` vào `src/entities`. Vì trampoline sẽ không có thêm các tính năng mới, nên nội dung của entity này sẽ chính là nội dung của BaseEntity

```python
from entities.animated_entity import PropEntity
class Trampoline(PropEntity):
    """
    Trampoline item for the TRAMPOLINE_QUEST. This class just inherits from the parent class and
    does not need any custom behavior hence the body is empty.
    """
```

B2: Thêm type mới `TRAMPOLINE` vào `src/common/types.py`:
```python
TRAMPOLINE = 30
```

B3: Thêm thiết lập mới cho `Trampoline` vào file `config.py` để hỗ trợ cho việc thêm entity mới vào `entity_factory`:

```python
class TrampolineConfig:
    SPRITE_PATH: Path = ASSET_DIR / "items" / "trampoline"
    SCALE: float = 0.3
    ANIMATION_INTERVAL_MS: int = 200
```

B4: Khai báo entity mới vào `src/entities/entity_factory.py` trong hàm `create`:

```python
elif entity_type == EntityType.TRAMPOLINE:
    return Trampoline(
        entity_type=entity_type,
        x=x,
        y=y,
        sprite_path=TrampolineConfig.SPRITE_PATH,
        scale=TrampolineConfig.SCALE,
        animation_interval_ms=TrampolineConfig.ANIMATION_INTERVAL_MS,
    )
```
B5: Sau khi chúng ta tạo được `Trampoline`, cần phải có một nơi để chúng ta có thể tương tác với các trampoline này. Trong file `src/worlds/world.py`, tạo hàm mới tên `get_trampolines`:
```python
def get_trampolines(self) -> List[BaseEntity]:
    return [
        entity
        for entity in self.entities.values()
        if entity.entity_type == EntityType.TRAMPOLINE
    ]
```
B6: Hiện trampoline với tọa độ cố định phục vụ cho việc hiện thực chức năng. Trong `src/worlds/world.py`, thêm đoạn code sau vào cuối hàm `load_level`
```python
# add a trampoline into a level temporary for development
self.add_entity(
    EntityType.TRAMPOLINE,
    76,
    612,
)
```

B7: Sau khi đã có hàm `get_trampolines` để chúng ta có thể truy xuất tất cả các trampolines, tạo hàm chính `_maybe_jump_with_trampoline` trong file `src/entities/player.py`:
```python
def _maybe_jump_with_trampoline(self):
    for trampoline in self.world.get_trampolines():
        if self.collide(trampoline) and self.rect.bottom > trampoline.rect.top:
            trampoline.set_action(ActionType.JUMP)
            self.jump_with_trampoline()
        else:
            trampoline.set_action(ActionType.IDLE)
```

B8: Trong file `src/enities/player.py`, gọi hàm `_maybe_jump_with_trampoline` trong hàm `update` để đảm bảo rằng sẽ kiểm tra xem người chơi có đang nhảy trên trampoline hay không

```python
def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._update_npc_near_by()
        self._pick_item_near_by()
        self._handle_events()
        self._update_screen_offset()

        # highlight this call only
        self._maybe_jump_with_trampoline()

        # Manage the dependent entities.
        self._update_inventory_entity()
```

## 5. Hiện thực logic cho một level (level logic)

>Nhiệm vụ: Khi chúng ta đã hiện thực xong tất cả các phần cho một level, đây là lúc kết nối các phần với nhau để tạo ra một level hoàn chỉnh
B1: Tạo thư mục mới tên `level_logics` để chứa logic của tất cả các level
B2: Tạo file `__init__.py` trong `src/level_logics` với nội dung như sau: 
```python
from typing import Callable, Optional
from level_logics import one
def get_event_handler(level_id: int) -> Optional[Callable]:
    return {
        1: one.event_handler,
    }.get(level_id)
```
B3: Tạo file `one.py` trong thư mục src/level_logics để chứa logic của level 1:
```python
from __future__ import annotations

from typing import TYPE_CHECKING

from common.event import EventType, GameEvent
from common.types import TRAMPOLINE_PART_TYPES, EntityType, QuestName

if TYPE_CHECKING:
    from worlds.world import World


def event_handler(world: World) -> None:
    """
    Logics for some specific events in level 1.
    """
    for event in world.events:
        npc_chu_nam_id = world.get_entity_id_by_type(EntityType.NPC_CHU_NAM)

        # Player finishes TRAMPOLINE quest.
        if (
            event.get_sender_id() == npc_chu_nam_id
            and event.is_type(EventType.NPC_DIALOGUE_END)
            and world.player.count_inventory(TRAMPOLINE_PART_TYPES) >= 4
        ):
            GameEvent(
                EventType.QUEST_END,
                listener_id=npc_chu_nam_id,
                quest_name=QuestName.TRAMPOLINE,
            ).post()

            world.player.discard_inventory(TRAMPOLINE_PART_TYPES)

            # NPC makes the trampoline
            npc = world.get_entity(npc_chu_nam_id)
            world.add_entity(
                EntityType.TRAMPOLINE,
                npc.rect.x + 76,
                npc.rect.y + 156,
            )
```
## Kết quả bài học

* Ta đã biết được các thiết kế và hiển thị một menu game
* Nhặt các vật phẩm và cập nhật túi vật phẩm
* Bắt đầu một nhiệm vụ và cập nhật trạng thái của các vật phẩm liên quan đến nhiệm vụ đó
* Hiện thực chức năng của một trampoline là giúp người chơi có thể nhảy cao hơn
* Hiện thực logic của một level và quản lý nó