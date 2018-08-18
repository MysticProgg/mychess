from Board import Board
from InputParser import InputParser
from AI import AI
import sys
import random

WHITE = True
BLACK = False


def askForPlayerSide():
    playerChoiceInput = input(
        "Выберите сторону: Белые(w) или черные(b).").lower()
    if 'w' in playerChoiceInput:
        print("Вы играете за белых")
        return WHITE
    else:
        print("Вы играете за черных")
        return BLACK


def askForDepthOfAI():
    depthInput = 2
    try:
        depthInput = int(input("Задайте глубину построения дерева решений.\n"
                               "При задании глубины >=3 возможно функциониривание будет медленным."))
    except:
        print("Неверные данные, установлено значение 2 по умолчанию.")
    return depthInput

# меню
def printCommandOptions():
    undoOption = 'u -- отмена последнего хода'
    printLegalMovesOption = 'l -- показать все возможные ходы'
    randomMoveOption = 'r -- сделать рандомный ход'
    quitOption = 'quit -- сдаться/выйти'
    moveOption = 'a3, Nc3, Qxa2 -- примеры возможных ходов'
    options = [undoOption, printLegalMovesOption, randomMoveOption,
               quitOption, moveOption, '', ]
    print('\n'.join(options))

# l
def printAllLegalMoves(board, parser):
    for move in parser.getLegalMovesWithShortNotation(board.currentSide):
        print(move.notation)

# r
def getRandomMove(board, parser):
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notationForMove(randomMove)
    return randomMove

# ход
def makeMove(move, board):
    print()
    print("Последний ход: " + move.notation)
    board.makeMove(move)

def printPointAdvantage(board):
    print("Сейчас разница в : " +
          str(board.getPointAdvantageOfSide(board.currentSide)))


def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()


def startGame(board, playerSide, ai):
    parser = InputParser(board, playerSide)
    while True:
        print(board)
        print()
        if board.isCheckmate():
            if board.currentSide == playerSide:
                print("ВЫ ПРОИГРАЛИ!")
            else:
                print("ВЫ ПОБЕДИЛИ!")
            return

        if board.isStalemate():
            if board.currentSide == playerSide:
                print("ПАТ")
            else:
                print("ПАТ")
            return

        if board.currentSide == playerSide:
            # printPointAdvantage(board) - доделать
            move = None
            command = input("Ваша очередь ходить."
                            " Нажмите '?' для вызова меню. ").lower()
            if command == 'u':
                undoLastTwoMoves(board)
                continue
            elif command == '?':
                printCommandOptions()
                continue
            elif command == 'l':
                printAllLegalMoves(board, parser)
                continue
            elif command == 'r':
                move = getRandomMove(board, parser)
            elif command == 'quit':
                return
            else:
                move = parser.moveForShortNotation(command)
            if move:
                makeMove(move, board)
            else:
                print("Некорректный синтаксический ввод, повторите запрос")

        else:
            print("AI думает...")
            move = ai.getBestMove()
            move.notation = parser.notationForMove(move)
            makeMove(move, board)

board = Board()
playerSide = askForPlayerSide()
print()
aiDepth = askForDepthOfAI()
opponentAI = AI(board, not playerSide, aiDepth)

try:
    startGame(board, playerSide, opponentAI)
except KeyboardInterrupt:
    sys.exit()
