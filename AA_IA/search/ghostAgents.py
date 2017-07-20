# ghostAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util

class GhostAgent( Agent ):
  def __init__( self, index ):
    self.index = index

  def getAction( self, state ):
    dist = self.getDistribution(state)
    if len(dist) == 0: 
      return Directions.STOP
    else:
      return util.chooseFromDistribution( dist )
    
  def getDistribution(self, state):
    "Returns a Counter encoding a distribution over actions from the provided state."
    util.raiseNotDefined()

class RandomGhost( GhostAgent ):
  "A ghost that chooses a legal action uniformly at random."
  def getDistribution( self, state ):
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist

class DirectionalGhost( GhostAgent ):
  "A ghost that prefers to rush Pacman, or flee when scared."
  def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
    self.index = index
    self.prob_attack = prob_attack
    self.prob_scaredFlee = prob_scaredFlee
  
  def getGhostSuccessors(self, state):
      legalActions = state.getLegalActions( self.index )
      return [(state.generateSuccessor( self.index , action), action, state.generateSuccessor( self.index , action).getGhostPosition(self.index) ) for action in legalActions]
      
  def getDistribution( self, state ):
    #Le variaveis de state
    ghostState = state.getGhostState( self.index ) #Atibui a ghostState o estado referente a cada fantasma, cada fantasma e representado por um index
    pos = state.getGhostPosition( self.index ) #Atribui a pos a posicao de cada fantasma
    isScared = ghostState.scaredTimer > 0 #variavel booleana que informa se o fantasma esta ou nao no modo assustado
    pacmanPosition = state.getPacmanPosition() #Atribui a pacmanPosition a posicao do pacman
    fantasmas = state.getGhostPositions() #fantasmas retorna uma lista de tuplas com as posicoes (X,Y) de cada fantasma

    #O bloco if abaixo e executado caso o fantasma esteja assustado e faz com que o fantasma escape do pacman
    if isScared:
      suc = self.getGhostSuccessors(state) #Retorna todas as possiveis acoes que o fantasma pode tomar
      '''Para cada possibilidade de nova posicao que o fantasma pode ir, a distancia entre o fantasma e o pacman e 
      calculada e, a maior distancia e escolhida como nova posicao do fantasma'''
      d, local = max((util.manhattanDistance(s[2], pacmanPosition), s[1]) for s in suc )
      dist = util.Counter()
      dist[local] = 1
      dist.normalize()
      return dist
    #O bloco else abaixo e executado caso o fantasma nao esteja assustado e, nesse momento inicia a execucao da busca A*
    else:
      filaPrioridade = util.PriorityQueue() #Cria a fila de prioridades que, neste momento esta vazia
      visitados = fantasmas
      filaPrioridade.push((state,[]) , 0)
      while not filaPrioridade.isEmpty():
        stateAtual , acao = filaPrioridade.pop()

        if stateAtual.getGhostPosition(self.index) == pacmanPosition:
          dist = util.Counter()
          dist[acao[0]] = 1
          return dist

        for stateProximo, acaoProximo, posProximo in self.getGhostSuccessors(stateAtual):
            if not posProximo in visitados: #So expande a posicao caso ela nao pertenca as posicoes ja visitadas
              novaAcao = acao + [acaoProximo]
              '''Adiciona o novo estado do fantasma que foi colocado na fila atribuindo sua funcao objetivo que e
              o custo que teve da acao inicial (len(novaAcao)) ate essa acao atual acrescido da heuristica que, nesse 
              caso e o calculo da distancia de Manhattan'''
              filaPrioridade.push((stateProximo, novaAcao), len(novaAcao) + util.manhattanDistance(posProximo, pacmanPosition))
              visitados = visitados + [posProximo]
    
    '''No caso de o fantasma nao ter encontrado o caminho ate o pacman, isto e, de ele ja ter o cercado, os passos
    abaixo realizam uma distribuicao que atribui um valor qualquer a posicao do fantasma'''
    dist = util.Counter()
    for a in state.getLegalActions( self.index ): dist[a] = 1.0
    dist.normalize()
    return dist
      
