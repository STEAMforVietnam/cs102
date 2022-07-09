# Bài 4: Thách Thức Giới Hạn

> Đây là phần ghi chú và hướng dẫn cho bài học. Bạn có thể dùng nó để ôn tập và luyện tập sau giờ lên lớp.
> Chúc bạn thành công! 

## Cấu trúc thư mục (Cột mốc 1)

Đây là cấu trúc thư mục cơ bản của một game

```shell
├── assets
│   ├── items - chứa các hình ảnh vật phẩm
│   ├── npcs - chứa các hình ảnh NPC
│   └── player - chứa các hình ảnh player
├── readme.md
├── requirements-dev.txt
├── requirements.txt
└── src
    ├── common
    │   ├── __init__.py
    │   ├── event.py - hiện thực các sự kiện trong game
    │   ├── types.py - khai báo các kiểu dữ liệu trong game
    │   └── util.py - các hàm hữu dụng trong game
    ├── game_entities
    │   ├── __init__.py
    │   ├── base_entity.py - thực thể cơ bản
    │   ├── game_item.py - chứa các lớp của vật phẩm trong game
    │   ├── player.py - chứa lớp người chơi
    │   └── robot.py - chứa lớp robot
    ├── gui
    │   ├── __init__.py
    │   ├── animated_sprite.py - chứa lớp hiện thực hoạt họa (animation)
    │   └── base_sprite.py - chứa lớp hiện thực hoạt họa cơ bản
    ├── worlds
    │   ├── __init__.py 
    │   ├── base_world.py - lớp thế giới game cơ bản
    │   ├── world_manager.py  - quản lý các thế giới game
    │   └── world.py - thế giới game (mỗi thế giới là một level khác nhau)
    ├── main.py - hàm chính
    └── config.py - thiết lập các thông số cho game
```

## Chuyển động trong thế giới game và Trọng lực (Cột mốc 2)

Trong file `src/game_entities/movable`, chúng ta dùng kiến thức vật lý `dx` và `dy` để hiện thực các bước chuyển động của nhân vật 
```python
# Step 1: calculate would-be dx, dy when unobstructed
self.dx = 0
self.dy += GameConfig.GRAVITY

if self.moving_left:
    self.dx = -self.speed
if self.moving_right:
    self.dx = self.speed

# Step 2: update current position by the deltas
self.rect.x += self.dx
self.rect.y += self.dy

self.is_landed = False
```
Để có thể cho nhân vật đứng trên mặt đất, chúng ta thêm đoạn code sau
```python
# Step 3: Use a hardcoded ground (before next lesson)
if self.rect.bottom >= GameConfig.GROUND_LEVEL:
    self.rect.bottom = GameConfig.GROUND_LEVEL
```

## Chuyển động với hoạt họa (Cột mốc 3)

### Hoạt họa là gì?
Hoạt họa là một hiệu ứng phổ biến trong hoạt hình khi sử dụng sự thay đổi của các hình ảnh tĩnh để tạo nên hình ảnh đang chuyển động (add gif here)

### Load các sprites dùng array

```python
def _load_sprites(
        sprites_dir: Path, scale: float = 0.1
    ) -> Dict[ActionType, List[pygame.Surface]]:
    """
    Load all images from directory and convert into a Dictionary
    which maps ActionType to list of Surface
    """
    sprites: List[pygame.Surface] = []

    
    for image_file in sprites_dir.iterdir():
        image = pygame.image.load(str(image_file))

        sprites.append(util.scale_image(image, scale))
    return sprites
```

### Cập nhật index cho sprite hiện tại

```python
def render(self, screen: pygame.Surface,is_moving: Boolean, *args, **kwargs) -> None:
    """
    Redraw at every Game tick
    """
    # Change to the next sprite in the sequence corresponding to the current action
    # (note that there are multiple sequences to choose from)
    current_ms = pygame.time.get_ticks()
    if current_ms - self.last_animation_ms > self.animation_interval_ms:
        self.last_animation_ms = current_ms
        if is_moving:
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
    self.image = self.sprites[self.sprite_index]

    super().render(screen, flip_x=self.flip_x, *args, **kwargs)
```

## Hoạt họa nâng cao với nhiều hành động (Cột mốc 4)

### Dùng dictionary để lưu trữ các sprites của các hành động khác nhau
Chúng ta dùng một dictionary để lưu các sprites của các hành động, trong đó `key` là tên của hành động và `value` là một array chứa các sprites của hành động đó. Trong file `src/gui/animated_sprite.py`, chúng ta có thể sửa hàm `_load_sprites` sau thành:
```python
def _load_sprites(
        sprites_dir: Path, scale: float = 0.1
    ) -> Dict[ActionType, List[pygame.Surface]]:
    """
    Load all images from directory and convert into a Dictionary
    which maps ActionType to list of Surface
    """
    sprites: Dict[ActionType, List[pygame.Surface]] = {}

    for sprite_subdir in sprites_dir.iterdir():
        action_sprites: List[pygame.Surface] = []
        try:
            action_type: ActionType = ActionType(sprite_subdir.name)
        except ValueError as e:
            logger.warning(
                f"Unrecognized ActionType when loading from sprites_dir '{sprites_dir}': {e}"
            )
            continue

        # Read list of images & create list of sprites
        for image_file in sprite_subdir.iterdir():
            image = pygame.image.load(str(image_file))
            action_sprites.append(util.scale_image(image, scale))

        sprites[action_type] = action_sprites
    return sprites
```

### Cập nhật hành động hiện tại và index của sprite hiện tại
Thêm hàm `set_action` vào file `src/gui/animated_sprite.py`:
```python
def set_action(self, new_action) -> None:
    if self.action != new_action:
        logger.debug(f"Set action {new_action}")
        self.action = new_action
        self.sprite_index = 0
```
Trong file `src/gui/animated_sprite.py`, chúng ta có thể sửa hàm `render` sau thành:
```python
def render(self, screen: pygame.Surface, *args, **kwargs) -> None:
    """
    Redraw at every Game tick
    """
    # Change to the next sprite in the sequence corresponding to the current action
    # (note that there are multiple sequences to choose from)
    current_ms = pygame.time.get_ticks()
    if current_ms - self.last_animation_ms > self.animation_interval_ms:
        self.last_animation_ms = current_ms
        self.sprite_index = (self.sprite_index + 1) % len(self.sprites[self.action])
    self.image = self.sprites[self.action][self.sprite_index]

    super().render(screen, flip_x=self.flip_x, *args, **kwargs)
```

## Thêm hành động nhảy vào danh sách hành động (Cột mốc 5)
### Thêm event
Trong file `src/game_entities/player.py`, thêm sự kiện nhảy: 
```python
for event in self.events:
    if event.is_key_down(pygame.K_LEFT, pygame.K_a):
        self.move_left(True)
    elif event.is_key_down(pygame.K_RIGHT, pygame.K_d):
        self.move_right(True)
    elif event.is_key_down(pygame.K_UP, pygame.K_SPACE, pygame.K_w):
        self.jump()
    elif event.is_key_up(pygame.K_LEFT, pygame.K_a):
        self.move_left(False)
    elif event.is_key_up(pygame.K_RIGHT, pygame.K_d):
        self.move_right(False)
```

Trong file `src/game_entities/movable.py`, thêm hàm `jump`:
```python
def jump(self):
    if self.is_landed:
        self.is_landed = False
        self.dy = -self.jump_vertical_speed
```
### Điều khiển trạng thái nhảy
Chúng ta dùng biến `self.is_landed` trong class `MovableEntity` trong file `src/game_entities/movable.py` để kiểm tra xem nhân vật đã tiếp đất hay chưa
