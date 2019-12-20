from classes import *

def gen_board(table):
    index = ((table.rows[0].cells[0].text).split(" "))[0]
    name = "".join(((table.rows[0].cells[0].text).split(" "))[1:])
    desc = table.rows[-1].cells[0].text
    return Board(index, name, desc)

def gen_chip(table):
    index = ((table.rows[0].cells[0].text).split(" "))[0]
    name = "".join(((table.rows[0].cells[0].text).split(" "))[1:])
    addr = table.rows[0].cells[-1].text
    offset = None
    external = None
    size = None
    for j in range (len(table.rows)):
            row = table.rows[j]
            if row.cells[0].text.lower() == 'offset':
                for i in range(len(row.cells)):
                    if row.cells[i].text.lower() == 'offset' and row.cells[i].text != row.cells[i + 1].text:
                        offset = row.cells[i + 1].text
                    if row.cells[i].text.lower() == 'external ' and row.cells[i].text != row.cells[i + 1].text:
                        external = row.cells[i + 1].text
                    if row.cells[i].text.lower() == 'size' and row.cells[i].text != row.cells[i + 1].text:
                        size = row.cells[i + 1].text
    return Chip(index, name, offset, external, size, addr)

def gen_block(table):
    index = ((table.rows[0].cells[0].text).split(" "))[0]
    name = "".join(((table.rows[0].cells[0].text).split(" "))[1:])
    addr = table.rows[0].cells[-1].text
    offset = None
    external = None
    size = None
    for j in range (len(table.rows)):
            row = table.rows[j]
            if row.cells[0].text.lower().strip() == 'offset':
                for i in range(len(row.cells)):
                    if row.cells[i].text.lower().strip() == 'offset' and row.cells[i].text != row.cells[i + 1].text:
                        offset = row.cells[i + 1].text
                    if row.cells[i].text.lower().strip() == 'external ' and row.cells[i].text != row.cells[i + 1].text:
                        external = row.cells[i + 1].text
                    if row.cells[i].text.lower().strip() == 'size' and row.cells[i].text != row.cells[i + 1].text:
                        size = row.cells[i + 1].text

    return Block(index, name, offset, external, size, addr)
    
def gen_reg_group(table):
    index = ((table.rows[0].cells[0].text.strip()).split(" "))[0]
    name = "".join(((table.rows[0].cells[0].text.strip()).split(" "))[1:])
    descr = table.rows[-1].cells[0].text
    offset = None
    external = None
    repeat = None
    size = None
    for j in range (len(table.rows)):
            row = table.rows[j]
            if row.cells[0].text.lower().strip() == 'offset':
                for i in range(len(row.cells)):
                    if row.cells[i].text.lower().strip() == 'offset' and row.cells[i].text != row.cells[i + 1].text:
                        offset = row.cells[i + 1].text
                    if row.cells[i].text.lower().strip() == 'external ' and row.cells[i].text != row.cells[i + 1].text:
                        external = row.cells[i + 1].text
                    if row.cells[i].text.lower().strip() == 'size' and row.cells[i].text != row.cells[i + 1].text:
                        size = row.cells[i + 1].text
                    if row.cells[i].text.lower().strip() == 'repeat' and row.cells[i].text != row.cells[i + 1].text:
                        repeat = row.cells[i + 1].text

    return Reg_group(index, name, offset, external, repeat, size, descr)


def gen_reg(table, size):
    index = ((table.rows[0].cells[0].text).split(" "))[0]
    name = "".join(((table.rows[0].cells[0].text).split(" "))[1:])
    addr = table.rows[0].cells[-1].text
    offset = None
    external = None
    default = None
    description = ""
    f_bits = []
    f_name = []
    f_sw = []
    f_hw = []
    f_default = []
    f_description = []
    for j in range (len(table.rows)):
            row = table.rows[j]
            if row.cells[0].text.lower() == 'offset':
                for i in range(len(row.cells)):
                    if row.cells[i].text.lower() == 'offset' and row.cells[i].text != row.cells[i + 1].text:
                        offset = row.cells[i + 1].text
                    if row.cells[i].text.lower().strip() == 'external' and row.cells[i].text != row.cells[i + 1].text:
                        external = row.cells[i + 1].text
                    if row.cells[i].text.lower() == 'default' and row.cells[i].text != row.cells[i + 1].text:
                        default = row.cells[i + 1].text
                    description = table.rows[j+3].cells[0].text
            elif row.cells[0].text.lower() == 'bits':
                for i in range(len(row.cells)):
                    if row.cells[i].text.lower() == 'bits' and row.cells[i].text != row.cells[i + 1].text:
                        for k in range (j+1, len(table.rows)):
                            f_bits.append(table.rows[k].cells[i].text)
                    if row.cells[i].text.lower() == 'name' and row.cells[i].text != row.cells[i + 1].text:
                        for k in range (j+1, len(table.rows)):
                            names = table.rows[k].cells[i].text
                            #names = "".join(names.split("_"))
                            f_name.append(split_lines(names.strip()))
                    if row.cells[i].text.lower() == 's/w' and row.cells[i].text != row.cells[i + 1].text:
                        for k in range (j+1, len(table.rows)):
                            f_sw.append(table.rows[k].cells[i].text)
                    if row.cells[i].text.lower() == 'h/w ' and row.cells[i].text != row.cells[i + 1].text:
                        for k in range (j+1, len(table.rows)):
                            f_hw.append(table.rows[k].cells[i].text)
                    if row.cells[i].text.lower() == 'default' and row.cells[i].text != row.cells[i + 1].text:
                        for k in range (j+1, len(table.rows)):
                            f_default.append(table.rows[k].cells[i].text)
                    if row.cells[i].text.lower() == 'description' and row.cells[i].text != row.cells[i - 1].text:
                        for k in range (j+1, len(table.rows)):
                            f_description.append(split_lines(table.rows[k].cells[i].text))
    return (Reg(index, name, description, offset, external, size, default, f_bits, f_name, f_sw, f_hw, f_default, f_description, addr))

