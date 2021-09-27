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

#Assumimos que deve ser um valor par e que deve ter pelo menos 2 a menos que o tamanho da população inicial
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

#realiza cópia de um tabuleiro em uma nova posição de memória
def copiaRegistro(origem):
    novoReg = EstadoTabuleiroGA(qtdeRainhas)

    novoReg.setPercAptidao(origem.getPercAptidao())
    novoReg.setPropLocal(origem.getPropLocal())
    novoReg.setValorFitness(origem.getValorFitness())
    novoReg.setTabuleiro(origem.getTabuleiro())
		
    return novoReg

#realiza a operação de seleção de individuos
def selecionaIndividuos(popInicial):
    indivSelecionados = []
    probTotal = 0

    #setando probabilidade local de cada estado e obtendo a probabilidade geral de todos os estados
    for indice in range(len(popInicial)):
        aptidao = popInicial[indice].getValorFitness()
        propLocal = ((aptidao - 100) * - 1)
        popInicial[indice].setPropLocal(propLocal)
        probTotal += propLocal

    #setando percentual de aptidão para ser escolhido
    for indice in range(len(popInicial)):
        probLocal = popInicial[indice].getPropLocal()
        popInicial[indice].setPercAptidao(probLocal / probTotal)

    #realizando escolha de modo aleatório através da técnica de PROBABILIDADE ACUMULADA
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

#realiza a operação de crossover/cruzamento
def cruzamentoDeIndividuos(popSelecionada):
    filhosCruzados = []


    #trecho abaixo selecionará o ponto de corte e obterá gene dos pais para realizar crossover
    for pai1 in range(len(popSelecionada)-1):
        pai2 = (pai1 + 1)
        posicaoDeCorte = random.randint(0,  qtdeRainhas-1)

        filhoCruzado1 = EstadoTabuleiroGA(qtdeRainhas)
        filhoCruzado2 = EstadoTabuleiroGA(qtdeRainhas)

        genesPai1 = popSelecionada[pai1].getTabuleiro()
        genesPai2 = popSelecionada[pai2].getTabuleiro()

        #realizando crossover, ou seja, trocando parte dos genes dos pais para em seguida gerar filhos
        for posicao in range(posicaoDeCorte):
            linha = genesPai1[posicao]
            genesPai1[posicao] = genesPai2[posicao]
            genesPai2[posicao] = linha
        
        #setando novos dados dos pais que foram cruzados nos filhos
        filhoCruzado1.setTabuleiro(genesPai1)
        filhoCruzado2.setTabuleiro(genesPai2)
        filhosCruzados.append(filhoCruzado1)
        filhosCruzados.append(filhoCruzado2)
        
        pai1 += 1
    
    return filhosCruzados

#atualiza população inicial com os novos filhos otimizados usando ELITISMO
#1 dos pais será inserido aleatoriamente, dando chance a manter pais ruins e possivelmente gerar filhos melhores a partir dele futuramente
def atualizaPopInicial(popInicial, filhosGerados):
    novaPopInicial = []

    #ordenando de casos bons até os ruins
    popInicial = sorted(popInicial, key= EstadoTabuleiroGA.getValorFitness)
    filhosGerados = sorted(filhosGerados, key= EstadoTabuleiroGA.getValorFitness)

    #escolhendo pai aleatoriamente para continuar na população inicial
    paiRandomIndice = random.randint(0,  qtdePopInicial-1)
    paiRandom = copiaRegistro(popInicial[paiRandomIndice])
    novaPopInicial.append(paiRandom)

    qtdeAInserir = len(popInicial)

    #inserindo regs do pai
    for indice in range(int((qtdeAInserir/2)-1)):
        novaPopInicial.append(popInicial[indice])

    #inserindo regs dos filhos gerados a partir de cruzamentos
    for indice in range(int((qtdeAInserir/2))):
        novaPopInicial.append(filhosGerados[indice])
    
    #resetando população inicial
    popInicial = []

    #reinserindo dados na população inicial
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