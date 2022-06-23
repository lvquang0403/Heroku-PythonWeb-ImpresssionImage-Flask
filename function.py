from collections import Counter
from huffman_tree import *
import numpy as np
from PIL import Image
import re


#Hàm lấy tần suất xuất hiện của các kí tự trong chuỗi đầu vào
def getFreq(data):
    #img data
    if type(data) is not str:
        data_asstr = str(data.tolist())
        data = data_asstr

    str_based_res = dict()  
    for item in data:  
        if str_based_res.get(item) == None:  
            str_based_res[item] = 1  
        else:   
            str_based_res[item] += 1

    return str_based_res



#Hàm sắp xếp các symbols theo số lần xuất hiện để đưa vào cây
def sortSymbolList(nodes_list, node):
    node_value, char1 = node.value
    index = 0
    max_index = len(nodes_list)
    while True:
        if index == max_index:
            nodes_list.append(node)
            return
        current_val, char2 = nodes_list[index].value
        if current_val <= node_value:
            nodes_list.insert(index, node)
            return
        index += 1



#Hàm tính gán các code (mã nhị phân) cho các kí tự trong chuỗi đầu vào(nodes)
def CalculateCodes(root):
    if root is None:
        return {}
    characters = (root.value)[0]
    char_dict = dict([(i, '') for i in list(characters)])

    left_branch = CalculateCodes(root.get_left())

    for key, value in left_branch.items():
        char_dict[key] += '0' + left_branch[key]

    right_branch = CalculateCodes(root.get_right())

    for key, value in right_branch.items():
        char_dict[key] += '1' + right_branch[key]

    return char_dict


#Hàm tạo cây Huffman từ danh sách nodes (symbols, freq), thứ tự giảm dần
#
def build_tree(data):
    lst = getFreq(data)
    nodes_list = []
    for node_value in lst.items():
        node = Node(node_value)
        nodes_list.append(node)

    while len(nodes_list) != 1:
        first_node = nodes_list.pop()
        val1, char1 = first_node.value

        second_node = nodes_list.pop()
        val2, char2 = second_node.value
        node = Node((val1 + val2, char1 + char2))
        node.insert_left(second_node)
        node.insert_right(first_node)
        sortSymbolList(nodes_list, node)

    root = nodes_list[0]    
    tree = Tree()
    tree.root = root
    return tree


def huffman_encoding(data):
        
    #img data
    if type(data) is not str:
        data_asstr = str(data.tolist())
        data = data_asstr

    if data == '':
        return None, ''
        
    tree = build_tree(data)
    dict = CalculateCodes(tree.root)
    codes = ''
    for char in data:
        codes += dict[char]

    return tree, codes



# The function traverses over the encoded data and checks if a certain piece of binary code could actually be a letter
def str_decoding(data, tree):
    if data == '':
        return ''
    dict = CalculateCodes(tree.root)
    reversed_dict = {}
    for value, key in dict.items():
        reversed_dict[key] = value
    start_index = 0
    end_index = 1
    max_index = len(data)
    s = ''

    while start_index != max_index:
        if data[start_index : end_index] in reversed_dict:
            s += reversed_dict[data[start_index : end_index]]
            start_index = end_index
        end_index += 1

    return s


def img_decoding(data, tree, imgshape):
    bitstr = str_decoding(data, tree)
    temp = re.findall(r'\d+', bitstr)
    res = list(map(int, temp))
    res = np.array(res)
    res = res.astype(np.uint8)
    res = np.reshape(res, imgshape)

    return res

