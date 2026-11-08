"""Key bindings for the curses interface (no curses import: works everywhere).

Movement: arrow keys, vi keys (hjkl yubn), or the numpad digits 1–9.
"""
from __future__ import annotations

# curses key codes (stable across platforms with ncurses)
KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT = 258, 259, 260, 261
KEY_HOME, KEY_END, KEY_PPAGE, KEY_NPAGE = 262, 360, 339, 338
KEY_A1, KEY_A3, KEY_C1, KEY_C3, KEY_B2 = 348, 349, 351, 352, 350  # keypad corners/centre
KEY_ENTER = 343
ESC = 27
TAB = 9

MOVE_KEYS: dict[int, tuple[int, int]] = {
    KEY_UP: (0, -1), KEY_DOWN: (0, 1), KEY_LEFT: (-1, 0), KEY_RIGHT: (1, 0),
    KEY_HOME: (-1, -1), KEY_PPAGE: (1, -1), KEY_END: (-1, 1), KEY_NPAGE: (1, 1),
    KEY_A1: (-1, -1), KEY_A3: (1, -1), KEY_C1: (-1, 1), KEY_C3: (1, 1),
}
for _ch, _d in {
    "k": (0, -1), "j": (0, 1), "h": (-1, 0), "l": (1, 0),
    "y": (-1, -1), "u": (1, -1), "b": (-1, 1), "n": (1, 1),
    "8": (0, -1), "2": (0, 1), "4": (-1, 0), "6": (1, 0),
    "7": (-1, -1), "9": (1, -1), "1": (-1, 1), "3": (1, 1),
}.items():
    MOVE_KEYS[ord(_ch)] = _d

WAIT_KEYS = {ord("."), ord("5"), ord("s"), KEY_B2}
CONFIRM_KEYS = {10, 13, KEY_ENTER, ord("f"), ord(".")}

COMMANDS: dict[int, str] = {
    ord("g"): "pickup", ord(","): "pickup",
    ord("i"): "inventory",
    ord("d"): "drop",
    ord("w"): "equip",
    ord("t"): "throw",
    ord(">"): "descend",
    ord("S"): "search",
    ord("p"): "pray",
    ord("x"): "look", ord(";"): "look",
    ord("?"): "help",
    ord("m"): "messages",
    ord("c"): "close",
    ord("H"): "scores",
    ord("T"): "timeline",
    ord("Q"): "quit",
}

HELP_TEXT = [
    "EMBERDEEP — controls",
    "",
    "Move / attack    arrows, hjkl yubn, or numpad 1-9",
    "Wait a turn      . 5 or s",
    "Pick up          g or ,",
    "Inventory / use  i, then the item's letter",
    "Drop             d, then the item's letter",
    "Equip / remove   w, then the item's letter",
    "Throw            t, then the item and a target (potions shatter)",
    "Descend stairs   >",
    "Search for traps S   (takes a turn, finds traps within 2)",
    "Pray at an altar p   (once per altar: heal + blessing)",
    "Eat / light torch  use food (%) or a torch (() from the inventory",
    "Close a door     c   (then a direction if several)",
    "Locked door (red +)  bump with an iron key (-), or bump twice to force",
    "Look around      x or ;  (Tab cycles creatures)",
    "Message history  m  (scroll with j/k, PgUp/PgDn)",
    "Hall of fame     H",
    "Run timeline     T   (depth-over-time chart + notable events)",
    "Help             ?",
    "Save & quit      Q   (the save is deleted when you load it)",
    "",
    "Targeting: move the cursor, Tab cycles enemies,",
    "Enter/f/. fires, Esc cancels.",
    "",
    "Monsters: r rat  k kobold  j jackal  i imp  s spider  m myconid",
    "          b fire beetle  h magma hound  T troll  & Ember Guardian",
    "          [B]urn [P]oison [C]onf [S]low [F]ast [z] asleep",
    "",
    "Legend:  @ you  # wall  . floor  > stairs  % corpse/food  ^ trap",
    "         \" fungus  ~ lava  _ altar  , rubble  + door  ' open door",
    "         ! potion  ? scroll  / weapon  [ armor  = ring  ( torch",
    "         * brazier (lights the area)  - iron key",
    "Unknown potions/scrolls are identified when used or thrown.",
    "",
    "Your torch burns down (smaller view) and you grow hungry over time.",
    "Level up by killing monsters: choose Vitality, Might or Guard.",
    "Goal: slay the Ember Guardian on depth 10 and take the Ember Heart (*).",
    "",
    "Press any key to return.",
]
