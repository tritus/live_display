from matrix.matrix_display import *

try:
  chained_matrices = 4
  matrix_rows = 32

  matrix_displayer = MatrixDisplay(matrix_rows, chained_matrices)
  matrix_displayer.start_display()

except KeyboardInterrupt:
  matrix_displayer.reset_screen
