# Emberdeep — screenshots

Real frames from the curses interface (96×30 terminal), captured while the balance bot plays seeded games. Regenerate with `python docs/make_screenshots.py`.

## Depth 1 — the Old Cellars

A fresh run (seed 42). Sidebar: HP, level and XP bars, torch and food, equipment, pack fill and what is in view.

```text
                                                                       EMBERDEEP
                                                                       Depth 1: Old Cellars

                                                                       HP 30/30
                                                                       █████████████████████
                                                                       Level 1  XP 0
                              #######                                  ▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱
                               .....                                   Power   5
                               #...#                                   Defense 1
                          #.####...#####.                              Torch   Bright
                          .......@.......                              ▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮
                          #.####.%.#####.                              Food    Full
                               #...#                                   Turn    0
                               .....                                   Pack    0/26
                              #######
                                                                       Wea: -
                                                                       Arm: -
                                                                       Rin: -

                                                                       Nothing in view

                                                                       Items in view: 1

──────────────────────────────────────────────────────────────────────────────────────────
You descend into Emberdeep. Find the stairs (>).




? for help
```

## First contact

A few dozen turns later, something has noticed us.

```text
                                                                       EMBERDEEP
                                                                       Depth 1: Old Cellars

                                                                       HP 29/30
                                                                       ████████████████████░
                                                                       Level 1  XP 36
                              #######                                  ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱
                          ..   .....                                   Power   5
                          #.#  #...#                                   Defense 1
            ###############.####...#####.                              Torch   Bright
            #..%..@......................                              ▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮
            #......########.####...#####.                              Food    Full
            #...>..#  #......###...####                                Turn    34
            #.....%#  #.................                               Pack    1/26
            ##.#.###  #......###########
             #k#.#    ####..#######                                    Wea: -
             # #.#########.........                                    Arm: -
               #...................                                    Rin: -
               ##########..,.######
                        #.,,,#                                         In view:
                        #..,.#                                         k kobold
                        #....#                                           ██████████
                        ######
──────────────────────────────────────────────────────────────────────────────────────────
You hit the kobold for 4. The kobold dies!
You strike the sleeping kobold!
You hit the kobold for 8. The kobold dies!
You strike the sleeping kobold!
You hit the kobold for 8. The kobold dies!
? for help
```

## Depth 4 — the Fungal Caves

Cellular-automata caves with glowing fungus.

```text
                                                                       EMBERDEEP
                                                                       Depth 4: Fungal Caves

                                                                       HP 39/54
                                                                       ███████████████░░░░░░
                                                                       Level 5  XP 642
                                                                       ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▱▱
                                                                       Power   7
                                                                       Defense 4
                                                           .           Torch   Steady
                                                          ""#          ▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯▯▯
                                                         ."..###       Food    Fed
                                                        .....jj##      Turn    1024
                                                        ........###    Pack    14/26
                                                        ."........##
                                                        """...@..."#   Wea: dagger
                                                        .T......."""#  Arm: chain mail
                                                        .......###".#  Rin: -
                                                        .......#    #
                                                         .......       In view:
                                                          ....[.       j jackal
                                                           ..##.         ██████████
                                                                       j jackal [z]
──────────────────────────────────────────────────────────────────────────────────────────
You hit the rat for 4. The rat dies!
You hit the kobold for 3. The kobold dies!
Pale fungus glows on the walls of a damp cave.
You descend to depth 4. The air grows hotter.
The jackal wakes up!
? for help
```

## Depth 7 — the Magma Halls

Lava pools, braziers (`*`) lighting the halls, fire beasts.

```text
##########                                                             EMBERDEEP
#........#                                                             Depth 7: Magma Halls
#........###...
#.......@'.'..i                                                        HP 80/88
#........###...                                                        ███████████████████░░
#........#                                                             Level 9  XP 2101
##########                                                             ▰▰▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱
                                                                       Power   10
                                                                       Defense 5
                                                                       Torch   Steady
                                                                       ▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯▯
                                                                       Food    Fed
                                                                       Turn    2267
                                                                       Pack    20/26

                                                                       Wea: warhammer
                                                                       Arm: chain mail
                                                                       Rin: ring of vitality

                                                                       In view:
                                                                       i ember imp
                                                                         ██████████

──────────────────────────────────────────────────────────────────────────────────────────
You pick up crimson potion (n).
Heat shimmers over rivers of molten rock.
You descend to depth 7. The air grows hotter.
You open the door.
The ember imp wakes up!
? for help
```

## Depth 10 — the Ember Guardian

The final arena: the guardian's sanctum inside a ring of lava.

```text
                        ###...#####....##########                      EMBERDEEP
          ###         ###.................##....### ###                Depth 10: Ember Heart
          #*#         ............................###*#####
         #....        ..,......#.,........................#            HP 56/112
        #......       .....#.....,.....#...................            ██████████░░░░░░░░░░░
       #.......# ..,.......................................            Level 13  XP 5152
      #........................................,...........            ▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱▱
 #####...........#............#............,........~~~~,~~            Power   13
##..........................#.........#...........~~~.....             Defense 5
#..................,.............................~~~......             Torch   Steady
##...............#.............,.................~~......              ▮▮▮▮▮▮▮▮▮▮▯▯▯▯▯▯▯▯▯▯▯
 ##...........................,......#....,.............&.             Food    Fed
##............................................#..~~........  .~~..     Turn    3914
#..........#........,...,...#.#..............,...~~~..h......~~~...    Pack    26/26
##................................................~~~.......~~~....
 ######...#.......................,.................~~~~.~~~~....#     Wea: war axe
      ##.........,...............#.#....................,...# #*#      Arm: chain mail
       ##.............................................@....#   ##      Rin: ring of vitality
        ##..........#...#...#..........,..................##
         ########..................#.....................##            In view:
                ####.#.###...........#...........#########             h magma hound
                   ##### ######*#####..###########                       ██████████
                              ###   ####                               & Ember Guardian
──────────────────────────────────────────────────────────────────────────────────────────
You pick up scroll of lightning (z).
Your pack is nearly full: 0 free slots left.
Your torch burns lower.
The Ember Guardian rises from the magma, eyes blazing!
The magma hound wakes up!
? for help
```

## The ascent screen

After a win (seed 3) the run's timeline: depth over time and the notable events. `T` shows it at any time; the morgue file has a copy.

```text
 ASCENT — the story of your victory

   1 ┤███
   2 ┤   ███████
   3 ┤          ████████
   4 ┤                  █████
   5 ┤                       ███████
   6 ┤                              █████
   7 ┤                                   ████████
   8 ┤                                           ██████
   9 ┤                                                 ███████
  10 ┤                                                        ████
     └────────────────────────────────────────────────────────────
      0                                                 3866 turns

 [ 1992] > Reached depth 6 (the Fungal Caves)
 [ 2070] x First cave troll slain
 [ 2077] + Reached experience level 9
 [ 2262] > Reached depth 7 (the Magma Halls)
 [ 2271] x First magma hound slain
 [ 2353] + Reached experience level 10
 [ 2779] + Reached experience level 11
 [ 2789] ! Identified the fireball scroll
 [ 2808] > Reached depth 8 (the Magma Halls)
 [ 3205] > Reached depth 9 (the Magma Halls)
 [ 3225] + Reached experience level 12
 [ 3598] + Reached experience level 13
 [ 3627] > Reached depth 10 (the Ember Heart)
 [ 3793] & The Ember Guardian entered phase 2
 [ 3803] & The Ember Guardian entered phase 3
 [ 3846] ! Identified the speed potion
 [ 3847] ! Identified the fire potion
 [ 3848] ! Identified the greater healing potion
 [ 3864] & Slew the Ember Guardian
 [ 3864] + Reached experience level 14
 [ 3866] ! Took the Ember Heart
 [ 3866] * Carried off the Ember Heart. VICTORY!


 Press any key.
```

## Text mode

`python -m emberdeep --text` — the fallback interface for terminals without curses.

```text
                              #######
                               .....
                               #...#
                          #.####...#####.
                          .......@.......
                          #.####.%.#####.
                               #...#
                               .....
                              #######









HP 30/30 [##########]  Pow 5 Def 1  Depth 1  Lv 1 XP 0  Turn 0
Torch Bright  Food Full  [the Old Cellars]
----------------------------------------------------------------------
You descend into Emberdeep. Find the stairs (>).
```
