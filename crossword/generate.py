import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            # Remove words that don't match the variable's length
            self.domains[var] = {
                word for word in self.domains[var]
                if len(word) == var.length
            }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        
        # Get overlap between x and y
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        
        i, j = overlap  # x[i] must equal y[j]
        
        # For each value in x's domain, check if there's a matching value in y's domain
        to_remove = set()
        for x_value in self.domains[x]:
            # Check if there's at least one y value that works with x_value
            has_match = False
            for y_value in self.domains[y]:
                if x_value[i] == y_value[j]:
                    has_match = True
                    break
            
            if not has_match:
                to_remove.add(x_value)
                revised = True
        
        # Remove inconsistent values from x's domain
        for value in to_remove:
            self.domains[x].remove(value)
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Initialize queue of arcs
        if arcs is None:
            queue = [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]
        else:
            queue = list(arcs)
        
        # Process queue
        while queue:
            x, y = queue.pop(0)
            
            # Revise x with respect to y
            if self.revise(x, y):
                # If domain is empty, no solution
                if len(self.domains[x]) == 0:
                    return False
                
                # Add all neighbors of x (except y) back to queue
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        queue.append((neighbor, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return all(var in assignment for var in self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check all values are distinct
        used_words = []
        for var, word in assignment.items():
            # Check length constraint
            if len(word) != var.length:
                return False
            
            # Check distinctness
            if word in used_words:
                return False
            used_words.append(word)
        
        # Check for conflicts between neighbors
        for var, word in assignment.items():
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        if word[i] != assignment[neighbor][j]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Get unassigned neighbors
        neighbors = [n for n in self.crossword.neighbors(var) if n not in assignment]
        
        # For each value, count how many options it eliminates for neighbors
        value_counts = []
        for value in self.domains[var]:
            eliminated = 0
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap:
                    i, j = overlap
                    # Count how many neighbor values are eliminated
                    for neighbor_value in self.domains[neighbor]:
                        if value[i] != neighbor_value[j]:
                            eliminated += 1
            value_counts.append((eliminated, value))
        
        # Sort by number eliminated (ascending)
        value_counts.sort()
        
        return [value for _, value in value_counts]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [v for v in self.crossword.variables if v not in assignment]
        
        # Sort by domain size (ascending), then by degree (descending)
        # Degree = number of neighbors
        unassigned.sort(key=lambda v: (
            len(self.domains[v]),
            -len(self.crossword.neighbors(v))  # negative for descending
        ))
        
        return unassigned[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Base case: assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Select unassigned variable
        var = self.select_unassigned_variable(assignment)
        
        # Try each value in domain
        for value in self.order_domain_values(var, assignment):
            # Add value to assignment
            assignment[var] = value
            
            # Check if assignment is consistent
            if self.consistent(assignment):
                # Inference: enforce arc consistency
                saved_domains = {v: self.domains[v].copy() for v in self.domains}
                
                # Infer by running AC3 on neighbors of var
                arcs = [(neighbor, var) for neighbor in self.crossword.neighbors(var)]
                if self.ac3(arcs):
                    # Recursively try to complete assignment
                    result = self.backtrack(assignment)
                    if result is not None:
                        return result
                
                # Rollback if no solution found
                self.domains = saved_domains
            
            # Remove value from assignment
            assignment.pop(var)
        
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
