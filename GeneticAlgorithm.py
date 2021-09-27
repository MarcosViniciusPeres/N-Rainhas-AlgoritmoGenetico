from EstadoTabuleiroGA import EstadoTabuleiroGA
import time
import sys

tempoInicial = 0    
qtdeRainhas = 0 
qtdeGeracoes = 0
qtdePopInicial = 0
qtdeMaxSelecao = 0
valoresValidosQtdeCruzamento = []

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

    
    
    

def main():
    global qtdeRainhas, qtdeGeracoes, qtdePopInicial, qtdeMaxSelecao
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

        MAX_INT = sys.maxsize

        melhorFilho = melhorIndividuoAteAgora(geraPopInicial(qtdeRainhas), MAX_INT)

        print("A execucao levou ", int((tempoAtualMili() - tempoInicial) / 1000), " segundos(s).")
        print("\n\n--------------------------------------------------------------------------------------------------------------------\n\n")

main()