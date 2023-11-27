def maxSumDistinctSum(matrix, size):
    rows = len(matrix)
    cols = len(matrix[0])

    # Calculate the cumulative sum matrix
    cumulative_sum = [[0] * (cols + 1) for _ in range(rows + 1)]

    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            cumulative_sum[i][j] = matrix[i - 1][j - 1] + cumulative_sum[i - 1][j] + cumulative_sum[i][j - 1] - cumulative_sum[i - 1][j - 1]

    maxSum = 0
    maxSums = set()

    for i in range(size, rows + 1):
        for j in range(size, cols + 1):
            submatrix_sum = cumulative_sum[i][j] - cumulative_sum[i - size][j] - cumulative_sum[i][j - size] + cumulative_sum[i - size][j - size]
            distinct_numbers = set()

            for x in range(i - size, i):
                for y in range(j - size, j):
                    distinct_numbers.add(matrix[x][y])

            if submatrix_sum > maxSum:
                maxSum = submatrix_sum
                maxSums = distinct_numbers
            elif submatrix_sum == maxSum:
                maxSums.update(distinct_numbers)

    return sum(maxSums)

# Example usage:
matrix = [
    [1, 0, 1, 5,6],
    [3,3,0,3,3],
    [2, 9,2,1,2],
    [0,2,4,2,0]
]
size = 2

result = maxSumDistinctSum(matrix, size)
print("Sum of distinct numbers from submatrices with max sum:", result)
