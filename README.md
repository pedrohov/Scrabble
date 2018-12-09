# Scrabble

Jogo de palavras cruzadas *Scrabble* que implementa rotinas para a geração de palavras dado o estado do tabuleiro.

O computador utiliza a estrutura *DAWG* para realizar buscas rápidas no dicionário, e forma palavras utilizando o método de backtracking proposto em [The World's Fastest Scrabble Program](https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf).

O jogo possui dois *DAWGs*, um minimizado e um sem minimizar, criados para analisar a eficiência do procedimento de formação de palavras com cada estrutura.

## Execução
Para executar o jogo com o DAWG minimizado, é preciso apenas executar o script *game.py* pelo terminal:
``` 
python3 game.py
``` 
Para utilizar o DAWG sem minimização, é preciso primeiro executar o script *dawg.py*:
```
python3 dawg.py
```
E alterar o import da linha 10 em game.py, para 
```
from dawg import *;
```
Após a alteração o jogo pode ser executado com a estrutura sem minimização:
```
python3 game.py
```