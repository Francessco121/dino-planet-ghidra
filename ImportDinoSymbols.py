# Imports a file with lines in the form "symbolName = 0xADDRESS; // type:DATATYPE" where DATATYPE is either func or something else.
#
# type:func will mark the address as a function, any other type will mark the address with a label.
# Modified from ImportSymbolsScript.py.
# @author Francessco121 <https://github.com/Francessco121>
# @category Data
#

from ghidra.program.model.symbol import *
import string

functionManager = currentProgram.getFunctionManager()

f = askFile("Select file to import", "Go!")

for line in file(f.absolutePath):  # note, cannot use open(), since that is in GhidraScript
    pieces = line.split()

    if len(pieces) < 5 or pieces[1] != "=" or pieces[3] != "//":
        continue
    
    name = pieces[0]
    address = toAddr(long(pieces[2][:-1], 16)) # [:-1] strips ;
    typePieces = pieces[4].split(":")

    if len(typePieces) != 2:
        continue

    dataType = typePieces[1]
    
    if dataType == "func":
        func = functionManager.getFunctionAt(address)

        if func != None and func.getName() == name:
            pass
        else:
            if func is not None:
                old_name = func.getName()
                func.setName(name, USER_DEFINED)
                print("Renamed function {} to {} at address {}".format(old_name, name, address))
            else:
                func = createFunction(address, name)
                print("Created function {} at address {}".format(name, address))

    else:
        existingSymbol = getSymbolAt(address)
        if existingSymbol != None and existingSymbol.getName() == name:
            pass
        else:
            if existingSymbol != None:
                existingSymbol.delete()
                createLabel(address, name, True)
                print("Renamed label {} to {} at address {}".format(existingSymbol.getName(), name, address))
            else:
                createLabel(address, name, True)
                print("Created label {} at address {}".format(name, address))
