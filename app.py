# Read input from command line
import sys
# Imported helper function used to find all subsets of a set
from itertools import combinations

# Reads input in the UWG format.
# Returns contants n, m and an list of lists of edges
def read_input():
    n = int(sys.stdin.readline().strip())
    m = int(sys.stdin.readline().strip())
    edges = []
    for _ in range(m):
        temp = sys.stdin.readline().strip()
        temp = temp.split(" ")
        edges.append([int(temp[0]),int(temp[1]),int(temp[2])])
    return n, m, edges

# Check if a given subgraph visits every node of its graph
def visits_all_nodes(n,m,edges,candidate):
  edgesPerNode = [0] * n
  edgesInCandidate = map(lambda i: edges[i-1], candidate)
  for edge in edgesInCandidate:
    edgesPerNode[edge[0]-1] += 1
    edgesPerNode[edge[1]-1] += 1
  return all(1 <= amount for amount in edgesPerNode)

# Normal depth first search traversal
def dfs(n, m, edges, subgraph):
  visited = []
  stack = [1]
  while stack:
    node = stack[-1]
    if node not in visited:
      visited.append(node)

    node_edges = list(filter(lambda edge: edges[edge-1][0] == node or edges[edge-1][1] == node, subgraph))
    neighbours = list(map(lambda edge: (edges[edge-1][0], edges[edge-1][1])[edges[edge-1][0]==node], node_edges))
    unvisited_neighbours = list(filter(lambda neighbour: neighbour not in visited, neighbours))

    if unvisited_neighbours:
      stack.append(unvisited_neighbours[0])
    else:
      stack.pop()
  return visited

# Check if a given subgraph is a tree, seing if dfs search visits all vertices
def is_tree(n, m, edges, subgraph):
  return len(dfs(n, m, edges, subgraph))==n

# Find all spanning trees of a given graph
# it works by
# - Finding all subsets of length n-1
# - Filtering away ones that doesn't visit all vertices
# - Filtering away all non-trees
def find_spanning_trees(n,m,edges):
  edgesets = combinations(range(1,m+1), n-1) # O(m choose n-1)
  edgesets_visiting_all = filter(lambda candidate: visits_all_nodes(n,m,edges,candidate), edgesets)
  spanning_trees = filter(lambda candidate: is_tree(n, m, edges, candidate), edgesets_visiting_all)
  return list(spanning_trees)

# Given a list of edges and a list of indices of edges in a tree
def spanning_tree_sum(edges, tree):
    return sum(edges[i-1][2] for i in tree)

# Given a list of edges and a list of indices of edges in a tree
# returns the sum of the weights of the tree's mirror subgraph
def mirror_subgraph_sum(m, edges, tree):
    return sum(edges[m-i][2] for i in tree)

# Main program
n, m, edges = read_input()
spanning_trees = find_spanning_trees(n,m,edges)
if spanning_trees:
  highest_sum = lambda tree: max(spanning_tree_sum(edges, tree), mirror_subgraph_sum(m, edges, tree))
  spanning_trees_highest_sums = list(map(highest_sum , spanning_trees))
  lowest_highest_sum = min(spanning_trees_highest_sums)
  index_of_lowest = spanning_trees_highest_sums.index(lowest_highest_sum)
  for edge in spanning_trees[index_of_lowest]:
    print(edge)
  print(lowest_highest_sum)
else:
  print("NO")