# Lists in lists 
In python, a list is an object that allow us to store an array of different datatypes. A list of lists are a list that contains multiple of these arrays within itself. The syntax goes as follow:

```python
[[],[],[]]
```
_Fig 1: a list containing multiple empty lists._

# Use cases 
## Matrices

In python, an n×m matrix is defined by placing the following structure
```python
A = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```

Matrices are useful, they allow us to do operations with other mathematical objects like vectors, networks, linear transformations, etc...

### Matrix multiplication

Matrix multiplication is a binary operation that combines two matrices to produce a new matrix, called the matrix product

Here is a video animation demonstrating matrix multiplication:


<iframe width="640" height="360" src="./_animations/media/videos/matrixMultiplication/1080p60/MatrixMultiplicationAnimation.mp4" frameborder="0" allowfullscreen></iframe>

```python
def matrix_multiply(A, B):
    m = len(A)
    n = len(A[0])
    p = len(B[0])

    result = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result
```
_Fig 2: O(n^3) version of Matrix multiplication._

ADVANCED:
Using the strassen matrix multiplication algorithm in combination with `ctypes`, we are able to do a matrix multiplication at O(n^(log_2(7))); parring with C compilation speed*.


### Transposition
Matrix transposition is an operation that creates a new matrix by switching the rows and columns of an original matrix

Here is a video animation demonstrating matrix transposition:

![Matrix Transposition Animation](https://github.com/your-username/your-repo/raw/main/_animations/media/videos/transposition/1080p60/MatrixTransposeAnimation.mp4)


```python
def transpose_matrix(matrix):
    """Return the transpose of a 2D matrix."""
    return [list(row) for row in zip(*matrix)]
```

## Dataframes [dfs]
Dataframes are a 2 dimensional data structure, like a 2 dimensional array, or a table with rows and columns.
```python
data = [
        ["Alice", 24],
        ["Bob", 30],
        ["Charlie", 29],
        ["Diana", 22]
    ]
```

ADVANCED
For the handling of dataframes, it is usually used external libraries like Pandas, but with some OOP structure it is possible to apply dataframes without using any libraries. 
```python
class DataFrame:
    def __init__(self, data, columns=None):
        self.memory = 0
        if columns:
            if "ID" not in columns:
                self.columns = ["ID"] + columns
                self.data = [[i+1] + row for i, row in enumerate(data)]
            else:
                self.columns = columns
                self.data = data
        else:
            self.columns = [f"col{i}" for i in range(len(data[0]))]
            self.data = data

    def __repr__(self):
        col_widths = [
            max(len(str(row[i])) for row in self.data + [self.columns])
            for i in range(len(self.columns))
        ]
        header = " | ".join(f"{col:<{col_widths[i]}}" for i, col in enumerate(self.columns))
        rows = "\n".join(
            " | ".join(f"{str(row[i]):<{col_widths[i]}}" for i in range(len(self.columns)))
            for row in self.data
        )
        separator = "-" * len(header)
        return f"{header}\n{separator}\n{rows}"

    def shape(self):
        return (len(self.data), len(self.columns))

    def select(self, col):
        """Select a column by index or column name (no dicts used)."""
        if isinstance(col, int):
            col_index = col
        elif isinstance(col, str):
            col_index = self.columns.index(col)   # lookup via list, no dict
        else:
            raise TypeError("col must be int or str")
        return [row[col_index] for row in self.data]

    def row(self, row_index):
        return self.data[row_index]

    def head(self, n=5):
        """First n rows as a new DataFrame."""
        return DataFrame(self.data[:n], self.columns)
    
    def memory_usage(self):
        """Estimate memory usage in bytes."""
        total_size = 0
        for row in self.data:
            for item in row:
                total_size += len(str(item).encode('utf-8'))
        for col in self.columns:
            total_size += len(str(col).encode('utf-8'))
        return total_size
    
    def append(self, row):
        if len(row) != len(self.columns):
            raise ValueError("Row length must match number of columns")
        self.data.append(row)
```