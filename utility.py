from classes import *
import re

def rindex(s, e):
    return len(s) - s[::-1].index(e) - 1

def find_des(s):
    if "{" in s:
        start = s.index("{")
        end  = rindex(s, "}")
        return s[:start] + s[end+1:]
    return s.strip(" ")

def find_arg(s):
    try:
        start = s.index("/$") + len("/$")
        end = s.index( "$/", start )
        return [s[start:end]] + find_arg(s[end:])
    except ValueError:
        return []

def find_cond(s):
    try:
        start = s.index("/%") + len("/%")
        end = s.index( "%/", start )
        return s[start:end]
    except ValueError:
        return ""
    
def get_address(addr_list, index):
    for i in addr_list:
        if i.index == (".".join(index)).strip():
            return i.address

def get_parent_reg(reg, level):
    index = reg.parent_index()
    for i in level:
        for j in i:
            if index == j.index:
                return j

def get_block_reg(reg, level):
    for i in level:
        for j in i:
            if j.type == "block":
                l = len(j.index)
                if j.index == reg.index[:l]:
                    return j

def get_child(parent, level, t):
    child = []
    for elements in level:
        for element in elements:
            if element not in child and element.type == t and element.parent_index() == parent.index:
                child.append(element)
    return child

def get_more_child(parent, level, t):
    child = []
    for elements in level:
        for element in elements:
            if element not in child and element.type == t and (element.parent_index() == parent.index or element.parent_index()[:-1] == parent.index):
                child.append(element)
    return child

def hex_add(hex_number, n):
    tmp = int(hex_number, 16)
    tmp = tmp + n
    return (hex(tmp)[2:]).upper()

def get_addr(parent, level):
    if parent.type == "group":
        childs = get_child(parent, level, "register")
        return childs[0].addr
    if parent.type == "block":
        childs = get_child(parent, level, "register")
        return childs[0].addr  
    if parent.type == "chip":
        childs = get_child(parent, level, "block")
        return get_addr(childs[0], level)

def split_lines(s):
    return "".join(s.split("\n"))

def find_intr_pair(reg, level):
    tmp = re.split("}{|}|{|; |=", reg.description.strip())

    signal = ""

    for i in range(len(tmp)):
        if tmp[i] == "intr.status":
            
            signal = (tmp[i+1]).strip()
    for l in level:
        for i in l:
            if i.type == "register":
                tmp1 = re.split("}{|}|{|; |=", i.description.strip())
                for index in range(len(tmp1)):
                    if tmp1[index] == "intr.enable":
                        signalr = (tmp1[index+1]).strip()

                        if signalr == signal:
                            return i

def find_intr_pair_f (reg, level):
    for ele in reg.field_description:
        tmp = re.split("}{|}|{|; |=", ele.strip())
        signal = ""

        for i in range(len(tmp)):
            if tmp[i] == "intr.status":
            
                signal = tmp[i+1]
        for l in level:
            for i in l:
                if i.type == "register":
                    for f in i.field_description:
                        tmp1 = re.split("}{|}|{|; |=", f.strip())
                        for index in range(len(tmp1)):
                            if tmp1[index] == "intr.enable":
                                signalr = tmp1[index+1]
                                if signalr == signal:
                                    return i

