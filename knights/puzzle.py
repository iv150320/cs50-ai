from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is either a knight or a knave (not both)
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # A says "I am both a knight and a knave" (this sentence is false)
    # If A is a knight, the statement is true
    # If A is a knave, the statement is false
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B is either a knight or a knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A says "We are both knaves"
    # If A is a knight, the statement is true (both are knaves)
    # If A is a knave, the statement is false (not both are knaves)
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B is either a knight or a knave
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # A says "We are the same kind" (both knights OR both knaves)
    # Same kind = (AKnight ∧ BKnight) ∨ (AKnave ∧ BKnave)
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # B says "We are of different kinds" (one knight, one knave)
    # Different kinds = (AKnight ∧ BKnave) ∨ (AKnave ∧ BKnight)
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
#
# A cannot say "I am a knave" because:
#   - If A is knight, saying "I am knave" is a lie (knight can't lie)
#   - If A is knave, saying "I am knave" is truth (knave can't tell truth)
# So A must have said "I am a knight" and A must be knave
#
# B says "A said 'I am knave'" which is false → B is knave
# B says "C is knave" which is false → C is knight
# C says "A is knight" which is false (A is knave) → C is knave
# Solution: A=knave, B=knave, C=knave
knowledge3 = And(
    # Each character is either a knight or a knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    # A must be knave (knight can't say false, knave can't say true)
    AKnave,
    # B says false things
    BKnave,
    # C says false things
    CKnave
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
