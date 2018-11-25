'''
    Documentation:
    Date:24/11/2018 
'''

from graphviz import Digraph

path_root = '/home/rodriguesfas/Mestrado/workspace/data_science/view_data/graphviz/'

dot = Digraph(comment='The Round Table')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)

dot.render(path_root + 'round-table.graphviz', view=True)  