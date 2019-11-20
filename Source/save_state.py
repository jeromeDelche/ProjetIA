taille_char = 64
file_name = "../histo_state.csv"
def Write (open_type, string) :
    with open(file_name, 'open_type') as file:
        file.write(f'{string};')


def Read():
    with open(file_name, 'r') as file:
        contend = file.read()
        return contend

def Search(state_seek, contend):
    for char in contend.split(';'):
        #sépare la value qui se trouve en 1ere position
        value = char[0]
        state = char[1:taille_char]
        if (state_seek in state):
            return [value,state]
        else:
            return 0

def Maj(state, new_value, contend):
    result = Search(state, contend)
    if result == 0:
        Write('a', f"{new_value}{state};")
    else:
        new_contend = ""
        for char in contend.split(';'):
            if state in char:
                char = f"{new_value}{state}"
            new_contend += char +';'

        Write('w', new_contend)

def GetValue(state):
    contend = Read()
    return Search(state, contend)[0]