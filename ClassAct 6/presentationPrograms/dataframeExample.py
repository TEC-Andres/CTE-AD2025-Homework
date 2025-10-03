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

if __name__ == "__main__":
    data = [
        ["Alice", 24],
        ["Bob", 30],
        ["Charlie", 29],
        ["Diana", 22]
    ]
    df = DataFrame(data, ["Name", "Age"])
    print("DataFrame with auto-generated ID column:")
    a = input("Do you want to add a new row? (y/n): ")
    if a.lower() == 'y':
        name = input("Enter name: ")
        age = int(input("Enter age: "))
        df.append([len(df.data) + 1, name, age])

    print(df.head(10))
    print(f"Memory usage: {df.memory_usage()} bytes")
    
