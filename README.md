# Travelling Salesman Problem - MST Heuristic

## Description

* solver_yours.py - main solution for travelling salesman problem using MST (Minimum Spanning Tree). According to [this](https://courses.engr.illinois.edu/cs598csc/sp2011/Lectures/lecture_2.pdf) material, the brief description of this program is:

	* Compute an MST <i>T</i> from graph <i>G</i> using [Prim's algorithm](https://en.wikipedia.org/wiki/Prim%27s_algorithm).
	* Obtain an Eulerian graph by doubling edges of <i>T</i>.
	* An Eulerian tour of <i>2T</i> gives a tour in <i>G</i>.
	* Obtain a Hamiltonian cycle by shortcutting the tour.
	* Take a route that crosses over itself and reorder it using 2-opt.
	* For more information, please refer to [this](http://www.dais.is.tohoku.ac.jp/~shioura/teaching/dais08/dais08.pdf) material. (in Japanese)
  
* adjacent.py - helper program for solver_yours.py. <br>
  This program makes an adjacent matrix from the input file. All cells are filled with Euclidean distance. 
  
## Visualiser

* The visualiser for my solution is [here](https://chiaki-i.github.io/google-step-tsp/visualizer/)
