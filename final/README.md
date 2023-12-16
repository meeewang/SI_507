# SI 507: Final Project: A College Application Recommender

The recommender is based on an undirected graph where each node
is one charactertisitc of the institution and each edge is an 
institution. An edge connects two nodes if an institution shares
the two charactertistics corresponding to the nodes. 

The adjacency matrix of the graph is the matrix where element (i,j)
is the number of edges connecting nodes i and j, i.e. the number of
movies that both i and j have acted in.

It follows that the square of the adjacency matrix is a matrix where
element (i,j) is the number of paths of length 2 connecting nodes i
and j. In general, the Nth power of the adjacency matrix gives the
number of paths of length N connecting any two nodes. Note that the
adjacency matrix is symmetric and so are higher powers of it.

When users are asked to provide two institions of their preference, a 
list of institutions will be generated to users which connect to these 
two nstitutions most.

**NOTE:** This runs horribly slow.

