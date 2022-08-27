# Bài 11: Năng Lượng Hạnh Phúc

# 1. HP cho người chơi

> Mục tiêu: Thêm máu (HP) cho người chơi, nếu người chơi chạm phải `Shadow` thì mất máu

> Branch: [ls11-1](https://github.com/STEAMforVietnam/cs102/tree/ls11-1)

> Compare: [ls11-zero => ls11-1](https://github.com/STEAMforVietnam/cs102/compare/ls11-zero...ls11-1)

Bước làm:
- B1: Thêm thông số (configuration) - `PlayerHPConfig` và `MAX_HP` của `PlayerConfig`
- B2: Thêm thuộc tính `self.hp` cho `Player`
- B3: Thay đổi phương thức `render` của `Player` để vẽ thêm trái tim
- B4: Thêm phương thức `_handle_get_hit` để kiểm tra người chơi có đụng bóng ma hay không
- B5: Thêm phương thức `_take_damage` để tính toán lại HP của người chơi

# 2. Restart Level

> Mục tiêu: nếu người chơi mất hết máu thì khởi tạo lại level hiện tại

> Branch: [ls11-2](https://github.com/STEAMforVietnam/cs102/tree/ls11-2)

> Compare: [ls11-1 => ls11-2](https://github.com/STEAMforVietnam/cs102/compare/ls11-1...ls11-2)

Bước làm:
- B1: Gọi phương thức `.die()` khi `hp` về 0 (inhert từ `MovableEntity`)
- B2: Tạo scene `Defeated` - viết text lên màn hình và gửi `EventType.RESTART_LEVEL` sau 4 giây
- B3: Nhận event `EventType.DIE` từ `EntityType.PLAYER` ở `WorldManager` và chuyển cảnh sang scene `Defeated`

# 3. ShadowBoss
## 3.1 Render ShadowBoss

> Mục tiêu: Vẽ được ShadowBoss và HP bar cho ShadowBoss

> Branch: [ls11-3.1](https://github.com/STEAMforVietnam/cs102/tree/ls11-3.1)

> Compare: [ls11-2 => ls11-3.1](https://github.com/STEAMforVietnam/cs102/compare/ls11-2...ls11-3.1)

Bước làm:
- B1: Tạo Entity mới tên `ShadowBoss` kế thừa từ Entity `Shadow`
- B2: Overwrite phương thức `render` để vẽ thêm HP Bar
- B3: Thêm Entity mới vào game. Theo 4 bước học ở bài số 9 // cột mốc 2
    > - B1: Định nghĩa Entity Type
    > - B2: Tạo lớp riêng cho thực thể mới
    > - B3: Khai báo thông số cơ bản trong config.py
    > - B4: Khai báo thực thể mới trong entity_factory.py
- B4: Cập nhật lại vị trí `ShadowBoss` xuất hiện trong level (`3.csv`)

## 3.2 Victory khi diệt được ShadowBoss

> Mục tiêu: Giảm ShadowBoss HP khi trúng đạn của người chơi, và hiện scene Victory sau khi tiêu diệt được boss

> Branch: [ls11-3.2](https://github.com/STEAMforVietnam/cs102/tree/ls11-3.2)

> Compare: [ls11-3.1 => ls11-3.2](https://github.com/STEAMforVietnam/cs102/compare/ls11-3.1...ls11-3.2)

Bước làm:
- B1: Tạo event mới `VICTORY` và `BOSS_DIE`
- B2: Thêm phương thức `_handle_get_hit` ở class `ShadowBoss` để kiểm tra xem boss có trúng đạn của người chơi hay không
- B3: Thêm phương thức `_take_damage` ở class `ShadowBoss` để trừ boss HP khi trúng đạn, và trigger `.die()` khi hết máu
- B4: Bắn event `VICTORY` sau khi boss đã chết (phương thức `.die` kết thúc)
- B5: Tạo Scene `Victory` và reset game / chuyển cảnh về `Menu` sau 4 giây (dùng event `SHOW_MENU_AND_RESET_LEVEL_ID`)
- B6: Nhận event `VICTORY` và chuyển cảnh sang scene `Victory`

# 4 Boss Fight

## 4.1 Angry Boss shoot bullets

> Mục tiêu: Cứ mỗi 7s, làm cho `ShadowBoss` tức giận (Angry) và bắn đạn ra nhiều hướng trong vòng 2s

> Branch: [ls11-4.1](https://github.com/STEAMforVietnam/cs102/tree/ls11-4.1)

> Compare: [ls11-3.2 => ls11-4.1](https://github.com/STEAMforVietnam/cs102/compare/ls11-3.2...ls11-4.1)

Bước làm:
- B1: Tạo thêm ActionType `ANGRY` ở `src/common/types.py`
- B2: Tạo thêm EntityType `SHADOW_BULLET` ở `src/common/types.py`
- B3: Thêm thông số liên quan đến chế độ `ANGRY` cho `ShadowBoss` và `ShadowBullet`
- B4: Thêm `ShadowBullet` vào `EntityFactory`
- B5: Ở `ShadowBoss`, mở rộng phương thức `update` để chuyển `ShadowBoss` sang chế độ `ANGRY` mỗi 7 giây
- B6: Thêm phương thức `_shoot_bullet` để `ShadowBoss` bắn đạn đi khắp nơi. Sau đó gọi phương thức này khi ShadowBoss bắt đầu sang chế độ `ANGRY`


## 4.2 Hurt State

> Mục tiêu: Trường hợp `Player` hoặc `ShadowBoss` trúng đạn, render bằng 1 sprite mới trong 1 khoảng thời gian nhất định

> Branch: [ls11-4.2](https://github.com/STEAMforVietnam/cs102/tree/ls11-4.2)

> Compare: [ls11-4.1 => ls11-4.2](https://github.com/STEAMforVietnam/cs102/compare/ls11-4.1...ls11-4.2)

Bước làm:
- B1: Thêm event `HURT` ở `src/common/event.py`
- B2: Tạo thêm ActionType `HURT` ở `src/common/types.py`
- B3: Thêm thông số liên quan đến chế độ `HURT` cho `ShadowBoss` và `Player`
- B4: Thêm `ActionType.HURT` vô `AnimatedEntity`
- B5: Thêm phương thức `start_hurt(duration_ms)` vào `AnimatedEntity` để có thể bật chế độ HURT cho 1 khoảng thời gian nhất định
- B6: Gọi phương thức `start_hurt` ở class `Player`, `Shadow`, `ShadowBoss` mỗi Entity tương ứng khi mất máu
