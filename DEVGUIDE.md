# STEAM Valley - Developer's Guide

## The game loop - how it works

We set `GameConfig.FPS = 60`, so a game loop (a tick) runs every 1/60 seconds.

The life of 1 game loop:

`main.py`
-> call `world_manager.tick()`
-> get all `events` from Event Queue, call `active_world.tick(events)`

During the execution of `active_world.tick(events)`, you'll see 2 phases:

1. Update: call `.update()` on all entities objects managed by the instance (object) of class `World`
2. Render: call `.render()` on all such entities

## Sound Effects and Music

Sound effects are in `assets/sounds/effect/<entity-type-name>_<event-type-name>.wav`

for example: `.../player_hurt.wav`

Background musics are in `assets/sounds/background/level_<level-id>.wav`
for example: `.../level_1.wav`.

Implementation: https://github.com/STEAMforVietnam/steamvalley/pull/129

## How to build

### Build a new feature

![highlevel](https://user-images.githubusercontent.com/52057040/178127952-4e80005c-ebe0-4272-9cb4-12a8ec9e1316.jpg)

`.update()` and `.render()` are already being called at the right time right place, you most likely do not need to call
them in your additional code. If you have a child class overriding these methods, you need to keep the signature the same,
and you need to call the parent's method, for example `super().update(events, world)` should be in the body `Player.update`.

Think of which entities are involved.

  * If only one type is in concerned, your logic should be added to that entity class in the `.update` method.
  * If there is some interaction,  for example between Player and a Shadow, in addition to adding logic to various `.update` methods on entity classes, you will post and handle events through the Event Queue (see example #2 below).
    * Pay some attention to `level_logics/__init__.py` and `level_logics/one.py` for how custom level logics - based on the game story - are implemented.

### Build a whole new level

You would add file `<int>.csv` to `data/levels/`, add file `level_<int>.png` to `assets/backgrounds/`.

When designing the CSV file, to know the correct column numbers (CSV indices) as displayed on the game screen,
turn on `GameConfig.DEBUG` flag in `config.py`, so you'll get the bottom row of blue numbers:

![level_design_blue_column_guide](https://user-images.githubusercontent.com/52057040/181862497-81ebb970-d989-49dd-a9eb-7b1c31d8b19c.png)

For you new level:

* either treat it as a bonus level (like a minigame), if so, use some level ID value > 10.
* or maybe you want it as part of the main story, then the level ID value should be somewhere in the sequence 1 -> 9.

Tips:

You can add the flag (`LEVEL_END_FLAG = 99`) to the CSV at the end of the level, so when the player collects that flag,
the level ending routine is triggered.

## Examples

**Example 1**:

User hits K_SPACE, `WorldManager` passes this event all the way to the object of class `Player`.

During `update` phase, `player.rect` is set to new coordinates and `player.sprite` is set to the jumping image.

During `render` phase, the jumping image is drawn at the new coordinates.

Take a quick look at the actual code for `Player.update` that call other private methods to update its positions and sprite.

```python
    def update(self, events: Sequence[GameEvent], world: World) -> None:
        super().update(events, world)
        self._update_npc_near_by()
        self._handle_events()
        self._update_screen_offset()
```

---

**Example 2**

User hits activation key "e" when Player is standing next to an NPC.

`WorldManager` passes this event all the way to the object of class `Player`.

During `update` phase, Player object will then post (broadcast to the Event Queue) a custom event `PLAYER_ACTIVATE_NPC`:

```python
GameEvent(EventType.PLAYER_ACTIVATE_NPC, listener_id=self.npc_near_by.id).post()
```

During `render` phase, nothing happens yet.
IN THE NEXT TICK, the posted event is collected by `WorldManager`, which then passes it on to all entities including the
objects of class `FriendlyNpc`. However, only the object with id equals to the `event.get_listener_id()` will act upon
this `PLAYER_ACTIVATE_NPC` event.

The object of class `FriendlyNPC` instructs the current `world` (object of class `World`) to add the dialogue box to
list of managed entities.

```python
self.world.add_entity(EntityType.DIALOGUE_BOX)
```

TO SUM UP, if player "activates" a friendly NPC during tick X, then in the render phase of tick X+1, the dialogue box
is rendered.

---


## Tips

### Use mypy for static type checking

Call it with the root of src dir:

```shell
mypy src
```

**It will show you all the typing errors. Please attempt to fix as much as possible
(we do NOT enforce zero error yet).**

### Code Linter

We use [black](https://black.readthedocs.io/en/stable/) and [flake8](https://flake8.pycqa.org/)
to keep the code easy to read and adhere to Python guidelines.

`black` can be run like this:

```shell
$ black src
reformatted src/common/util.py
reformatted src/game_entities/base_entity.py
reformatted src/game_entities/movable_entity.py
reformatted src/game_entities/animated_entity.py

All done! ✨ 🍰 ✨
4 files reformatted, 7 files left unchanged.
```

It will also run automatically whenever you do `git commit` as a pre-commit hook.
If either `black` or `flake8` fails to auto-format your code, you need to go fix the format errors before continue.

### Instead of `print`, use standard `logging` library.

To turn on verbose debug logging, in `src/config.py`:

```python
class GameConfig:
    DEBUG: bool = True
```

Add these lines at the beginning of src code file:

```python
from common.util import get_logger

logger = get_logger(__name__)
```

Use the `logger`:

```python
logger.debug(...)  # this will only shows with GameConfig.DEBUG == True
logger.info(...)
logger.warning(...)
```
