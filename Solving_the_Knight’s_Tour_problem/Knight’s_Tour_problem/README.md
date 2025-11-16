# The-Knight-s-Tour-problem-using-a-genetic-algorithm
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)

<img height="200" alt="knights" src="https://th.bing.com/th/id/R.314a9194f7a96c3906b196145d5fd2be?rik=2eKU667bP2MRyw&riu=http%3a%2f%2fmedia.moddb.com%2fimages%2fgames%2f1%2f61%2f60096%2fGameLogoBckg.png&ehk=RaL0%2f8IAzvllAM2T%2f6WMVCUPJopruIaZz2glunMpS%2f8%3d&risl=&pid=ImgRaw&r=0" width="100%"/>


The knight can move to the square marked in red and then repeat the process on the new square.
A **knight's tour** is a sequence of moves where the knight visits every square on the chessboard exactly once.

---
## 📖 Table of Contents

- [Objective](#-Objective)
- [How to Use](#-How-to-Use)
- [1. Chromosome Class](#-1.-Chromosome-Class)
- [2. Knight Class](#-2.-Knight-Class)
- [3. Population Class](#-3.-Population-Class)
- [4. Main Function](#-4.-Main-Function)

---

## Objective

The goal of this assignment is to solve the knight's tour problem using a **genetic algorithm** by creating the following classes:

---
## 🎮 How to Use

After launching the application, you will see the main window. 
<table>
  <tr>
    <td width="100%" align="left">
      <img src="./assets/main.png" alt="Screenshot of the loading" width="100%"/>
    </td>
  </tr>
</table>

This application offers two main modes: playing pre-designed **Default** position of knight is (0,0)

### Playing a Default Mode

**1. Select Game Mode**
After launching the application, you will see the main menu. Click the **Play** button.

<p align="center">
  <img src="./assets/choose_position.png" alt="Map type selection after clicking Play" width="50%">
</p>

**a. Choose a Level**
Next, pick a position of x and y (0 - 7).

<p align="center">
  <img src="./assets/choose_position.png" alt="Map type selection after clicking Play" width="50%">
</p>

**3. Preview the animation**
 If you're ready, click **play**.

**5. View the Results**
Once solved, a victory pop-up will display the performance statistics for the run, such as time, memory usage, and steps taken. 
<table>
  <tr>
    <td width="50%" align="left">
      <img src="./assets/res.png" alt="Screenshot of the failure" width="100%"/>
    </td>
    <td width="50%" align="right">
      <img src="./assets/res_1.png" alt="Screenshot of the victory" width="100%"/>
    </td>
  </tr>
</table>
---
## 1. Chromosome Class

In the knight's tour problem, the **moves made by the knight** represent the genes of the chromosome.

**Attributes:**

* `genes`: an array of length 63 representing the knight's moves. Each gene corresponds to one of the 8 possible moves.

**Functions:**

* `__init__(genes)`:
  Creates a new chromosome. If no genes are provided (as in the initial population), it generates a random set of genes.

* `crossover(partner)`:
  Combines genes from this chromosome and another (`partner`) using **single-point crossover** to create new offspring.

* `mutation()`:
  Introduces mutations by randomly changing some genes with a certain probability, helping the genetic algorithm explore new moves.

---

## 2. Knight Class

Each knight stores the following:

* `position`: coordinates `(x, y)` for the knight's current position.
* `chromosome`: sequence of moves taken by the knight.
* `path`: list of knight's positions after applying moves from the chromosome.
* `fitness`: fitness value, with a maximum of 64 (total squares on the chessboard).

**Functions:**

* `__init__(chromosome)`:
  Creates a new knight. If no chromosome is provided, generates a new one. Sets the initial position to `(0, 0)`, fitness to 0, and saves the initial position in `path`.

* `move_forward(direction)`:

  Moves the knight in one of 8 directions:

  <div style="display: flex; align-items: center; gap: 20px;">
    <img src="https://github.com/user-attachments/assets/f1114825-b354-4484-a29f-92aecb3727f5" alt="Knight Moves" style="max-width: 200px; height: auto; border-radius: 8px;">

    <ol>
      <li>up-right</li>
      <li>right-up</li>
      <li>right-down</li>
      <li>down-right</li>
      <li>down-left</li>
      <li>left-down</li>
      <li>left-up</li>
      <li>up-left</li>
    </ol>
  </div>

  Computes the new position after the move.
* `move_backward(direction)`:
  Reverts the knight’s position if the move was illegal.

* `check_moves()`:
  Checks validity of each move in the chromosome. A move is invalid if it places the knight outside the board or on a previously visited square.
  If invalid, cancels the move using `move_backward()` and tests other moves by cycling forward or backward.
  The cycling direction is chosen randomly at the start and remains consistent for the entire chromosome.

  * **Forward cycle example:** For current move `4 (down-right)`, the order to test is:
    5 (down-left), 6 (left-down), 7 (left-up), 8 (up-left), 1 (up-right), 2 (right-up), 3 (right-down)
  * **Backward cycle example:** For current move `4 (down-right)`, the order to test is:
    3 (right-down), 2 (right-up), 1 (up-right), 8 (up-left), 7 (left-up), 6 (left-down), 5 (down-left)
    If no valid move is found, the last move is retained.

* `evaluate_fitness()`:
  Calculates the fitness by iterating through the knight’s path and counting valid visited squares until an invalid move is encountered.
  Fitness is 64 if all squares are visited.

---

## 3. Population Class

Represents a group of knights.

**Attributes:**

* `population_size`: e.g., 100.
* `generation`: number of generations (initially 1).
* `max_generation`: number of generations maximal 1000 .
* `knights`: list of knights in the population.
* `mutation_rate`: e.g., 15%.

**Functions:**

* `__init__(population_size)`:
  Initializes the population with knights and sets generation to 1.

* `check_population()`:
  Loops through all knights and checks their moves’ validity using `check_moves()`.

* `evaluate()`:
  Evaluates the fitness of every knight using `evaluate_fitness()`. Returns the best knight and its fitness.

* `tournament_selection(size)`:
  Selects parents for crossover using tournament selection with sample size `n` (e.g., 3).
  Randomly samples `n` knights and selects the two best based on fitness.

* `create_new_generation()`:
  Creates a new population of the same size. For each pair of offspring:

  * Select parents with `tournament_selection(size)`.
  * Generate offspring via `crossover(partner)` on their chromosomes.
  * Apply `mutation()` to offspring chromosomes.
  * Increment generation count.

---

## 4. Main Function

Runs the genetic algorithm and displays the optimal solution through a graphical interface.

