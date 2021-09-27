import random
from EstadoTabuleiroGA import EstadoTabuleiroGA
import time
import sys


tempoInicial = 0    
qtdeRainhas = 0 
qtdeGeracoes = 0
qtdePopInicial = 0
qtdeMaxSelecao = 0
valoresValidosQtdeCruzamento = []
MAX_INT = sys.maxsize

def tempoAtualMili():
    return round(time.time() * 1000)

def populaValoresValidosQtdeCruzamento(valoresValidosQtdeCruzamento, qtdePopInicial):
    valorAdimissivel = int((qtdePopInicial/2))
    for valorAdimissivel in range(valorAdimissivel,qtdePopInicial):
        if valorAdimissivel % 2 == 0 and ((valorAdimissivel + 2) <= qtdePopInicial):
            valoresValidosQtdeCruzamento.append(valorAdimissivel)

#método utilizado para geração de população inicial
def geraPopInicial(qtdeRainhas):
    listEstados = []

    for i in range(qtdePopInicial):
        novoEstado = EstadoTabuleiroGA(qtdeRainhas)    
        listEstados.append(novoEstado)

    return listEstados

def melhorIndividuoAteAgora(popInicial, melhorFitnessAtual):
    popInicial = sorted(popInicial, key= EstadoTabuleiroGA.getValorFitness)
    
    fitnessAtual = MAX_INT

    indice = -1
    
    for i in range(len(popInicial)):
        fitnessRegAtual = popInicial[i].getValorFitness()
        
        if fitnessRegAtual < melhorFitnessAtual and fitnessRegAtual < fitnessAtual:
            fitnessAtual = popInicial[i].getValorFitness()
            indice = i
        
        if fitnessAtual == 0:
            break
        
    if indice != -1:
        return copiaRegistro(popInicial[indice])
    else: 
        return None

def copiaRegistro(origem):
    novoReg = EstadoTabuleiroGA(qtdeRainhas)

    novoReg.setPercAptidao(origem.getPercAptidao())
    novoReg.setPropLocal(origem.getPropLocal())
    novoReg.setValorFitness(origem.getValorFitness())
    novoReg.setTabuleiro(origem.getTabuleiro())
		
    return novoReg
    
def selecionaIndividuos(popInicial):
    indivSelecionados = []
    probTotal = 0

    for indice in range(len(popInicial)):
        aptidao = popInicial[indice].getValorFitness()
        propLocal = ((aptidao - 100) * - 1)
        popInicial[indice].setPropLocal(propLocal)
        probTotal += propLocal

    for indice in range(len(popInicial)):
        probLocal = popInicial[indice].getPropLocal()
        popInicial[indice].setPercAptidao(probLocal / probTotal)

    for qtde in range (qtdeMaxSelecao):
        percRandom = random.random()
        percAcumulada = 0

        for indice in range(len(popInicial)):
            percAcumulada += popInicial[indice].getPercAptidao()

            if percAcumulada > percRandom and not popInicial[indice] in indivSelecionados:
                estadoTabuleiroGA = EstadoTabuleiroGA(qtdeRainhas)
                estadoTabuleiroGA = copiaRegistro(popInicial[indice])
                indivSelecionados.append(estadoTabuleiroGA)
                break
                
    return indivSelecionados

def cruzamentoDeIndividuos(popSelecionada):
    filhosCruzados = []

    for pai1 in range(len(popSelecionada)-1):
        pai2 = (pai1 + 1)
        posicaoDeCorte = random.randint(0,  qtdeRainhas-1)

        filhoCruzado1 = EstadoTabuleiroGA(qtdeRainhas)
        filhoCruzado2 = EstadoTabuleiroGA(qtdeRainhas)

        genesPai1 = popSelecionada[pai1].getTabuleiro()
        genesPai2 = popSelecionada[pai2].getTabuleiro()

        for posicao in range(posicaoDeCorte):
            linha = genesPai1[posicao]
            genesPai1[posicao] = genesPai2[posicao]
            genesPai2[posicao] = linha
        
        filhoCruzado1.setTabuleiro(genesPai1)
        filhoCruzado2.setTabuleiro(genesPai2)
        filhosCruzados.append(filhoCruzado1)
        filhosCruzados.append(filhoCruzado2)
        
        pai1 += 1
    
    return filhosCruzados
    
def atualizaPopInicial(popInicial, filhosGerados):
    novaPopInicial = []

    popInicial = sorted(popInicial, key= EstadoTabuleiroGA.getValorFitness)
    filhosGerados = sorted(filhosGerados, key= EstadoTabuleiroGA.getValorFitness)

    paiRandomIndice = random.randint(0,  qtdePopInicial-1)
    paiRandom = copiaRegistro(popInicial[paiRandomIndice])
    novaPopInicial.append(paiRandom)

    qtdeAInserir = len(popInicial)

    for indice in range(int((qtdeAInserir/2)-1)):
        novaPopInicial.append(popInicial[indice])

    for indice in range(int((qtdeAInserir/2))):
        novaPopInicial.append(filhosGerados[indice])
    
    popInicial = []

    for indice in range(len(novaPopInicial)):
        estado = copiaRegistro(novaPopInicial[indice])
        estado.funcaoFitness()
        popInicial.append(estado)

def copiaTabuleiro(tabuleiro1, tabuleiro2):
    tabuleiro1.setPropLocal(tabuleiro2.getPropLocal())
    tabuleiro1.setPercAptidao(tabuleiro2.getPercAptidao())
    tabuleiro1.setValorFitness(tabuleiro2.getValorFitness())
    tabuleiro1.setTabuleiro(tabuleiro2.getTabuleiro())


def main():
    global qtdeRainhas, qtdeGeracoes, qtdePopInicial, qtdeMaxSelecao, MAX_INT
    while True:
        
        valoresValidosQtdeCruzamento = []

        qtdeRainhas = int(input("Informe a quantidade de Rainhas(>=4): "))

        if qtdeRainhas < 4:
            print("A quantidade de rainhas informada é inválida!")
            print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")
            continue
        
        qtdePopInicial = int(input("Informe quantos indivíduos haverá na população inicial(>= 4 e <=10): "))

        if qtdePopInicial < 4 or qtdePopInicial > 10:
            print("A quantidade de indivíduos na população inicial é inválida!")
            print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")
            continue

        populaValoresValidosQtdeCruzamento(valoresValidosQtdeCruzamento, qtdePopInicial)

        print("Valores Validos são: ", valoresValidosQtdeCruzamento)
        qtdeMaxSelecao = int(input("Informe quantos indivíduos serão selecionados para cruzamento: "))

        if not qtdeMaxSelecao in valoresValidosQtdeCruzamento:
            print("A quantidade de indivíduos selecionados para cruzamento é inválida!")
            print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")
            continue
        
        qtdeGeracoes = int(input("Informe quantas gerações de indivíduos devem ser gerados: "))

        popInicial = []

        melhorFilho = melhorIndividuoAteAgora(geraPopInicial(qtdeRainhas), MAX_INT)

        tempoInicial = tempoAtualMili()

        while True:
            popInicial = geraPopInicial(qtdeRainhas)
            
            for geracaoAtual in range(qtdeGeracoes):
                popSelecionada = selecionaIndividuos(popInicial)
                filhosGerados = cruzamentoDeIndividuos(popSelecionada)

                atualizaPopInicial(popInicial, filhosGerados)
                
                melhorFitnessAtual = melhorFilho.getValorFitness()

                if melhorFitnessAtual != 0:
                    novoMelhor = melhorIndividuoAteAgora(popInicial, melhorFitnessAtual)

                    if novoMelhor != None:
                        copiaTabuleiro(melhorFilho, novoMelhor)
                        melhorFilho.funcaoFitness()

                if melhorFilho.getValorFitness() == 0:
                    break
            
            if melhorFilho.getValorFitness() == 0:
                break
			

        melhorFilho.imprimirTabuleiro();	
        
        print("A execucao levou ", int((tempoAtualMili() - tempoInicial) / 1000), " segundos(s).")
        print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")

main()