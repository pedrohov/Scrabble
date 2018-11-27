# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

from player import *;

class PlayerIA(Player):

    def __init__(self, name, board, dictionary):
        super().__init__(name,  board, dictionary);
        self.anchors  = [];
        self.anchor   = None;
        self.bestMove = None;
        self.playDir  = None;
        self.placedNew = False;
        self.placedRight = 0;
        self.pos = (0, 0);

        # Lista de tuplas que informa se foram utilizadas pedras
        # em branco para formar a jogada e a posicao da pedra.
        # Utilizado para calcular o valor da jogada pelo tabuleiro.
        self.brancos = [];

    def play(self):
        """ Determina e realiza a melhor jogada 
            encontrada, tomando 'self.anchors' como
            pontos ancora.
        """

        # Determina todos os pontos ancora:
        self.getAnchors();

        for anchor in self.anchors:
            # Define ancora atual:
            self.anchor = (anchor[1].value, anchor[1]);
            self.pos = self.anchor[1].pos;

            # Direcao da jogada:
            self.playDir = anchor[0];

            # Forma palavras:
            self.leftPart("", self.dict, 10, anchor[1]);

        # Faz a melhor jogada encontrada:
        if(self.bestMove is None):
            print("Nao tenho jogada nenhum smaliefaec.");
            exit();
        else:
            self.board.insertWord(self.bestMove, self);
            self.addWord(self.bestMove);
            print(self.bestMove);


    def leftPart(self, word, root, limit, square):
        """ Cria prefixos a esquerda do ponto ancora.
            Sempre que um novo prefixo for formado,
            tenta encontrar as palavras correspondentes.
        """

        # Se houver espaco a esquerda:
        if(limit > 0):
            # Para cada letra possivel:
            for l in root.edges:

                # Se a letra for a ancora, estende para a direita:
                if(l == self.anchor[0]):
                    self.extendRight(word, root, square);

                # Demais pedras:
                elif(l in self.hand) and (self.hand[l].quantity > 0):
                    self.hand[l].quantity -= 1;
                    self.placedNew = True;
                    newRoot = root.edges[l];
                    self.leftPart(word + l, newRoot, limit - 1, square);
                    self.hand[l].quantity += 1;
                    self.placedNew = False;

                # Trata pedras em branco na mao:
                elif('#' in self.hand) and (self.hand['#'].quantity > 0):
                    self.hand['#'].quantity -= 1;
                    self.placedNew = True;
                    newRoot = root.edges[l];
                    
                    # Adiciona a peca em branco a lista:
                    self.brancos.append((l, len(word)));

                    self.leftPart(word + l, newRoot, limit - 1, square);

                    # Remove a pedra em branco da lista:
                    self.brancos.pop();
                    self.hand['#'].quantity += 1;
                    self.placedNew = False;

        return;

    def extendRight(self, word, root, square):
        """ Forma sufixos para um dado prefixo 'word'. 
            Poda palavra formada cria-se uma nova jogada,
            mantendo a que garantir mais pontos.
        """
        if(square.isEmpty()):
            if(root.final == True):
                # Cria uma nova jogada:
                self.generateMove(word, square);

            for l in root.edges:

                # Se a letra 'l' esta na mao do jogador:
                if(l in self.hand) and (self.hand[l].quantity > 0):
                    # Define a proxima posicao no tabuleiro:
                    nextSquare = None;
                    if((self.playDir == "V") and (square.pos[0] + 1 < 15)):
                        nextSquare = self.board.matrix[square.pos[0] + 1][square.pos[1]];
                    elif((self.playDir == "H") and (square.pos[1] + 1 < 15)):
                        nextSquare = self.board.matrix[square.pos[0]][square.pos[1] + 1];
                    if(nextSquare is None):
                        return;

                    # Remove a peca 'l' da mao do jogador:
                    self.hand[l].quantity -= 1;
                    self.placedNew = True;

                    # Atualiza a posicao no dawg:
                    newRoot = root.edges[l];

                    # Informa que foi colocada uma peca a direita:
                    self.placedRight += 1;

                    # Continua a formar palavras a direita:
                    self.extendRight(word + l, newRoot, nextSquare);
                    self.hand[l].quantity += 1;
                    self.placedNew = False;
                    self.placedRight -= 1;

                # Trata pedras em branco na mao:
                elif('#' in self.hand) and (self.hand['#'].quantity > 0):
                    # Define a proxima posicao no tabuleiro:
                    nextSquare = None;
                    if((self.playDir == "V") and (square.pos[0] + 1 < 15)):
                        nextSquare = self.board.matrix[square.pos[0] + 1][square.pos[1]];
                    elif((self.playDir == "H") and (square.pos[1] + 1 < 15)):
                        nextSquare = self.board.matrix[square.pos[0]][square.pos[1] + 1];
                    if(nextSquare is None):
                        return;

                    # Remove a peca 'l' da mao do jogador:
                    self.hand['#'].quantity -= 1;
                    self.placedNew = True;

                    # Adiciona a peca em branco a lista:
                    self.brancos.append((l, len(word)));

                    # Atualiza a posicao no dawg:
                    newRoot = root.edges[l];

                    # Informa que foi colocada uma peca a direita:
                    self.placedRight += 1;

                    # Continua a formar palavras a direita:
                    self.extendRight(word + l, newRoot, nextSquare);

                    # Remove a pedra em branco da lista:
                    self.brancos.pop();
                    self.hand['#'].quantity += 1;
                    self.placedNew = False;
                    self.placedRight -= 1;
        else:
            l = square.value;
            if(l in root.edges):
                if((self.playDir == "V") and (square.pos[0] + 1 < 15)):
                    nextSquare = self.board.matrix[square.pos[0] + 1][square.pos[1]];
                    newRoot = root.edges[l];
                    self.placedRight += 1;
                    self.extendRight(word + l, newRoot, nextSquare);
                    self.placedRight -= 1;
                elif((self.playDir == "H") and (square.pos[1] + 1 < 15)):
                    nextSquare = self.board.matrix[square.pos[0]][square.pos[1] + 1];
                    newRoot = root.edges[l];
                    self.placedRight += 1;
                    self.extendRight(word + l, newRoot, nextSquare);
                    self.placedRight -= 1;
        return;

    def firstPlay(self):
        """ Faz a primeira jogada. """

        hand = self.hand;
        limit = 7;
        square = self.board.matrix[7][7];
        self.playDir = "V";
        
        # Cria palavras com as pecas da mao do jogador
        # usando cada letra como ancora uma vez:
        size = len(hand);
        for i in range(size):
            # Peg a peca 'i':
            (letter, piece) = list(hand.items())[i];
            hand[letter].quantity -= 1;

            # Define como ancora:
            self.anchor = (letter, square);

            # Forma palavras:
            self.leftPart("", self.dict, limit, square);

            # Devolve a peca:
            hand[letter].quantity += 1;

        # Faz a melhor jogada encontrada:
        if(self.bestMove is None):
            print("Nao tenho jogada nenhuma smaliefaec.");
            exit();
        else:
            self.board.insertWord(self.bestMove, self);
            self.addWord(self.bestMove);
            print(self.bestMove);

    def generateMove(self, word, square):
        """ Cria uma jogada.
            Mantem a que fizer mais pontos em 'self.bestMove'.
        """

        # Se nao foi colocada nenhuma nova peca
        # a jogada gerada eh invalida:
        if(self.placedNew == False):
            return;

        if(self.playDir == "H"):
            iniY = square.pos[1] - len(word);
            newMove = Move(word, (square.pos[0], iniY), "H");
        elif(self.playDir == "V"):
            anchor = self.anchor[1];
            iniX = square.pos[0] - len(word);
            newMove = Move(word, (iniX, square.pos[1]), "V");
        newMove.value = self.board.calcMovePoints(newMove);
        newMove.parseBrancos(self.brancos);

        # A jogada criada nao eh valida
        if(self.board.isValid(newMove, self) is False):
            return;

        # Mantem a melhor jogada salva em 'self.bestMove':
        if((self.bestMove is None) or (newMove.value > self.bestMove.value)):
            self.bestMove = newMove;

    def getAnchors(self):
        """ Atualiza a lista 'self.anchors' com
            todas as posicoes preenchidas no tabuleiro
            que possuirem uma posicao vazia adjacente. 
        """
        for lin in range(len(self.board.matrix)):
            for col in range(len(self.board.matrix[lin])):
                
                # Se a linha for valida:
                if((lin >= 1) and (lin < 15)):
                    # Se a posicao acima estiver vazia, marca esta como ancora:
                    if((self.board.matrix[lin - 1][col].isEmpty()) and (self.board.matrix[lin][col].isEmpty() == False)):
                        self.anchors.append(("V", self.board.matrix[lin][col]));

                # Se a coluna for valida:
                if((col >= 1) and (col < 15)):
                    # Se a posicao a esquerda estiver vazia, marca esta como ancora:
                    if((self.board.matrix[lin][col - 1].isEmpty()) and (self.board.matrix[lin][col].isEmpty() == False)):
                        self.anchors.append(("H", self.board.matrix[lin][col]));

    def isValid(self):
        return True;

    def reset(self):
        self.anchors  = [];
        self.anchor   = None;
        self.bestMove = None;
        self.playDir  = None;
        self.placedNew   = False;
        self.placedRight = 0;
        self.brancos  = [];