import numpy as np

test_matrix = np.array((1, 8))
test_matrix2 = np.array((4, 6))
solutions = [(1, 1), (2, 2)]

result_matrix = np.linalg.solve([test_matrix, test_matrix2], solutions)
print(test_matrix)
print(result_matrix)
print(np.matmul(test_matrix, result_matrix))
print(np.matmul(test_matrix2, result_matrix))