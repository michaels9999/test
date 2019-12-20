import docx
import sys
import re
import getopt
import os
from classes import *
from utility import *
from file_reader import *

inputfile  = []
outdir     = ""
outputfile = ""

##############################################
#command opts and args define
##############################################

opts, args = getopt.getopt(sys.argv[1:],"twhi:o:",["ws=","input=","output=", "option=","ignore="]) #Seprate the options and arguments

for opt, arg in opts:		#Identify the options
   if opt == '-h':        			#Help option
      print ("Example:")
      print ('python3.7 main.py --ws ${RUN_DIR} -i include/ai_test_pkg.svh -o out dir --ignore true --option op1,op2,op3')
      sys.exit()

   elif opt in ("-i", "--input"):		#input file option
      inputfile = arg
      print(inputfile)
   elif opt in ("-o", "--output"):		#output file option
      outdir = arg.strip()
      if outdir[:] != "/":
          outdir = outdir + "/"
      print(outdir)
   elif opt in ("-w", "--ws"):
      ws_dir = arg
   elif opt == "--option":
      option = arg
   elif opt == "--ignore":
      print(arg)
      if arg.lower() == "true":
          ignore_comment = True

#default output dir
if outdir == "":
    outdir = "./out"

if inputfile == []:
    sys.exit("Please enter the name of file correctly.")

input_file = inputfile + ".docx"
if not os.path.exists(outdir):
    os.mkdir(outdir)

doc = docx.Document(input_file)
tables = doc.tables

###########################################################
#Extract register information
###########################################################

i = len(tables) - 1
while i >= 0:
    #print (tables[i].rows[0].cells[0].text)
    if re.search("end regGroup",tables[i].rows[0].cells[0].text,re.I|re.M) != None:
        tables.pop(i)
    i = i - 1

level = [[],[],[],[],[]]

addr_list = []
for t in tables:
    #if t.rows[1].cells[0].text == "Table of Content":
    if re.search("Table of Content",t.rows[1].cells[0].text,re.I|re.M) != None:
        for i in t.rows:
            tmptext = i.cells[0].text.strip()
            index = tmptext
            depth = len(list(filter(None,tmptext)))
            addr = i.cells[3].text.strip()
            #print(index + "   -----  " + str(depth) + "   -----   " + addr)
            childs = []
            addr_list.append(addr_table(index, depth, addr, childs))
        break

output_parameter = outdir + "/" + input_file[:-5] + ".para.txt"
output_file = outdir + "/" + input_file[:-5] + ".regmem.sv"
output_file2 = outdir + "/" + input_file[:-5] + "_pkg.regmem.sv"
filep  = open(output_parameter, "w")
filew  = open(output_file, "w")
filew2 = open(output_file2, "w")
filew3 = open(outdir + "/" + input_file[:-5] + "_hw_if.sv","w")

type_list = []
has_enum = -1
for i in range(5):
    #print("pw_dbg_001 --- "+tables[i].rows[1].cells[0].text)
    if tables[i].rows[1].cells[0].text == "ENUM":
        type_list.append("tmp")
        has_enum = i
    elif tables[i].rows[1].cells[0].text == "DEFINE":
        type_list.append("tmp")
        for j in range(2, len(tables[i].rows)):
            filew.write("`define " + tables[i].rows[j].cells[0].text + " " + tables[i].rows[j].cells[1].text + "\n")
    elif tables[i].rows[1].cells[0].text == "Table of Content" or tables[i].rows[0].cells[0].text.strip() == "Revision" or tables[i].rows[1].cells[0].text.lower() == "tableofcontent":
        type_list.append("tmp")
for x in range(len(type_list)):
    print(type_list[x])

inline_shapes = doc.inline_shapes
for i in range(len(inline_shapes)):
    print(inline_shapes[i]._inline.docPr.attrib.get("descr"))
    type_list.append(inline_shapes[i]._inline.docPr.attrib.get("descr"))

for i in range (len(type_list)):
    print(type_list[i])
    if type_list[i] == "board":
        Board = gen_board(tables[i])
        level[len(Board.index)-1].append(Board)
    if type_list[i] == "chip":
        Chip = gen_chip(tables[i])
        level[len(Chip.index)-1].append(Chip)
    elif type_list[i] == "block":
        Blocks = gen_block(tables[i])
        level[len(Blocks.index)-1].append(Blocks)
    elif type_list[i] == "section":
        Group = gen_reg_group(tables[i])
        level[len(Group.index)-1].append(Group)
    elif type_list[i] == "reg32":
        Register = gen_reg(tables[i], 32)
        level[len(Register.index)-1].append(Register)
    elif type_list[i] == "reg16":
        Register = gen_reg(tables[i], 16)
        level[len(Register.index)-1].append(Register)
    elif type_list[i] == "reg8":
        Register = gen_reg(tables[i], 8)
        level[len(Register.index)-1].append(Register)

###########################################################
## Print chip, block, register, field parameters in *_para.txt file
###########################################################
print("\n Start print Chip parameters ... \n ")
print("\n Start print Block parameters ... \n ")
print("\n Start print Register parameters ... \n ")
print("\n Start print Field parameters ... \n ")

filep.close()
filew.close()
filew2.close()
filew3.close()
