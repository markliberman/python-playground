import random
# mineSweeper game.  Currently hard coded to 4 x 4 grid.  Could easily prompt
class mineSweeper:
    def __init__ (self, h: int, w: int):
      self.noBombValue = " "
      self.bombValue = "b"
      self.notDeterminedValue = "?"
      self.winningReturn = 1
      self.losingReturn = -1
      self.grid = [[self.notDeterminedValue for x in range(w)] for y in range(h)]
      self.h = h
      self.w = w
      self.m = 0

    # checks if cell [m,n] contains a comb
    def isBomb(self, m: int, n: int) -> bool:
      if self.grid[m][n] == self.bombValue:
          return True
      else:
          return False

    # helper function that provides min and max rows and columns for the adjacent
    # cells to cell [m,n]
    def getAdjacentCellRange(self, m: int, n:int) -> {}:
      adjacentCellRange = {}
      adjacentCellRange["minRow"] = max(0, m-1)
      adjacentCellRange["maxRow"] = min(self.h - 1, m + 1)
      adjacentCellRange["minCol"] = max(0, n-1)
      adjacentCellRange["maxCol"] = min(self.w - 1, n + 1)

      return adjacentCellRange

    # returns the count for the number of bombs adjacent to cell [m,n]
    def getAdjacentBombCounts(self, m: int, n: int) -> int:
      adjacentCellRange = self.getAdjacentCellRange(m, n)
      adjacentBombs = 0
      for i in range(adjacentCellRange["minRow"], adjacentCellRange["maxRow"] + 1):
        for j in range(adjacentCellRange["minCol"], adjacentCellRange["maxCol"] +1):
          if self.isBomb(i, j):
            adjacentBombs += 1

      return adjacentBombs

    # returns a boolen true if all adjacent cells have been exposed (either by choice)
    # or because they were exposed via adjacency logic
    def allAdjacentCellsExposed(self, m:int, n: int) -> bool:
      adjacentCellRange = self.getAdjacentCellRange(m, n)
      for i in range(adjacentCellRange["minRow"], adjacentCellRange["maxRow"] + 1):
        for j in range(adjacentCellRange["minCol"], adjacentCellRange["maxCol"] +1):
          if self.grid[i][j] == self.notDeterminedValue:
            return False

      return True

    # updates the adjacent counts for the current cell
    def updateCurrentCell(self, m: int, n: int):
      adjValue = self.getAdjacentBombCounts(m,n)
      if adjValue == 0:
        self.grid[m][n] = self.noBombValue
      else:
        self.grid[m][n] = adjValue
      return

    # updates all adjacent cells recursively with a count or a blank value for no adjacent bombs
    def updateAdjacentCells(self, m: int, n: int):
      adjacentCellRange = self.getAdjacentCellRange(m, n)
      if self.allAdjacentCellsExposed(m, n):
        self.updateCurrentCell(m,n)
        return

      for i in range(adjacentCellRange["minRow"], adjacentCellRange["maxRow"] + 1):
        for j in range(adjacentCellRange["minCol"], adjacentCellRange["maxCol"] +1):
          if self.grid[i][j] != self.bombValue:
            adjValue = self.getAdjacentBombCounts(i,j)
            if adjValue == 0:
              if self.grid[i][j] != self.noBombValue:
                self.grid[i][j] = self.noBombValue
                # call recursively
                self.updateAdjacentCells(i,j)
              else:
                return
            else:
              self.grid[i][j] = adjValue

    # returns true if game is over
    def didIWinYet(self) -> bool:
      for i in range(self.h):
        if self.notDeterminedValue in self.grid[i]:
          return False

      return True

    # populates the grid with a prompted number of bombs
    def addBombs(self):
      while self.m == 0:
        print("You are playing MineSweep on a ", self.h, " x ", self.w, "grid.")
        # totalBombs = int(input("Enter total number of bombs: "))
        totalBombs = input("Enter total number of bombs(int): ")
        try:
          totalBombs = int(totalBombs)
        except:
          print("That's not an integer number.")
          continue

        maxBombs = self.h * self.w
        if totalBombs < maxBombs:
          self.m = totalBombs
        else:
          print("Invalid number of bombs: ", "totalBombs.  Must be < ", maxBombs)

      cellList = list(range(self.h*self.w))
      bombs = random.sample(cellList, self.m)
      for i in range(self.h):
        for j in range(self.w):
          k = i*self.h
          if k + j in bombs:
            self.grid[i][j] = self.bombValue

    # Prompts user to make a choice (zero-based grid coordinates)
    def makeChoice(self) -> []:
      m = n = -1
      print("Enter your move [m,n] (zero based)")
      while m < 0:
        m = input("Enter your value for m: ")
        try:
          m = int(m)
        except:
          print("That's not an integer number.")
          m = -1
          continue

        if m + 1 > self.h:
          print("Invalid entry for m: ", m, ". Must be < ", self.h - 1)
          m = -1

      while n < 0:
        n = input("Enter your value for n: ")
        try:
          n = int(n)
        except:
          print("That's not an integer number.")
          n = -1
          continue

        if n + 1 > self.w:
              print("Invalid entry for n: ", n, ". Must be < ", self.w - 1)
              n = -1

      result = [m,n]
      return result

def main():
  ms = mineSweeper(4, 4)
  ms.addBombs()
  print("grid with bombs: ", ms.grid)

  # for i, choice in enumerate(choices):
  while True:
      choice = ms.makeChoice()
      print("choice: ", choice)
      if ms.isBomb(choice[0], choice[1]):
        print("I'm sorry.  You chose a bomb. You lose")
        return ms.losingReturn
      else:
        ms.updateAdjacentCells(choice[0], choice[1])
        print("updated grid: ", ms.grid)
        if ms.didIWinYet():
          print("Congratulations.  You win!")
          return ms.winningReturn

  return 0

main()

