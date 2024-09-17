# automated-reasoning

## Intro for Forth problem

Generally, when writing a program, it needs to be executed to eventually arrive at a solution. This means the program reads input values and assigns them to variables. But what if someone wants to check if the program is feasible, determine when it is feasible, and explore all possible paths—not just the reachable ones? This is where symbolic execution comes into play.
   
Symbolic execution was originally proposed in the 1970s [CITATION HERE]. However, it relied on automated theorem-proving and did not become widely used immediately. Today, it is employed in a wide variety of modalities, including program analysis, testing, and reverse engineering.

The following problem is strongly related to this matter since we need to explore all possible program paths and then use a solver to determine for which values of n the crash condition can or cannot be satisfied.  
