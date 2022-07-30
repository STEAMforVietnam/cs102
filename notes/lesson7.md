# Bài 7: Lần Theo Dấu Vết

> Đây là phần ghi chú và hướng dẫn cho bài học. Bạn có thể dùng nó để ôn và luyện tập sau giờ lên lớp.
> Chúc bạn thành công! 

## 1. Hiển Thị NPC

>Nhiệm vụ: Khởi tạo và hiển thị được các NPC trong game.

Đầu tiên, ta sẽ khởi tạo các thông số (configure) cho NPC (trong game này NPC của chúng ta sẽ là NPC_CO_NGA) bằng cách như sau:

B1: Truy cập `src/config.py` và thêm vào đoạn code dưới đây:

```python
@dataclass
class NpcConfig:
    entity_type: EntityType
    scale: float = 0.07
    animation_interval_ms: int = 900
    default_alpha: int = 180  # 255 is fully opaque

    def __post_init__(self):
        self.sprite_path = ASSET_DIR / "npcs" / self.entity_type.name.lower()
```
B2: Truy cập `src/common/types.py` và sẽ khởi tạo trong class `EntityType` với biến `NPC_CO_NGA = 42`.

```python
class EntityType(enum.Enum):
    # The images of these types will be scaled down to GameConfig.tile_size right after loading.
    ...
    PLAYER = 41 
    NPC_CO_NGA = 42

OBSTACLES_TYPES = (EntityType.GROUND,)
COLLECTABLE_TYPES = (EntityType.HEART, EntityType.CANDY)	
COLLECTABLE_TYPES = (EntityType.HEART, EntityType.CANDY)
FRIENDLY_NPC_TYPES = (EntityType.NPC_CO_NGA,)
```
B3: Thêm đoạn code sau vào `src/game_entities/entity_factory.py`, giúp gọi class `NPCconfig` khi cần thiết.

```python
...
class EntityFactory:
    ...
    elif entity_type in FRIENDLY_NPC_TYPES:
            config: NpcConfig = NpcConfig(entity_type=entity_type)
            return FriendlyNpc(
                entity_type=entity_type,
                npc_config=config,
                sprite=AnimatedSprite(
                    x=x,
                    y=y,
                    sprite_path=config.sprite_path,
                    scale=config.scale,
                    animation_interval_ms=config.animation_interval_ms,
                ),
            )
    else:
        return BaseEntity(entity_type=entity_type,)
```

B4: Khởi tạo class `FriendlyNPC` trong `src/game_entities/friendly_npc.py`

```python
from __future__ import annotations

from config import GameConfig, NpcConfig
from game_entities.base import BaseEntity


class FriendlyNpc(BaseEntity):
    """
    Non-playable character, will talk and interact with Player.
    """

    def __init__(self, npc_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Shift position up to above the ground tile, since Npc is taller than standard tile size.
        self.rect.bottom = self.rect.y + GameConfig.TILE_SIZE
        self.npc_config: NpcConfig = npc_config
```
B5: Truy cập file `1.csv` để thêm NPC vào vị trí mong muốn.

## 2. Tương Tác Với NPC

>Nhiệm vụ: Làm quen với Game Events, cách khởi tạo một Game Event và thêm nó vào Event Queue.

Miêu tả: Khi `Player` đến gần `NPC` thì sẽ xuất hiện dấu chấm hỏi.

Ta sử dụng `pygame.event` một module giúp tương tác với các event trong game và Event Queue.

Trong sự án này, để làm được nhiệm vụ ta cần:

1. Dùng hàm `pygame.event.custom_type()` để khởi tạo một Event cho biết liệu Player có đứng gần NPC hay không?
    ```python
        PLAYER_NEAR_NPC = pygame.event.custom_type()
    ```
2. Nếu `Player` đứng gần `NPC` thì sẽ xuất hiện dấu hỏi, ngược lại thì không, bằng cách liên tục thực hiền hàm `update()` ở mỗi tick đối với `NPC` và `_update_npc_near_by()`

Hàm `update()` trong `src/game_entities/friendly_npc.py`.

```python
def update(self, events: Sequence[GameEvent], world: World) -> None:
        self.events = events
        self.world = world
        self._handle_events()
        if self.is_near_player:
            self._highlight()   // Xuất hiện Dấu chấm hỏi
        else:
            self._unhighlight()   // Nếu Player đi xa khỏi NPC, mất dấu chấm hỏi
        super().update(events, world)
```
Hàm `_update_npc_near_by()` trong `src/game_entities/player.py`

```python
def _update_npc_near_by(self):
        for npc in self.world.get_friendly_npcs():
            if self.collide(npc):
                # Get a hold of the NPC, and broadcast an event for that NPC to handle
                self.npc_near_by = npc
                GameEvent(EventType.PLAYER_NEAR_NPC, listener_id=npc.id).post()
                break
```
## 3. Xuất Hiện Hộp Thoại

>Nhiệm vụ: Khi `Player` đứng gần `NPC`, sau khi xuất hiện dấu chấm hỏi, nếu người chơi ấn phím `e` thì sẽ xuất hiện hộp hội thoại và nội dung của nó.

Để hoàn thành nhiệm vụ này, ta cũng sẽ cần thêm một event vào event queue, đó là `PLAYER_ACTIVATE_NPC`, tương tự như trên.

```python
       PLAYER_ACTIVATE_NPC = pygame.event.custom_type()
```

Tiếp theo, Khi `Player` đứng gần `NPC` và người chơi ấn `e` thì sẽ thực hiện hàm `_handle_activation()`

```python
 def _handle_activation(self):
        logger.info(f"_handle_activation - self.npc_near_by: {self.npc_near_by}")
        if not self.npc_near_by:
            return
        # Broadcast an event for the NPC to handle
        GameEvent(EventType.PLAYER_ACTIVATE_NPC, listener_id=self.npc_near_by.id).post()
```
Hàm này sẽ thêm Event `PLAYER_ACTIVATE_NPC` vào event queue đối với class `Player`, còn đối với class `FriendlyNPC` hàm `_activate()` sẽ thực hiện khi thấy event `PLAYER_ACTIVATE_NPC`.

```python
def _activate(self):
        """
        Manipulates the dialogue box entity.
        """
        logger.info("NPC Activated")
        if not self.dialogue_box_id:
            self.dialogue_box_id = self.world.add_entity(EntityType.DIALOGUE_BOX)
        dialogue_box = self.world.get_entity(self.dialogue_box_id)
        dialogue_box.sprite.set_text("Xin chào!")
```
Hàm này sẽ thiết lập Hộp hội thoại và nội dung của nó.

Còn đây là đoạn code giúp hiển thị Hộp thoại và nội dung:
`src/gui/dialogue_box_sprite.py`
```python
from config import Color, DialogueBoxConfig, Font
from gui.base_sprite import BaseSprite


class DialogueBoxSprite(BaseSprite):
    """
    Render the dialogue box and text within it.
    """

    def set_text(self, text):
        self.text = text

    def render(self, screen, *args, **kwargs):
        super().render(screen, *args, **kwargs)
        if not self.text:
            return

        x = self.rect.x + DialogueBoxConfig.PADDING_X
        y = self.rect.y + DialogueBoxConfig.PADDING_Y + DialogueBoxConfig.LINE_HEIGHT
        screen.blit(
            Font.FREESANSBOLD_14.render(self.text, True, Color.TEXT_DIALOGUE_SUBJECT),
            (x, y),
        )
```
## 4. Trò chuyện với NPC

>Nhiệm vụ: Lần lượt hiển thị toàn bộ nội dung của cuộc hội thoại giữa `PLAYER` và `NPC`.

Sử dụng thư viện `json` đối với nhiệm vụ này.

Tạo một file `json` và viết toàn bộ nội dung của cuộc hội thoại ví dụ như sau:

`src/gui/dialogue_box_sprite.py`

```json
{
    "name": "Cô Nga",
    "dialogues": [
      [
        {
          "Subject": "Cô Nga",
          "Line": "Xin chào em! Em tên là gì?"
        },
        {
          "Subject": "Táy Máy",
          "Line": "Xin chào cô! Em tên là Táy Máy. Em là thực tập sinh mới ạ."
        },
        {
          "Subject": "Cô Nga",
          "Line": "Ồ, tốt quá. Em có thể nhặt hộ cô những viên kẹo bị đánh rơi được không?"
        },
        {
          "Subject": "Táy Máy",
          "Line": "Được ạ!"
        }
      ],
      [
        {
          "Subject": "Cô Nga",
          "Line": "Em nhặt được hết kẹo chưa?"
        }
      ]
    ]
}
```

Sau đó, ta cũng sẽ khởi tạo một event cho việc hiển thị lần lược từng câu cho đến khi kết thúc hội thoại.

```python
NPC_DIALOGUE_END = pygame.event.custom_type()
```

Đây là đoạn code để hiện thị từng dòng khi ấn nút `e` giữa 2 nhân vật

`src/game_entities/friendly_npc.py`

```python
def _get_next_line(self) -> Optional[str]:
        """
        Returns the next line in the current dialogue or None.
        """
        self.line_index += 1
        if self.line_index >= len(self.dialogues[self.dialogue_index]):
            # Prepare to move on to the next dialogue,
            # return None to indicate current dialogue has ended.
            self.line_index = -1
            self.dialogue_index += 1
            return None
        if not self.has_quest():
            return None
        line = self.dialogues[self.dialogue_index][self.line_index]
        return "\n".join((line["Subject"], line["Line"]))
```

## 5. Hiển Thị Font Tiếng Việt

Khi thực hiên xong cột mốc 4, trong Python sẽ bị lỗi không thể hiển thị được Font tiếng Việt, để khắc phục vấn đề này, ta sẽ làm như sau:

Thêm file chưa font chữ mong muốn, cụ thể trong game này sẽ là font chữ `Arial`

```python
FONT_PATH = ASSET_DIR / "fonts" / "arial.ttf"
```

```python
@functools.lru_cache(maxsize=None)
def get_font(font_size):
    """
    Font loading is slow, but PyGame doesn't let you load a font without specifying a font size,
    so we cache the loaded ones to improve performance.
    If you get some error around here, that is probably due to using an older Python version.
    In that case, remove the decorator line `@functools.lru_cache(maxsize=None)` and try again.
    """
    return Font(FONT_PATH, font_size)
```

Nếu bạn gặp lỗi tại bước này, khả năng là bạn đang sử dụng Python phiên bản cũ hơn. Trong trường hợp này, bạn có thể bỏ dòng `@functools.lru_cache(maxsize=None)` và chạy lại chương trình.

## Kết quả bài học

* Ta đã biết được NPC là gì và cách hiển thị một NPC trong game.
* Tương tác với NPC thông qua việc gửi và nhận Event
* Cài đặt đoạn hội thoại và cách hiển thị Font tiếng Việt trong khi Python không hỗ trợ việc này.