# Emberdeep screenshots

Captured from the real curses UI with `python -m emberdeep.screenshot` (seed 7, after 900 balance-bot actions; colours not shown).

## Exploring

The map, the sidebar (HP, XP, torch, food, load, gear, monsters in view) and the message log.

```
######  #..,..#  ########        #....#  ########....#  #,,,#   #...#  EMBERDEEP
#....#  #.,,,.#  #......#  ##### #....####...........####.,.#####...#  Depth 3: Old Cellars
#....####..,..####......####...###..........................'...'...#
#....'........'..'.........'...'.'..................#####...#####...#  HP 38/54
#....####.....####......####...####################.#   ##.##   #####  ███████████████░░░░░░
#....#  #.....#  ####.###  #...#                  #.#    #.#           Level 5  XP 618
######  #######     #.#    #...#                  #.# ####'###  #####  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱
                    #.#    #...#             ######'# #......#  #.^.#  Power   7
         ####    ####'###  ##.##             #......# #......####...#  Defense 4
         ......###*##...#   #.#           .###......###.........#...#  Torch   Steady
         ......'....'^..#   #.#          ....'......'.'.............#  ▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯
         ......######...#                ..###......###......##.#...#  Food    Fed
         ....       ##'##                    ######.# #########.#...#  Load    61/64
         .           #.#                          #.#         #.#...#  Pack    12/26
                     #.#                          #.#         #.#####  Turn    900
                     #.#                          #.#         #%#
        #####  #######.#                          #.#     #####'#####  Wea: dagger
 #      #...#  #.......#                          ...     #...@.....#  Arm: chain mail
 #..,,###...####.......#                                .......>....#  Rin: -
 #...,'.'......'.......#                                ............#
 #....###...####.......#                                #############  Nothing in view
 #      #####  #########

──────────────────────────────────────────────────────────────────────────────────────────────
You pick up scroll labelled "GORHUL" (l).
You pick up milky potion (m).
The scroll erupts into a roaring fireball!
You are singed by your own fireball for 5!
The scroll labelled "GORHUL" was a scroll of fireball.
? for help
```

## Inventory

Letters a–z; unidentified potions and scrolls show their random appearance.

```
######  #..,..#  ########        #....#  ########....#  #,,,#   #...#  EMBERDEEP
#....#  #.,,,.#  #......#  ##### #....####...........####.,.#####...#  Depth 3: Old Cellars
#....####..,..####......####...###..........................'...'...#
#....'........'..'.........'...'.'..................#####...#####...#  HP 38/54
#....####.....####......####...####################.#   ##.##   #####  ███████████████░░░░░░
#....#  #.....#  ####.###  #...#                  #.#    #.#           Level 5  XP 618
######  #######     #.┌─────────────────────────────────────────────────┐▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱▱▱
                    #.│ Use which item?                                 │wer   7
         ####    ####'│                                                 │fense 4
         ......###*##.│ a) ! 4 potions of healing  — heals 12           │rch   Steady
         ......'....'^│ b) ( torch  — +700 torch fuel                   │▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯
         ......######.│ c) [ leather armor  — +1 defense                │od    Fed
         ....       ##│ d) % food ration  — +1200 food                  │ad    61/64
         .           #│ e) / dagger (equipped)  — +1 power, +3 thrown   │ck    12/26
                     #│ f) [ chain mail (equipped)  — +2 defense        │rn    900
                     #│ g) [ leather armor  — +1 defense                │
        #####  #######│ h) ! glowing potion  — unidentified             │a: dagger
 #      #...#  #......│ i) ! icy potion  — unidentified                 │m: chain mail
 #..,,###...####......│ j) ? scroll of teleportation  — random teleport │n: -
 #...,'.'......'......│ k) [ leather armor  — +1 defense                │
 #....###...####......│ l) ! milky potion  — unidentified               │thing in view
 #      #####  #######│                                                 │
                      │ Press a letter, or Esc to cancel.               │
──────────────────────└─────────────────────────────────────────────────┘─────────────────────
You hit the rat for 4. The rat dies!
You pick up scroll labelled "GORHUL" (l).
You pick up milky potion (m).
The scroll erupts into a roaring fireball!
You are singed by your own fireball for 5!
The scroll labelled "GORHUL" was a scroll of fireball.
```

## Run timeline (`T`)

Depth over time plus notable events — also shown after every run.

```
 EMBERDEEP — your run so far

   3 |                               █████████████████████████████
     |                ████████████████████████████████████████████
   1 |████████████████████████████████████████████████████████████
     +------------------------------------------------------------
      0                                                   turn 900

 Turns per depth: D1:238  D2:222  D3:440
 [   21] D1  ! first kobold slain
 [   37] D1  ! first rat slain
 [   37] D1  + reached experience level 2
 [  356] D2  ! first jackal slain
 [  380] D2  + reached experience level 3
 [  474] D3  ! first cave spider slain
 [  589] D3  ! first ember imp slain
 [  600] D3  + reached experience level 4
 [  684] D3  + reached experience level 5
 [  716] D3  ! first fire beetle slain

 Press any key.
```
