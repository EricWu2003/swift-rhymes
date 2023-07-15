from pyvis.network import Network
from os import path
import os
import sys

LYRICS_DATA_DIR = "lyrics_data"
ALBUMS = ("01_Taylor_Swift", "02_Fearless", "03_Speak_Now")



# A connection is a tuple of a string and a frozenset. 
# for example: ("Tim Mcgraw", frozenset({"shined", "night"})) which means that "shined" and "night" rhymes in the song "Tim Mcgraw"
# connections is a set of such tuples.
connections = set()



for album in ALBUMS:
  curr_path = path.join(LYRICS_DATA_DIR, album)
  for filename in os.listdir(curr_path):
    with open(path.join(curr_path, filename)) as f:
      album = f.readline().strip()
      song_title = f.readline().strip()
      for line in f.readlines():
        line = line.strip()
        if line == "":
          continue

        words = list(map(lambda x: x.strip(' '), line.split(',')))
        assert(len(words) > 1)

        # add a connection for each pair of words on a same line
        # so if a line has n words, then we add (n choose 2) connections
        for i in range(0, len(words)):
          for j in range(i+1, len(words)):
            word1 = words[i]
            word2 = words[j]
            connections.add((song_title, frozenset((word1, word2))))






added_nodes = set()
net = Network()

edges_to_add = {}

for connection in connections:
  song_title = connection[0]

  if len(list(connection[1])) == 1:
    # in the data, we have some words that rhyme with themselves
    continue

  word1, word2 = list(connection[1])
  e = connection[1]

  if word1 not in added_nodes:
    added_nodes.add(word1)
    net.add_node(word1)
  if word2 not in added_nodes:
    added_nodes.add(word2)
    net.add_node(word2)
  
  if e in edges_to_add.keys():
    edges_to_add[e] = edges_to_add[e] + '\n' + song_title
  else:
    edges_to_add[e] = song_title


for (words, song_title) in edges_to_add.items():
  word1, word2 = list(words)
  net.add_edge(word1, word2, title=song_title, width = 12)

  

net.show("output_graph.html")


print("done.")
