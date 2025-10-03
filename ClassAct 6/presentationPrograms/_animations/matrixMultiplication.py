from manim import *

class MatrixMultiplicationAnimation(Scene):
    """
    Visualizes matrix multiplication: C = A * B.
    Shows how each entry in C is computed as a dot product of a row from A and a column from B.
    """
    def construct(self):
        # 1. Define matrices (3x3)
        A_data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        B_data = [
            [9, 8, 7],
            [6, 5, 4],
            [3, 2, 1]
        ]
        C_data = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        # 2. Create matrix mobjects and labels
        A = Matrix(A_data).scale(0.9)
        B = Matrix(B_data).scale(0.9)
        C = Matrix(C_data).scale(0.9)
        A_label = MathTex("A").next_to(A, UP)
        B_label = MathTex("B").next_to(B, UP)
        C_label = MathTex("C = A \\times B").next_to(C, UP)

        # Arrange matrices
        group = VGroup(
            VGroup(A_label, A),
            VGroup(B_label, B),
            VGroup(C_label, C)
        ).arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        self.play(FadeIn(group))
        self.wait(0.5)

        # 3. Animate computation of each entry in C
        A_entries = A.get_entries()
        B_entries = B.get_entries()
        C_entries = C.get_entries()

        n = 3  # Matrix size

        # Helper to highlight row and column
        def highlight_row_col(row, col):
            row_indices = [row * n + i for i in range(n)]
            col_indices = [i * n + col for i in range(n)]
            row_group = VGroup(*[A_entries[i] for i in row_indices])
            col_group = VGroup(*[B_entries[i] for i in col_indices])
            return row_group, col_group

        # Helper to compute dot product and animate
        for i in range(n):
            for j in range(n):
                row_group, col_group = highlight_row_col(i, j)
                target_entry = C_entries[i * n + j]

                # Highlight row and column
                self.play(
                    row_group.animate.set_color(YELLOW),
                    col_group.animate.set_color(BLUE),
                    run_time=0.5
                )

                # Show arrows from row and column to result entry
                arrows = VGroup(
                    Arrow(row_group.get_center(), target_entry.get_center(), buff=0.1, color=YELLOW),
                    Arrow(col_group.get_center(), target_entry.get_center(), buff=0.1, color=BLUE)
                )
                self.play(Create(arrows), run_time=0.3)

                # Compute value and update entry
                value = sum(A_data[i][k] * B_data[k][j] for k in range(n))
                new_entry = MathTex(str(value)).move_to(target_entry)
                self.play(Transform(target_entry, new_entry), run_time=0.5)
                self.wait(0.2)

                # Unhighlight and remove arrows
                self.play(
                    row_group.animate.set_color(WHITE),
                    col_group.animate.set_color(WHITE),
                    FadeOut(arrows),
                    run_time=0.3
                )

        self.wait(0.5)

        # 4. Final highlight
        self.play(Indicate(C, color=GREEN, scale_factor=1.1))
        self.wait(1)