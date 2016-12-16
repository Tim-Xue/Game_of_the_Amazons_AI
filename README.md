# Game of the Amazons Autoplayer AI - (GA-AI)
* @author Anthony (Tony) Poerio
* @email tony@tonypoer.io

## Overview
**GA-AI** is an Artificial Intelligence project whose purpose to competitively play the board game called "Game of The Amazons" automatically, via an Artificially Intelligent Agent.
For more info on "Game of The Amazons" itself, see: https://en.wikipedia.org/wiki/Game_of_the_Amazons

The Project is Divided into two parts. Information About each is found in the respective section, below.

## PART I
Part I of the part project is to  implement the Minimax search algorithm--both WITH and WITHOUT Alpha-Beta Pruning.

* Info on **Minimax**: https://en.wikipedia.org/wiki/Minimax
* Info on **Alpha-Beta Pruning**:  https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

### Source Code
The source code for part 1 can be found in the file named: "minimax_a_b.py"

### Running the program
To run the program for part 1, simply type:

`python minimax_a_b.py [config file]`

Config files must be in the following format:

`['A', ['B', ('D', 3), ('E', 5)], ['C', ['F', ['I',('K',0), ('L', 7)],('J',5)], ['G', ('M',7), ('N',8)], ('H',4)]]`

Where tuples are the leaf nodes, and the second value in each tuple is the node value at the leaf.

### Example
To run Part I on each test tree, copy and paste these lines:
`python minimax_a_b.py test_trees/test_tree1`

`python minimax_a_b.py test_trees/test_tree2`

`python minimax_a_b.py test_trees/test_tree3`
### Architecture
This program works by first constructing a tree from the data in the input file. And this section is found in the "Parse Data" section of the source code.

This tree is then passed to the Minimax and Minimax-AlphaBeta functions, and the output of each search algorithm is displayed as the data computed.


### Transcripts
The transcripts for this section can be found in this folder, along the path:
`/transcripts/part1`

There are 3 files TOTAL in this folder. One for each example provided.

### Report
The report for this section is found starting on the **first page** of the document located at:
`/reports/ADP59-CS1571-HW02-REPORT.pdf`

### Version
This source code is written using python version 2.7.8

--

## PART II
Part II of the project is use the minimax algorithms we have developed in Part I as the basis for an AI-Agent that automatically plays the board game called "Game of the Amazons"

### Source Code
The source code for my agent can be found in two files.

* 'adp59_minimax.py' -- this is the main source file for my agent. It loads in the data, parses it, builds a search tree, and then performs a search on that tree using **Minimax with alphabeta pruning**
* 'amazons27v3.py'
    - Within this file, see the function named **adp59**
    - @adp59 is the function which you will need to call within the game class itself. This function MUST be represented in whatever is the final version of the game that you are testing.
    - Note: @adp59 calls functions from the 'adp59_minimax.py' source file, so this file **MUST BE IMPORTED** into your final project for the agent to work correctly.

### Running the Program
To run the program, simply:
* Copy this whole folder down to your computer (git clone will work)
* Run the command:
`python amazons27v3.py`
* Type in the name of the .config file you intend to use, when prompted.
* .config files MUST be in the following format:  
[line 1 - seconds for the autoplayer to make its decision]  
[line 2 - size of the board]  
[line 3 - player 1]  
[line 4 - locations of player 1's queens]  
[line 5 - player 2]  
[line 6 - locations of player 2's queens]  

* Here's an example for a 5x5 board.
15  
5  
human  
c4 e2  
adp59  
c0 a2  


### Notes
I have a series of .config files that I used to test the program, feel free to use them. In practice, using more than 3 queens on a 7x7 board will take to long to be practical for this program. A future goal would be to optimize for speed on large boards, but it works as expected on a smaller input size

### Architecture
Just like part 1, this program works by:
* Taking in the board position
* Finding locations of all queens
* Finding all possible moves they can make
* Constructing a search tree down 2-ply ahead
* Running a Minimax-AlphaBeta Search on that search tree
* Getting the optimal move (based on whichever heuristic value function is defined)
* Making the optimal move

### Value Function
For the value function, I decided optimize and always pick the move which results in the HIGHEST NUMBER of Available spaces for the autoplayer.

Notes:
* I also tried to minimize the opponent's spaces, but this caused the player to be too aggressive and make more dumb moves.
* The current version plays defensively, and against a human who is aggressive, it will usually lose -- but against another autoplayer, I'd expect it to perform relatively well. It plays with its own best interest in mind.
* The value function heuristic can be be altered in the **GameNode class** within the @getValue function of 'adp59_minimax.py'

### Transcripts
The transcripts for this section can be found in this folder, along the path:
`/transcripts/part2`

I've included transcripts of both autoplayers tested -- one which plays offensively, and one which plays defensively.

Each set of transcripts can be found it its own respective subfolder.

I also split up the tests by board-size and player type (B or W).


### Report
The report for this section is found starting on the **first page** of the document located at:
`/reports/ADP59-CS1571-HW02-REPORT.pdf`

### Version
This source code is written using python version 2.7.8

--


## Prerequisities

This project depends upon Python v. 2.7.8

I am also using the **itertools** python library

You must also have the config files you intend to read from in the same directory as the source code

## Built With

* Python v. 2.7.8
* PyCharm

