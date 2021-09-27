import random

class EstadoTabuleiroGA:
    tabuleiro = []
    nRainhas = 0 
    valorFitness = 0 
    propLocal = 0
    percAptidao = 0

    def setPropLocal(self, propLocal):
        self.propLocal = propLocal

    def getPropLocal(self):
        return self.propLocal
    
    def setPercAptidao(self, percAptidao):
        self.percAptidao = percAptidao

    def getPercAptidao(self):
        return self.percAptidao

    def setValorFitness(self, valorFitness):
        self.valorFitness = valorFitness

    def getValorFitness(self):
        return self.valorFitness
    
    def setTabuleiro(self, tabuleiro):
        self.tabuleiro = tabuleiro

    def getTabuleiro(self):
        return self.tabuleiro

    def __init__(self, qtdeRainhas):
        self.nRainhas = qtdeRainhas

        self.tabuleiro = []
    
        for linha in range(self.nRainhas):
            linhas = []
            for coluna in range(self.nRainhas):
                if linha == coluna:
                    linhas.append(True)
                else:
                    linhas.append(False)
            self.tabuleiro.append(linhas)
        
        for linha in range(self.nRainhas):
            self.trocaPosicaoLinhas(linha, random.randint(0,  (self.nRainhas-1)))

        self.funcaoFitness()


    def funcaoFitness(self):
        fitnessParcial = 0 
        for linha in range(self.nRainhas):
            for coluna in range(self.nRainhas):
                if self.tabuleiro[linha][coluna]:
                    fitnessParcial += self.validarColisao(linha, coluna)
        self.valorFitness = (fitnessParcial / 2)

    def validarColisao(self, linhaRainhaOrigem, colunaRainhaOrigem):
        qtdeConflitos = 0

        for linhaRainhaAtual in range(self.nRainhas):
            for colunaRainhaAtual in range(self.nRainhas):
                temRainha = self.tabuleiro[linhaRainhaAtual][colunaRainhaAtual]
                
                naoEhRainhaOrigem = (linhaRainhaAtual  != linhaRainhaOrigem and colunaRainhaAtual != colunaRainhaOrigem)
                estaNaLinhaColunaRainhaOrigem = (linhaRainhaAtual  == linhaRainhaOrigem or colunaRainhaAtual == colunaRainhaOrigem)
                estaNaDiagonalRainhaOrigem = (linhaRainhaAtual + colunaRainhaAtual == linhaRainhaOrigem + colunaRainhaOrigem or linhaRainhaAtual - colunaRainhaAtual == linhaRainhaOrigem - colunaRainhaOrigem)
                
                if temRainha and ((naoEhRainhaOrigem and estaNaDiagonalRainhaOrigem) or (estaNaLinhaColunaRainhaOrigem and not naoEhRainhaOrigem and not estaNaDiagonalRainhaOrigem)):
                    qtdeConflitos += 1
        
        return qtdeConflitos	
        
        		            				         
    def trocaPosicaoLinhas(self, n1, n2):
            linha = self.tabuleiro[n1]
            self.tabuleiro[n1] = self.tabuleiro[n2]
            self.tabuleiro[n2] = linha
   
    def imprimirTabuleiro(self):
        print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")
        print("Impressao do resultado:")
        for linha in range(self.nRainhas):
            for coluna in range(self.nRainhas):
                print("[R]" if self.tabuleiro[linha][coluna] == True else "[ ]", end="")
            print("")

        print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")

        print("Solucao otima encontrada!" if self.valorFitness == 0 else "Solucao otima nao encontrada!")


