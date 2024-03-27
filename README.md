# 4iar-solver

The solver is used to find all the solutions of the given 4-in-a-row puzzle. This is the most stable version currently.

# How to use it?

+ Run ``python solver.py`` in the terminal
+ The default maximum search depth is 10 (win in 5).
  - It can solve most puzzles at a fast speed when maximum search depth is 10. However, it doesn't mean you can always find all the solutions if you set it as 10.
+ If you want to change the maximum search depth, edit the value of ``Max_Depth`` in ``solver.py``(line 9)
+ If you want to try it on more puzzle
  - Create a folder ``[Your_Puzzles]`` and add a file ``[YourPuzzles]/puzzles``
  - In ``[YourPuzzles]/puzzles``, you should orgnize your puzzle in this way
    + Case [Puzzle ID]:
    + black = [list of black pieces]
    + white = [list of white pieces]
    + solutions = [list of solution(first-step)]
  - You can find an example in ``shucheng_puzzles\puzzles``
  - Finally, you need to change the value of ``Puzzle_Path`` to ``./[YourPuzzles]`` in ``solver.py``(line 8)
+ If you want to do a simple test on a single puzzle, you can change the values of ``black`` and ``white`` in ``search.py``(line 171 & 172). Run ``python search.py`` in the terminal
  - If you don't want to check the complete paths, you can set ``display=True`` to ``False`` in line 176.
 
# Performance
  + On shucheng's puzzles:
    - 21.7s in average if ``Max_Depth = 5 * 2``
    - 328.6s in average if ``Max_Depth = 6 * 2``

# TODO
+ add multi-processing to speed up.
+ add args.parser for terminal users.
+ add GUI
