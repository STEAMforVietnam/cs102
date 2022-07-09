# Bài 2: Đường Đi Khó Khăn

> Đây là phần ghi chú và hướng dẫn cho bài học. Bạn có thể dùng nó để ôn tập và luyện tập sau giờ lên lớp.
> Chúc bạn thành công! 

## Tổng quan Git và Github

Git là công cụ giúp chúng ta quản lý các phiên bản khác nhau của mã nguồn (source code) một cách dễ dàng. 

GitHub một dịch vụ (miễn phí và có phí cho chức năng nâng cao) cung cấp bởi công ty Microsoft, nơi các lập trình viên
có thể lưu trữ và chia sẻ dự án phần mềm với nhau.

[Link tải Git](https://git-scm.com/downloads)

Repository là kho lưu trữ mã nguồn và lịch sử thay đổi (commit history). 

Để quản lý nhiều phiên bản mã nguồn, ta nhờ Git tạo và quản lý nhiều nhánh (git branch).

Mỗi repo có thể nhiều branch, thông thường sẽ có một branch chính tên là `master` hoặc `main`.

## Cách tải mã nguồn cho bài học số 2 về máy

Tải repo mới về máy lần đầu tiên (nhớ trước khi chạy lệnh, nên đứng trong một thư mục lớn bạn chuyên dùng để chứa nhiều dự án của mình):

```shell
git clone https://github.com/STEAMforVietnam/cs102.git
cd cs102  # sau khi chạy lệnh này, bạn ở trong "project root" và có thể chạy các lệnh git
```

Từ đây, có thể mở thư mục này ra trong IDE yêu thích của bạn.

Chuyển phiên bản mã nguồn sang cột mốc 0:

```shell
git checkout ls2-0
```

Chuyển phiên bản mã nguồn sang cột mốc cuối bài:

```shell
git checkout ls2-5
```

Nếu các lệnh `git checkout <tên branch>` báo lỗi và không cho bạn chuyển, hãy đọc về lệnh `git reset --hard` và thử nghiệm.

## Một số lệnh Git

> Lưu ý: phần này bạn có thể lướt qua, để tiếp tục học nội dung chính của bài học số 2 ở bên dưới. 
> Kỹ năng sử dụng Git của bạn sẽ dần thuần thục sau khi xài nó một thời gian.

Chạy các lệnh này bằng các gõ vào terminal. 

### Cơ bản
- `git clone <đường dẫn tới online repo>` : tải nguyên một dự án mới về máy của mình
- `git pull --rebase` : một thời gian sau khi clone repo, online repo có thể có nhiều commits mới, chạy lệnh này để lấy các commits mới này về máy của mình
- `git branch` : kiểm tra xem đang ở branch nào
- `git checkout <tên branch>` : chuyển sang một branch khác
- `git status` : kiểm tra trạng thái các file và folder thay đổi
- `git log` : xem lịch sử thay đổi trên branch hiện tại

### Nâng cao

- `git checkout -b <tên branch mới>` : tạo một branch mới từ branch hiện tại
- `git add <đường dẫn muốn add>` : thường chạy ngay trước khi chạy lệnh kế, chuẩn bị gom thay đổi lại
- `git commit -m <tên thay đổi>` : tạo một **commit** mới trên branch hiện tại, từ phần thay đổi đã gom thông qua lệnh `git add ...`
- (nguy hiểm) `git reset --hard` : huỷ bỏ toàn bộ những thay đổi chưa nằm trong commit nào

Đối với lệnh `git reset --hard`, bạn có thể mất phần việc đang dang dở. Lệnh này vẫn hữu dụng khi muốn chuyển qua lại
giữa các cột mốc trong bài học, đặc biệt khi bạn cảm thấy không cần lưu lại phần thay đổi thử nghiệm bạn vừa làm. 

---

# Tóm tắt nội dung bài học

## Tách nhỏ

Chúng ta có thể tách nhỏ đoạn code ra thành nhiểu file khác nhau và sau đó dùng lệnh `import` ngược lại, hệt như
cách import các hàm thư viện.

Cuối phần này, thư mục bên ngoài sẽ gồm 4 files `.py`.

### common.py

Là nơi lưu trữ những hằng số, font chữ, màu sắc, vv.
 
```python
SCREEN_WIDTH: int = 1280
SCREEN_HEIGHT: int = 768
...
```

### entities.py

Là nơi định nghĩa các lớp entity (thực thể) trong game

```python
class Player:
    ...

class Robot:
    ...

...
```

Để ý mỗi lớp entity này (các lớp `Player`, `Robot`, `NPC`) đều nắm giữ một `Surface` là hình ảnh cần vẽ, cặp toạ độ `(x, y)`
là vị trí hình ảnh trên màn hình game.

### utils.py

Là nơi mình lưu trữ một số hàm hay dùng như `scale_image` hay `overlap`.

### main.py

Chương trình chính bây giờ sẽ ngắn hơn, ở đây ta import lớp và hàm từ các file trên.

* Xem phiên bản dự án sau khi tách nhỏ: [GitHub cs102/tree/ls2-1](https://github.com/STEAMforVietnam/cs102/tree/ls2-1)
* Xem so sánh giữa trước và sau: [GitHub diff](https://github.com/STEAMforVietnam/cs102/compare/ls2-0...ls2-1)

## Thừa kế (Inheritance)

Tính năng thừa kế cho phép một lớp có thêm đặc trưng (attribute) và phương thức (method / function) từ lớp cha của nó.

Việc này giúp cho code gọn hơn và không phải lặp lại định nghĩa một hàm nhiều lần.

Cách định nghĩa quan hệ thừa kế `class <tên class con>(<tên class cha>):`

Khi lớp con có thể sử dụng phương thức lớp cha mà không cần thêm bớt gì, thì KHÔNG CẦN định nghĩa lại phương thức

Khi lớp con cần thay đổi một chút hành vi thừa kế, để chạy phần body đã định nghĩa trên lớp cha, có thể sử dụng từ khóa `super`, trong cú pháp:

```python
super().<tên phương thức>(<tham số>)
```

* Xem phiên bản dự án sau khi sử dụng tính năng thừa kế: [GitHub cs102/tree/ls2-2](https://github.com/STEAMforVietnam/cs102/tree/ls2-2)
* Xem so sánh giữa trước và sau: [GitHub diff](https://github.com/STEAMforVietnam/cs102/compare/ls2-1...ls2-2)

## Python package

Dự án lớn sẽ có nhiều thư mục con, chứa thêm nhiều file source code bên trong.

Để có thể import từ bên trong thư mục con ra ngoài, cần biến nó thành một Python package, bằng cách thêm file `__init__.py` vào thư mục.

File này có thể để trống.

* Xem phiên bản dự án sau khi tạo package `entities`: [GitHub cs102/tree/ls2-3](https://github.com/STEAMforVietnam/cs102/tree/ls2-3)
* Xem so sánh giữa trước và sau: [GitHub diff](https://github.com/STEAMforVietnam/cs102/compare/ls2-2...ls2-3)

## Tạo lớp World

Để gói gọn (encapsulation) và quản lý các game entities, ta dùng lớp `World`. Lớp này cũng hỗ trợ 2 pha mỗi game tick:

* update (tuỳ theo game logic)
* render (vẽ các entities đang quản lý lên màn hình ở vị trí thích hợp) 

**Tip:** Sau khi có lớp World, để hiện thực (implement) chức năng replay, chỉ cần kiểm tra các phím nhập bởi người chơi
và tạo lại `World` mới.

* Xem phiên bản dự án cuối bài học: [GitHub cs102/tree/ls2-5](https://github.com/STEAMforVietnam/cs102/tree/ls2-5)
* Xem so sánh giữa trước và sau: [GitHub diff](https://github.com/STEAMforVietnam/cs102/compare/ls2-3...ls2-5)

# Cấu trúc dự án cuối bài học

```shell
├── assets
│   ├── background.png
│   ├── diamond_blue.png
│   ├── diamond_red.png
│   ├── player.png
│   ├── robot.png
│   └── to_mo.png
├── readme.md
├── requirements-dev.txt
├── requirements.txt
└── src
    ├── common.py
    ├── entities
    │   ├── __init__.py
    │   ├── base_entity.py
    │   ├── game_item.py
    │   ├── player.py
    │   └── robot.py
    ├── game_status.py
    ├── main.py
    ├── utils.py
    └── world.py
```