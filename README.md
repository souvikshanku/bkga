Solving  Binary Knapsack Problem using Genetic Algorithm

## Problem Statement

Given a set of $n$ items with weights $\{ w_1, w_2, ..., w_n \}$ and values $\{ v_1, v_2, ..., v_n \}$ with maximum capacity $W$, 

maximize $\sum_{i=1}^n v_ix_i$

subject to, $\sum_{i=1}^n w_ix_i \le W$, where $x_i \in \{0, 1\} \forall i$

Here $x_i$ represents the number of instances of item $i$ to include in the knapsack.


## Usage
```console
$ git clone https://github.com/souvikshanku/bkga.git
$ python population.py
```