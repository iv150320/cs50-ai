# Analysis

## Layer 4, Head 11

This attention head appears to focus on preposition-object relationships. Prepositions like "through" and "on" show strong attention toward the noun objects they govern. In the sentence "She walked through the forest," the preposition "through" attends most strongly to "forest" (0.634), suggesting this head has learned to identify the connection between a preposition and the noun that follows it as its object. Similarly, in "The cat sat on the mat," the preposition "on" attends strongly to "mat" (0.869). This pattern indicates that BERT has at least one attention head dedicated to understanding prepositional phrases and the grammatical relationship between prepositions and their objects.

Example Sentences:
- She walked through the forest.
- The cat sat on the mat.
- He put the book on the table.

## Layer 7, Head 2

This attention head shows interesting patterns related to determiner sequences and grammatical structure. The head demonstrates attention patterns between consecutive determiners, suggesting it has learned to recognize how articles and determiners relate to each other within noun phrases. In the sentence "An old man walked down the street," the first "the" strongly attends to "an" (0.713), indicating awareness of how consecutive articles relate. This could be part of BERT's way of understanding definite vs. indefinite reference and how different noun phrases relate within a sentence.

Example Sentences:
- A dog chased the cat.
- The small bird flew away.
- An old man walked down the street.

## Layer 3, Head 1

This attention head exhibits a clear "next token" attention pattern where each token attends most strongly to the token that immediately follows it. For example, in "The happy child ate the sweet apple," the word "happy" strongly attends to "child" (1.00), "child" attends to "ate" (1.00), and "sweet" attends to "apple" (1.00). This pattern suggests this head has learned positional awareness, where understanding a word depends heavily on knowing what word comes next. This is consistent with how language often relies on sequential context for meaning.

Example Sentences:
- The happy child ate the sweet apple.
- A small brown dog barked loudly.
- The tall building stood quietly.

