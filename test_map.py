import osmnx as ox
import sqlite3
import networkx as nx
import matplotlib.pyplot as plt


def Min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


def Delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


def PrintMatrix(matrix):
    print("---------------")
    for i in range(len(matrix)):
        print(matrix[i])
    print("---------------")


#place = ["Moscow, Russia"]
#G = ox.graph_from_place(place, retain_all=True, simplify=True, network_type='walk')

connection = sqlite3.connect('my_map_database.db')
cursor = connection.cursor()

cursor.execute('SELECT * FROM Moscow_graph')
gr = cursor.fetchall()

connection.close()

graph = nx.Graph()


for i in gr:
    temp_str = i[4][1:-1]
    if "length" in temp_str:
        temp_index = temp_str.index("length")
        cur_length = temp_str[temp_index:].split(",")[0][9:]
    else:
        cur_length = 0
    graph.add_edge(i[1], i[2], weight=float(cur_length))

my_path_list = [5272070033, 8255123343, 90058438, 5271927963]
n = len(my_path_list)
my_graph = nx.Graph()

matrix = []
path_matrix = []
H = 0
PathLenght = 0
Str = []
Stb = []
res = []
result = []
result_str = ""
StartMatrix = []

for i in range(n):
    Str.append(i)
    Stb.append(i)
    matrix.append([float('inf') for x in range(n)])
    path_matrix.append(['' for x in range(n)])

for i in range(len(my_path_list) - 1):
    for j in range(len(my_path_list)-1, i, -1):
        cur_shortest_path = nx.shortest_path(graph, source=my_path_list[i], target=my_path_list[j], weight='weight')
        cur_shortest_length = nx.path_weight(graph, cur_shortest_path, weight='weight')
        my_graph.add_edge(my_path_list[i], my_path_list[j], weight=float(cur_shortest_length))
        matrix[i][j] = cur_shortest_length
        matrix[j][i] = cur_shortest_length
        path_matrix[i][j] = cur_shortest_path
        path_matrix[j][i] = list(reversed(cur_shortest_path))

for i in range(n):
    StartMatrix.append(matrix[i].copy())

while True:
    for i in range(len(matrix)):
        temp = min(matrix[i])
        H += temp
        for j in range(len(matrix)):
            matrix[i][j] -= temp

    for i in range(len(matrix)):
        temp = min(row[i] for row in matrix)
        H += temp
        for j in range(len(matrix)):
            matrix[j][i] -= temp

    NullMax = 0
    index1 = 0
    index2 = 0
    tmp = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 0:
                tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
                if tmp >= NullMax:
                    NullMax = tmp
                    index1 = i
                    index2 = j

    res.append(Str[index1] + 1)
    res.append(Stb[index2] + 1)

    oldIndex1 = Str[index1]
    oldIndex2 = Stb[index2]
    if oldIndex2 in Str and oldIndex1 in Stb:
        NewIndex1 = Str.index(oldIndex2)
        NewIndex2 = Stb.index(oldIndex1)
        matrix[NewIndex1][NewIndex2] = float('inf')
    del Str[index1]
    del Stb[index2]
    matrix = Delete(matrix, index1, index2)
    if len(matrix) == 1: break

for i in range(0, len(res) - 1, 2):
    if res.count(res[i]) < 2:
        result.append(res[i])
        result.append(res[i + 1])

for i in range(0, len(res) - 1, 2):
    for j in range(0, len(res) - 1, 2):
        if result[len(result) - 1] == res[j]:
            result.append(res[j])
            result.append(res[j + 1])

for i in range(0, len(result) - 1, 2):
    if i == len(result) - 2:
        PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]
        PathLenght += StartMatrix[result[i + 1] - 1][result[0] - 1]
    else:
        PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]

nx.draw(my_graph, with_labels=True)
plt.show()

print("----------------------------------")
result.append(result[-1])
result.append(result[0])

for i in range(0, len(result) - 1, 2):
    temp_index = int(result[i])
    result_str += f' -> {my_path_list[temp_index-1]}'
result_str += f' -> {my_path_list[int(result[0])-1]}'
result_str = result_str[4:]
print(result_str)

print(PathLenght)
print("----------------------------------")

for i in range(0, len(result) - 1, 2):
    start_index = int(result[i])
    end_index = int(result[i+1])
    print(path_matrix[start_index-1][end_index-1])
