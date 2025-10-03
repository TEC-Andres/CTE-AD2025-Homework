from manim import *

class MatrixTransposeAnimation(Scene):
    """
    An animation demonstrating the process of transposing a matrix.
    This scene visualizes the swapping of elements across the main diagonal.
    """
    def construct(self):
        # 1. Setup and display the original matrix
        matrix_data = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        
        # Create the matrix mobject and its label
        matrix = Matrix(matrix_data, h_buff=1.5, v_buff=1.2).scale(1.1)
        matrix_label = MathTex("A =").next_to(matrix, LEFT, buff=0.5)

        self.play(Write(matrix_label), Write(matrix))
        self.wait(0.5)

        # 2. Explain the transposition process
        explanation = Tex(
            "Transposing swaps elements across the main diagonal.",
            " An element at (row $i$, col $j$) moves to (row $j$, col $i$)."
        ).scale(0.8).to_edge(UP)
        self.play(Write(explanation))
        self.wait(1.25)
        self.play(FadeOut(explanation))

        # 3. Animate the swapping of elements
        
        # We only need to iterate through the upper triangle of the matrix
        # Manim's get_entries() uses 1-based indexing for (row, col)
        rows = len(matrix_data)
        cols = len(matrix_data[0])
        entries = matrix.get_entries()

        for i in range(rows):
            for j in range(i + 1, cols):
                # Get the mobjects for the elements to be swapped
                idx1 = i * cols + j
                idx2 = j * cols + i
                entry1 = entries[idx1]
                entry2 = entries[idx2]

                # Highlight the pair being swapped
                self.play(
                    entry1.animate.set_color(YELLOW),
                    entry2.animate.set_color(YELLOW)
                )

                # Create curved arrows to show the swap path
                arrow1 = CurvedArrow(entry1.get_center(), entry2.get_center(), angle=-PI/2, color=BLUE)
                arrow2 = CurvedArrow(entry2.get_center(), entry1.get_center(), angle=-PI/2, color=BLUE)

                self.play(Create(arrow1), Create(arrow2))

                # Use the Swap animation
                self.play(Swap(entry1, entry2))
                self.wait(0.3)

                # Clean up for the next pair
                self.play(
                    FadeOut(arrow1, arrow2),
                    entry1.animate.set_color(WHITE),
                    entry2.animate.set_color(WHITE)
                )
        self.wait(0.5)

        # 4. Show the final result with a new label
        transposed_label = MathTex("A^T =").next_to(matrix, LEFT, buff=0.5)
        self.play(Transform(matrix_label, transposed_label))

        # 5. Highlight the main diagonal, which is unchanged
        diagonal_elements = VGroup(*[entries[i * cols + i] for i in range(rows)])

        diag_text = Tex("The main diagonal is unchanged.").scale(0.8).next_to(matrix, DOWN, buff=0.7)
        self.play(Write(diag_text))
        self.play(Indicate(diagonal_elements, color=GREEN, scale_factor=1.5))

        self.wait(1.5)