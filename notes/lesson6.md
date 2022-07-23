# Bài 6: Bí Ẩn STEAM Valley

> Đây là phần ghi chú và hướng dẫn cho bài học. Bạn có thể dùng nó để ôn và luyện tập sau giờ lên lớp.
> Chúc bạn thành công! 

## 1. Ôn tập đọc hình ảnh

Ta dùng hàm thư viện `pygame.image.load` - truyền vào đường dẫn đến file hình ảnh - để đọc và lưu dữ liệu hình ảnh vào biến. Ví dụ:

```python
bg_img = pygame.image.load(ASSET_DIR / "bg.png")
```

Trong dự án, ta gọi hàm này để

* đọc hình background
* đọc hình các thực thể tĩnh (xem lớp `BaseSprite`)
* đọc hình các thực thể có cử động (xem lớp `AnimatedSprite`)

Lớp `BaseSprite` và `AnimatedSprite` đều nằm trong gói `src/gui`, là nơi chuyên trách các thao tác liên quan đến đồ hoạ game.

## 2. Vẽ thế giới

Ta dùng hàm thư viện `.blit` trên đối tượng `screen` (đối tượng này quản lý toàn màn hình game) để vẽ hình.

Trong dự án, hàm này được gọi bên trong các hàm `.render` của `BaseSprite` và `AnimatedSprite`.

Để vẽ thế giới, tức là tất cả các thực thể (entities) cùng với `Player` ta cần:

1. thiết kế thế giới (màn chơi) trong file CSV
2. quản lý, cho phép thêm (spawn) hoặc bớt (despawn) các entities này trên thuộc tính `.entities` trong lớp `World` -> đọc file CSV và spawn các entities khi `load_level`
3. vẽ lại các entities này trong mỗi game tick

Đoạn code đọc file CSV nằm trong file `src/config.py` - lưu ý đoạn code này có nhiều cú pháp Python nâng cao.
Về căn bản cần các em nắm được là nó đọc dữ liệu là các dòng số xen kẽ các dấu phẩy, vào biến `data` là danh sách 2 chiều (2-D array). 

```python
@dataclass
class WorldData:
    level_id: int
    data: Optional[List] = None

    def __post_init__(self):
        with open(DATA_DIR / "levels" / f"{self.level_id}.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            self.data = [
                [EntityType(int(tile or EntityType.EMPTY.value)) for tile in row] for row in reader
            ]
```

Đoạn code load level trong lớp `World` - đoạn code đọc dữ liệu trong danh sách 2 chiều `data` và thêm (spawn) các
entities ở toạ độ (x, y) là toạ độ tính theo pixel. Toạ độ (x, y) đc tính toán từ toạ độ (i, j) là chỉ số tham chiếu phần tử trong `data`.

```python
class World:
    def load_level(self, level_id):
        data = WorldData(level_id=level_id).data

        for i, row in enumerate(data):
            for j, entity_type in enumerate(row):
                if entity_type == EntityType.EMPTY:
                    continue
                x = j * GameConfig.TILE_SIZE
                y = i * GameConfig.TILE_SIZE
                self.add_entity(
                    entity_type=entity_type,
                    x=x,
                    y=y,
                )
```

Đoạn code vẽ tất cả các entities đang quản lý trong lớp `World` - hàm này được gọi mỗi game tick (khoảng 60 lần một giây):

```python
class World:
    def render(self, screen):
        """Render all entities."""
        self.player.sprite.render(screen)

        for entity in self.entities.values():
            # đây là dòng code dịch chuyển thế giới, sẽ được giải thích trong cột mốc kế tiếp
            entity.rect.x += self.delta_screen_offset   
            entity.sprite.render(screen)
```

## 3. Dịch chuyển thế giới

Đoạn code kiểm tra vị trí và hướng di chuyển của Player để xác định thế giới nên dịch chuyển hướng nào và bao nhiêu
pixels - mỗi game tick, Player sẽ quyết định có cần dịch chuyển thế giới theo chiều ngang hay không, và giá trị này được
tính vào biến `delta_screen_offset`, tính xong, ta gọi `self.world.update_screen_offset(delta_screen_offset)` để đối tượng
`world` biết là cần dịch chuyển các entities còn lại bao xa.

**Dịch về bên trái, để lộ thêm phần thế giới bên phải, thì `delta_screen_offset` sẽ có giá trị ÂM.
Dịch về bên phải, để lộ thêm phần thế giới bên trái, thì `delta_screen_offset` sẽ có giá trị DƯƠNG.**

```python
class Player:
    def _update_screen_offset(self):
        """Logics for horizontal world scroll based on player movement"""
        delta_screen_offset = 0

        at_right_edge = self.rect.right >= GameConfig.WIDTH
        at_right_soft_edge = self.rect.right > GameConfig.WIDTH - GameConfig.PLAYER_SOFT_EDGE_WIDTH
        at_left_edge = self.rect.left <= 0
        at_left_soft_edge = self.rect.left < GameConfig.PLAYER_SOFT_EDGE_WIDTH

        if (
            at_left_edge
            or at_right_edge
            or (at_left_soft_edge and not self.world.at_left_most())
            or at_right_soft_edge
        ):
            # Undo player position change (player walks in-place)
            self.rect.x -= self.dx
            delta_screen_offset = -self.dx

        self.world.update_screen_offset(delta_screen_offset)
```

## 4. Ngăn cản Player đi xuyên tường

Trong các thực thể di chuyển được (`MovableEntity`), trong đó có `Player` là lớp con của `MovableEntity`, ta chen thêm
**Step 2** vào trong lúc `update` các thực thể này, như đoạn code bên dưới:

```python
    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        # Knowing the current state of the subject, we calculate the amount of changes
        # - dx and dy - that should occur to the player position during this current game tick.
        # Step 1: calculate would-be dx, dy when unobstructed
        self.dx = 0
        if self.is_landed:
            self.dy = 0
        self.dy += GameConfig.GRAVITY
        if self.moving_left:
            self.dx = -self.speed
        if self.moving_right:
            self.dx = self.speed

        # Step 2:
        self._update_dx_dy_based_on_obstacles(self.world.get_obstacles())

        # Step 3: update current position by the deltas
        self.rect.x += self.dx
        self.rect.y += self.dy
```

**Step 2** sẽ ngăn cho thực thể - trong trường hợp ta quan tâm nhất, là thực thể Player - đè lên hoặc bị đè (overlap) bởi
các ô đường đi.

Nếu phát hiện đang overlap theo phương ngang, ta sửa `self.dx` trước khi nó được sử dụng ở **Step 3**.

Nếu phát hiện đang overlap theo phương dọc, ta sửa `self.dy` trước khi nó được sử dụng ở **Step 3**.

```python
    def _update_dx_dy_based_on_obstacles(self, obstacles):
        """
        Knowing the positions of all obstacles and the would-be position of this subject
        (self.rect.x + self.dx, self.rect.y + self.dy), check if the would-be position
        is colliding with any of the obstacles.
        If collision happens, restrict the movement by modifying self.dx and(or) self.dy.
        """
        # The obstacle check in the following for loop will determine
        # whether the subject is_landed, so we first reset it.
        self.is_landed = False
        for obstacle in obstacles:
            if obstacle.rect.colliderect(
                self.rect.x + self.dx,
                self.rect.y,
                self.rect.width,
                self.rect.height,
            ):
                # Hitting an obstacle horizontally, prevent horizontal movement altogether:
                self.dx = 0
            if obstacle.rect.colliderect(
                self.rect.x,
                self.rect.y + self.dy,
                self.rect.width,
                self.rect.height,
            ):
                # Hitting an obstacle vertically, reduce vertical movement:
                if self.dy < 0:
                    # the gap between player's head and obstacle above
                    self.dy = obstacle.rect.bottom - self.rect.top
                else:
                    self.is_landed = True
                    # the gap between player's feet and ground
                    self.dy = obstacle.rect.top - self.rect.bottom
```

## Kết quả bài học

Ta đã thiết kế được màn chơi số 1 trong file `1.csv`, đọc file này và spawn và render các entities lên màn hình.

Ta đã dịch chuyển được các entities này tuỳ theo vị trí và di chuyển của Player.

Ta đã ngăn không cho Player overlap với các entities là đường đi.