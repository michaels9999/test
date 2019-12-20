from utility import *

class addr_table:
    def __init__(self, index, depth, addr, childs):
        self.index = index.strip()
        self.depth = depth
        self.address = addr
        self.childs = childs
    def add_child(self, child):
        self.childs.append(child)
    def child_depth(self):
        return self.depth +1
    def parent_index(self):
        if len(self.index) > 1:
            return self.index[:-2]
        return "0"
    

class Board:
    def __init__(self, index, name, descr):
        self.index = index.split(".")
        self.name = split_lines(name.strip())
        self.description = descr
        self.type = "board"
        

class Chip:
    def __init__(self, index, name, offset, external, size, address):
        self.index = index.split(".")
        self.name = split_lines(name.strip())
        self.offset = offset
        self.external = external
        self.size = size
        self.type = "chip"
        self.address = address
        
    def parent_index(self):
        return self.index[:-1]

        


class Block:
    def __init__(self, index, name, offset, external, size, address):
        self.index = index.split(".")
        self.name = split_lines(name.strip())
        self.offset = offset
        self.external = external
        self.size = size
        self.type = "block"
        self.address = address

    def parent_index(self):
        return self.index[:-1]

class Reg_group:
    def __init__(self, index, name, offset, external, repeat, size, desc):
        self.index = index.split(".")
        self.name = split_lines(name.strip())
        self.offset = offset
        self.external = external
        self.repeat = repeat
        self.size = size
        self.type = "group"
        self.description = desc
        

    def parent_index(self):
        return self.index[:-1]

class Reg:
    def __init__(self, index, name, description, offset, external, size, default, field_bits, field_name, field_sw, field_hw, field_default, field_description, address):
        self.index = index.split(".")
        self.name = "".join(split_lines(name.strip()).split("-"))
        self.description = split_lines(description)
        self.offset = offset
        self.external = external
        self.size = size
        self.default = default
        self.field_bits = field_bits
        self.field_name = field_name
        self.field_sw = field_sw
        self.field_hw = field_hw
        self.field_default = field_default
        self.field_description = field_description
        self.type = "register"
        self.address = address

    def parent_index(self):
        return self.index[:-1]

    def get_rwpair(self):
        tmp = (((self.description).strip("{}")).split("=")[1])
        return Reg("".join(self.index), tmp.split(",")[0], "", self.offset, self.external, self.size, self.default, self.field_bits, self.field_name, [tmp.split(",")[1]], self.field_hw, self.field_default, self.field_description, self.address)
