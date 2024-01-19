import marshal

import bytecode

with open('C:\\Users\\Utente\\Documents\\GitHub\\DPDPython\\src\\main\\python\\Oracle\\Adapter\\__pycache__\\AdapterPattern.cpython-310.pyc', 'rb') as f:
    contenuto = f.read(16)  # Salta l'intestazione del file .pyc ATTENZIONE dipende dalla versione di python (Attuale 3.10)
    code_obj = marshal.load(f)

by = bytecode.Bytecode.from_code(code_obj)

# Modifica il bytecode (ad esempio, sostituisci 'a' con '100')
for instruction in by:
    print(instruction)
    print(instruction.name)
    print(instruction.arg)
    print(instruction.lineno)