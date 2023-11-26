import matplotlib.pyplot as plt
from heapq import heappush, heappop
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import random as rn


def proc_huffman(f):
    h = []
    out = []
    visited_fs = set()  # уникальные fs
    for i in f:
        heappush(h, (f[i], i))
    while len(h) > 1:
        f1, i = heappop(h)
        f2, j = heappop(h)
        fs = f1 + f2
        order_val = ord('a')
        fl = str(fs)
        while fl in visited_fs:  # уникальность fs
            letter = chr(order_val)
            fl = str(fs) + letter
            order_val += 1
        visited_fs.add(fl)
        out.append((fl, i, j))
        heappush(h, (fs, fl))
    out.reverse()
    return out


def rename_nodes_to_binary_and_encoding(tree):
    codes = {}
    text = [i for j in tree for i in j]
    text[0] = ''
    temp = set()
    for i in range(1, len(text)):
        if i in temp:  # Если буква уже во временном массиве
            continue
        if text[i].isalpha() or not text[i].isalnum():  # Eсли буква или пунктуация
            tempor = text[i]
            tempor2 = f'{text[i - i % 3]}{i % 3 -1}'
            text[i] += f"({tempor2})"
            codes[tempor] = tempor2
            continue
        if (text[i] != '0') and (text[i] != '1'):  # Eсли символ не равен нулю и единице
            for j in range(i+1, len(text)):
                if text[j] == text[i]:
                    temp.add(j)
                    text[j] = text[i - i % 3] + f'{i % 3 - 1}'
                    break
            text[i] = text[i - i % 3] + f'{i % 3 - 1}'
    text[0] = 'root'
    result = [(text[i], text[i+1], text[i+2]) for i in range(0, len(text), 3)]
    return result, codes


def encode(text, code_map):
    return ''.join(code_map[ch] for ch in text)


def decode(text, code_map):
    path = ''
    string = ''
    temp = ''
    node = [i[0] for i in text]
    for bit in code_map:
        path += bit
        if path in node:
            temp = node.index(path)
            continue
        else:
            string += text[temp][int(bit)+1][0]
            path = ''
    return string


if __name__ == "__main__":
    string = "Test string with a lot of ts"
    sentence = string
    character_count = {}

    for char in sentence:
        # Если символ уже есть в словаре, увеличиваем его счетчик на 1
        if char in character_count:
            character_count[char] += 1
        # Если символа еще нет в словаре, добавляем его и устанавливаем счетчик в 1
        else:
            character_count[char] = 1

    # Выводим результаты
    for char, count in character_count.items():
        print(f"'{char}': {count}")

    huffman_tree = proc_huffman(character_count)
    G = nx.DiGraph()
    huffman_tree, codes = rename_nodes_to_binary_and_encoding(huffman_tree)

    # Добавление ребер в граф
    for parent, left_child, right_child in huffman_tree:
        G.add_edge(parent, left_child)
        G.add_edge(parent, right_child)

    encoded = encode(string, codes)

    print(f"Коды: {codes}")
    print(f"Закодировано: {encoded}")
    print(f"Декодированно: {decode(huffman_tree, encoded)}")

    # Позиционирование узлов с помощью Graphviz
    pos = graphviz_layout(G, prog='dot', root=1)

    # Отрисовка графа с установками
    plt.figure(figsize=(8, 8))
    nx.draw_networkx(G, pos, with_labels=True, node_size=90,
                     node_color="lightblue", font_size=8, font_color="black")
    plt.tight_layout()
    plt.show()
