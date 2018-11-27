writeFile = open("dict.txt", 'w');

with open("dict1.txt") as file:
    for line in file:
        # Checa se todos os caracteres sao uppercase:
        if(line == line.upper()):
            continue;

        # Converte todos os caracteres para lowercase:
        newWord = line.lower();

        # Checa se a palavra possui um caractere invalido:
        invalid = ['k', 'w', 'y', '-'];
        isValid = True;
        for caractere in newWord:
            if caractere in invalid:
                isValid = False;
                break;

            if((caractere == 'á') or (caractere == 'ã') or
               (caractere == 'à') or (caractere == 'â')):
                arr = list(newWord);
                arr[arr.index(caractere)] = 'a';
                newWord = "".join(arr);
            elif((caractere == 'é') or (caractere == 'è') or
               (caractere == 'ê')):
                arr = list(newWord);
                arr[arr.index(caractere)] = 'e';
                newWord = "".join(arr);
            elif((caractere == 'í') or (caractere == 'ì') or
               (caractere == 'î')):
                arr = list(newWord);
                arr[arr.index(caractere)] = 'i';
                newWord = "".join(arr);
            elif((caractere == 'ó') or (caractere == 'õ') or
               (caractere == 'ò') or (caractere == 'ô')):
                arr = list(newWord);
                arr[arr.index(caractere)] = 'o';
                newWord = "".join(arr);
            elif((caractere == 'ú') or (caractere == 'ù') or
               (caractere == 'û') or (caractere == 'ü')):
                arr = list(newWord);
                arr[arr.index(caractere)] = 'u';
                newWord = "".join(arr);

        # Salva a palavra:
        if(isValid):
            writeFile.write(newWord);

writeFile.close();