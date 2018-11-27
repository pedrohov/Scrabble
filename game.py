# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

from player import *;
from piece  import *;
from move   import *;
from dawg   import *;
from board  import *;
from playerIA import *;

class Game():

    def __init__(self, boardFile, dawgFile):
        self.dict  = load(dawgFile).root;
        self.board = Board(boardFile, self.dict);

        self.pieces = {'#': 3, 'a': 14, 'e': 11, 'i': 10, 'o': 10,
                       's': 8, 'u': 7 , 'm': 6 , 'r': 6 , 't': 5 ,
                       'd': 5, 'l': 5 , 'c': 4 , 'p': 4 , 'n': 4 ,
                       'b': 3, 'ç': 2 , 'f': 2 , 'g': 2 , 'h': 2 ,
                       'v': 2, 'j': 2 , 'q': 1 , 'x': 1 , 'z': 1 };

        self.player1 = None;
        self.player2 = None;        

    def start(self):

        # Definir jogador Humano/Computador:
        opcao = 0;
        while(opcao < 1) or (opcao > 3):
            opcao = int(input("\nSCRABBLE\n1 - Jogador vs Jogador.\n2 - Jogador vs Com\n3 - Com vs Com\n\nOpcao: "));
        print("");
        self.setupPlayers(opcao);

        # Mostra o jogo:
        self.showBoard();

        # Faz a primeira jogada:
        self.turn.firstPlay();

        # Troca o turno atual:
        self.changeTurn();

        # Loop de jogadas:
        self.run();

    def run(self):
        """ Loop de jogo """
        while(True):
            self.showBoard();
            self.turn.play();
            self.changeTurn();

    def startingHand(self):
        """ Sorteia uma mao inicial e a retorna como dicionario de Pieces."""
        res = {};
        i = 0;
        while(i < 7):
            # Sorteia uma peca aleatoria:
            (piece, value) = random.choice(list(self.pieces.items()));
            if(value > 0):
                # Remove a peca do saquinho:
                self.pieces[piece] -= 1;
                i += 1;

                # Adiciona a peca a mao:
                if piece in res:
                    res[piece].quantity += 1;
                else:
                    res[piece] = Piece(piece);

        return res;

    def showBoard(self):
        print(self.board);
        self.turn.showHand();

    def changeTurn(self):
        """ Troca o turno do jogador atual.
            Reseta as informacoes utilizadas para criar a jogada.
        """
        if(self.turn == self.player1):
            self.turn = self.player2;
            self.player1.reset();
        else:
            self.turn = self.player1;
            self.player2.reset();

    def setupPlayers(self, opcao):
        if(opcao == 1):
            self.player1 = Player("JOGADOR 1", self.board, self.dict);
            self.player2 = Player("JOGADOR 2", self.board, self.dict);
        elif(opcao == 2):
            self.player1 = Player("JOGADOR", self.board, self.dict);
            self.player2 = PlayerIA("COMPUTADOR", self.board, self.dict);
        else:
            self.player1 = PlayerIA("COM1", self.board, self.dict);
            self.player2 = PlayerIA("COM2", self.board, self.dict);

        self.player1.hand = self.startingHand();
        self.player2.hand = self.startingHand();

        # Sorteia um jogador para comecar:
        if(random.choice([True, False])):
            self.turn = self.player1;
        else:
            self.turn = self.player2;


if __name__ == "__main__":
    jogo = Game("board.txt", "dict.dawg");
    jogo.start();