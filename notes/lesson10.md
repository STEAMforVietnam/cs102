# Bài 10: Vượt qua đối thủ đáng gờm

> Đây là phần ghi chú và hướng dẫn cho bài học. Bạn có thể dùng nó để ôn và luyện tập sau giờ lên lớp.
> Chúc bạn thành công! 

> Để thao tác với code bài 10, bạn hãy làm theo các bước sau:
 - Tìm các `file được yêu cầu` trong từng cột mốc. 
 - Sau đó bấm tổ hợp `Ctrl+F` để tìm kiếm từ khóa `"COT MOC"`.
 - Tiếp đến bạn hãy bôi đen đoạn code bên dưới từng dòng `"<-- COT MOC X -->"` và bấm tổ hợp `Ctrl+/` để `uncomment` đoạn code.
 - Tiếp theo, xóa dòng `"<-- COT MOC X -->"`
 - Cuối cùng, sau khi đã `uncomment tất cả các file được yêu cầu`, bạn có thể chạy chương trình

## 1. Thăng cấp màn chơi (Level 2)

>Nhiệm vụ: Tạo điều kiện kết thúc màn 1, tạo màn chơi thứ hai và xử lý event để khởi tạo màn chơi mới.

B1: Khởi tạo event mới tên `LEVEL_END` trong thư mục `src/common/event.py`

```python
class EventType(enum.Enum):
    [...]

    LEVEL_END = pygame.event.custom_type()
```
B2: Truy cập `src/level_logics/one.py` để uncomment đoạn code giúp gọi event LEVEL_END cùng các đoạn code yêu cầu khác: 

```python
# After talking to this NPC (the last NPC in level 1), level 1 should end.
        if event.get_sender_id() == npc_chu_nhan_id and event.is_type(EventType.NPC_DIALOGUE_END):
            GameEvent(EventType.LEVEL_END).post()
```
Đoạn code này có nghĩa rằng khi nhân vật là Chú Nhân và Táy Máy đã kết thúc trò chuyện thì chúng ta sẽ gửi tín hiệu kết thúc level lên chương trình.

Đừng quên chuyển đổi `hàm if` bên dưới đoạn code trên thành `elif` như sau để chương trình hoạt động.
```python
        # Player finishes TRAMPOLINE quest.
        elif (
            event.get_sender_id() == npc_chu_nam_id
            and event.is_type(EventType.NPC_DIALOGUE_END)
            and world.player.count_inventory(TRAMPOLINE_PART_TYPES) >= 4
        ):
            [...]
```
B3: Tìm đến file `src/world/world_manager.py` uncomment các đoạn được yêu cầu. Trong đó, hàm `tick()` chứa đoạn code giúp chương trình chuyển đổi màn chơi kế tiếp (level hiện tại + 1) khi nhận được event `LEVEL_END`:
```python
            elif e.is_type(EventType.LEVEL_END):
                e.event.level_id = self.level_id
                if self.level_id < 10:
                    # Player finishes a main story level, go to next level
                    GameEvent(EventType.START_GAME, level_id=self.level_id + 1).post()
                else:
                    # Player finishes a bonus level, show a congrats screen
                    self.start_scene(BonusLevelEnd)

```
B4: Bổ sung thông tin màn chơi thứ hai theo các bước
- Copy file `Cot moc 1 - asset/level_2.png` vào thư mục `assets/backgrounds`
- Copy file `Cot moc 1 - asset/2.csv` vào thư mục `data/levels`

## 2. Màn chơi bổ sung (Bonus round)

>Nhiệm vụ: Thêm và khởi tạo các màn chơi phụ để trò chơi thêm đa dạng

Miêu tả: Ta có thể thoải mái sáng tạo và thêm các level mới tùy ý thích bằng cách thêm file `.png` và file `.csv` như B4 của Cột mốc 1.

Tuy nhiên, ta cần lưu ý các quy tắc sau để chương trình không gặp lỗi:
- File background phải ở định dạng `.png` và được đặt tên theo cú pháp `level_x.png` với `x là số tự nhiên lớn hơn 10`
- File CSV phải được đặt tên theo cú pháp `x.csv` với `x là số tự nhiên lớn hơn 10`
- Số thứ tự của level bổ sung phải  lớn hơn 10 do chương trình sẽ nhận diện các level bổ sung là các level  > 10 nhằm tránh gây ảnh hưởng đến trò chơi chính. Đoạn code bonus round được tìm thấy trong `src/worlds/menu.py`
```python
        extra_level_ids = [level_id for level_id in available_level_ids if level_id >= 10]
        frame.pack(
            self.menu.add.dropselect(
                title="Play Extra Levels",
                items=[(str(level_id), level_id) for level_id in extra_level_ids],
                selection_option_font_size=20,
                onreturn=lambda a, _b: GameEvent(EventType.START_GAME, level_id=a[0][1]).post(),
            )
        )
```

## 3. Hiển thị màn hình Loading

>Nhiệm vụ: Khi chuyển đổi giữa các màn chơi, ta cần hiển thị màn hình Loading để người chơi không cảm thấy bất ngờ khi chuyển đổi. Đồng thời, màn hình Loading tạo hiệu ứng sinh động cho trò chơi

B1: Truy cập: `src/config.py` uncomment các đoạn code chứa thông tin của màn hình Loading. Chúng ta có thể thay đổi tốc độ chạy của thanh Loading bằng cách thay đổi giá trị `STEP`
```python
class LevelLoadingBarConfig:
    WIDTH: int = 600
    HEIGHT: int = 100
    STEP = 3 if not GameConfig.DEBUG else 10  # how fast the loading bar goes
```
B2: Uncomment các hàm hỗ trợ hiển thị màn hình Loading trong `src/common/util.py`

```python
def draw_loading_bar(screen: Surface, loading_percent: int):
    draw_pct_bar(
        screen,
        fraction=loading_percent / 100,
        x=(GameConfig.WIDTH - LevelLoadingBarConfig.WIDTH) / 2,
        y=(GameConfig.HEIGHT - LevelLoadingBarConfig.HEIGHT) / 2,
        width=LevelLoadingBarConfig.WIDTH,
        height=LevelLoadingBarConfig.HEIGHT,
        margin=10,
        color=Color.LOADING_BAR,
    )
```
Hàm `draw_pct_bar()` sẽ vẽ lên màn hình thanh loading, bao gồm hình chữ nhật rỗng bao ngoài tượng trưng cho độ dài thanh loading và một hình chữ nhật đặc với giá trị độ dài tăng dần theo thời gian tượng trung cho tiến độ tải của trò chơi:
```python
def draw_pct_bar(screen: Surface, fraction: float, x, y, width, height, margin, color: Color):
    """
    Draw a bar at given position, filled up to the given `fraction`.
    """
    fraction = min(fraction, 1)
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    pygame.draw.rect(
        screen,
        color,
        (x + margin, y + margin, int(fraction * (width - 2 * margin)), height - 2 * margin),
    )
```
B3: Trong hàm `tick()` của `src/worlds/world.py`, uncomment đoạn code giúp gọi màn hình loading mỗi khi tạo một `World` mới (chuyển màn chơi)

```python
        if self.is_loading:
            self.loading_percent += LevelLoadingBarConfig.STEP
            util.draw_loading_bar(self.screen, self.loading_percent)
            if self.loading_percent >= 100:
                self.is_loading = False
            return True
```
## 4. Chức năng "Ném Burger"

>Nhiệm vụ: Táy Máy sẽ ném Burger để xua đi năng lượng tiêu cực trong các bóng đen. Chúng ta sẽ khởi tạo entity mới là Burger và khởi tạo chức năng "Ném" cho Táy Máy.

B1: Khởi tạo các giá trị thiết lập cho entity mới trong `src/config.py` bao gồm các giá trị cơ bản như SPEED và GRAVITY.

```python
class PlayerBulletConfig:
    SPRITE_PATH: Path = ASSET_DIR / "items" / "player_bullet.png"
    SCALE: float = 0.7
    SPEED: int = 35
    GRAVITY: int = 2
    DAMAGE: int = 10

    # initial vertical movement
    INIT_DY: int = -10

    # the time between creation and deletion of entities of this type
    TTL_MS: int = 400 * 60 // GameConfig.FPS
```

B2: Trong `src/entities/entity_factory.py`, uncomment đoạn code giúp chương trình khởi tạo entity mới là Burger của Táy Máy
```python
        elif entity_type == EntityType.PLAYER_BULLET:
            return Bullet(
                entity_type=entity_type,
                ttl_ms=PlayerBulletConfig.TTL_MS,
                x=x,
                y=y,
                init_dy=PlayerBulletConfig.INIT_DY,
                sprite_path=PlayerBulletConfig.SPRITE_PATH,
                scale=PlayerBulletConfig.SCALE,
                gravity=PlayerBulletConfig.GRAVITY,
                speed=PlayerBulletConfig.SPEED,
                damage=PlayerBulletConfig.DAMAGE,
            )
```

B3: Thêm chức năng "Ném" (throw) cho Táy Máy. Truy cập `src/entities/player.py` và uncomment các đoạn code được yêu cầu. Trong đó, đoạn code bên dưới có nghĩa là khi người chơi nhấn nút `F` sẽ kích hoạt chức năng "Ném" của Táy Máy

```python
            elif event.is_key_down(pygame.K_f):
                self._handle_throw()
```
Đoạn code tiếp theo đây là chức năng "Ném". Khi người chơi nhấn nút `F`, chương trình sẽ khởi tạo một Entity mới là Burger và đưa vào mảng các entities đang có trong `World` hiện tại. Lưu ý rằng, mỗi Burger được tạo ra là một thực thể riêng biệt, có ID riêng trong chương trình.

Khi hết thời gian tồn tại của một Burger (thời gian được cài đặt ban đầu `TTL_MS` trong `config.py`), chương trình sẽ tự xóa Burger đó khỏi danh sách các entities tồn tại trong `Worlds`
```python
    def _handle_throw(self):
        """
        Spawns a ball at Player position, around the shoulder-level.
        Set it motions to go left or right depending on the facing of Player.
        :return:
        """
        self.set_action(ActionType.THROW, duration_ms=PlayerConfig.THROW_DURATION_MS)
        ball_id = self.world.add_entity(
            EntityType.PLAYER_BULLET,
            self.rect.centerx,
            self.rect.centery - 30,
        )
```
Tùy thuộc vào hướng nhìn của Táy Máy khi ném, Burger được tạo ra sẽ liên tục di chuyển theo hướng đó. Đồng thời, do Burger cũng có giá trị `GRAVITY` (trọng lực) nên khi di chuyển ngang, Burger cũng sẽ rơi dần xuống đất tạo thành đường cong như chúng ta thấy trong thực tế:
```python
        ball = self.world.get_entity(ball_id)
        if self.get_flip_x():
            ball.move_left()
        else:
            ball.move_right()
```

## Kết quả bài học

* Ta đã biết được cách kết thúc một level và bắt đầu level kế tiếp
* Ta có thể thoải mái sáng tạo các level mới và đưa vào trong trò chơi như một bonus level
* Ta tạo được màn hình Loading khi chuyển đổi giữa các màn chơi giúp trò chơi của chúng ta thú vị và hợp lý hơn
* Ta tạo được chức năng "Ném Burger" cho Táy Máy, chuẩn bị cho nhiệm vụ chinh phục các bóng đen trong bài học sau
