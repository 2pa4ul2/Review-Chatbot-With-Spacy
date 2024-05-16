import re

# Example data
possible_triple = ["apple", "Apple", "I like Apples and oranges"]

# Case-insensitive replacement
replaced_sentence = re.sub(re.escape(possible_triple[1]), '_' * len(possible_triple[1]), possible_triple[2], flags=re.IGNORECASE)
print(replaced_sentence)
