# Basic Uses

Setting up a synchronous client is easy, like so:
```py
from qbreader import Sync as qbr

sync_client = qbr()
```

- Print three tossups 
```py
for tossup in sync_client.random_tossup(number=3):
    print(tossup)
```

- Print three *recent* (but not too recent maybe because you've carded all of 2024 somehow) tossups
```py
for tossup in sync_client.random_tossup(number=3, min_year=2020, max_year=2023):
    print(tossup)
```

## Tossups by Category
This API exposes multiple ways to access a `random_tossup` *by category*.

For example, by a raw string literal
```py
for tossup in sync_client.random_tossup(number=3, categories=["Science"]):
    print(tossup)
```

However, you are likely to get an error if you do not capitalize properly or make a spelling mistake. Instead, if you have some sort of language server installed (or all-in-one extensions like VSCode Python), then figuring out what you want will be a lot easier through importing the QBReader module's `types`.
```py
from qbreader import types

# Type alias
Category = types.Category

for tossup in sync_client.random_tossup(number=3, categories=[Category.SCIENCE]):
    print(tossup)
```
This way, while typing (:smile:), your language server should give an autocomplete on this. This is usually a better strategy than trying to guess the string that is right.

## Tossup by Difficulty

- Maybe you want a challenge, say college-medium (7) and college-hard (8). Then you can filter by difficulty.
```py
for tossup in sync_client.random_tossup(number=3, difficulties=[7, 8])
    print(tossup)
```

## Bonuses

- Most quizbowl bonuses have three parts, but there are some bonuses in the QBReader database that are not the classic 3-part bonuses. By default, `random_bonus` returns ***all types of bonuses***. To adjust for only 3-part bonuses, you can do:
```py
for bonus in sync_client.random_bonus(three_part_bonuses=True):
    print(bonus)
```

> Anyhow, the odds you will get a non 3-part bonus is pretty low.

- The options you had for `random_tossup` can also be toggled for `random_bonus`
  
```py
for bonus in sync_client.random_bonus(number=3, difficulties=[4, 5], min_year=2010, max_year=2020, categories=[Category.FINE_ARTS] three_part_bonuses=True):
    print(bonus)
```

# Examples

## Simple quizbowl trainer CLI

Here is a working example of a simple quizbowl trainer CLI. 

```py
from qbreader import Sync
import time

# Set up synchronous client
sync_client = Sync()

# Set up session configuration
num_correct = 0
num_tossups = int(input("How many tossups do you want to answer? "))

# Clear the screen
print("\033c")

# Get tossups
tossups = sync_client.random_tossup(number=num_tossups)

# Read each tossup
for i, tossup in enumerate(tossups):

    # Print title and set up ANSI color
    print(f"Tossup {i+1}:",
          end="\033[94m\n")

    # Print word by word
    for word in tossup.question_sanitized.split():
        # Print word, flush to see tossup after `time.sleep`
        print(f"{word} ", end="", flush=True)

        # Delay for each word in seconds
        time.sleep(0.1)

    # Reset color, go to next line
    print("\033[0m\n")

    # Get user input
    response = input("Answer: ", end="\033[90m\n")

    # Check if answer is correct
    if sync_client.check_answer(tossup.answer, response):

        num_correct += 1

        # Green color for correct answer
        print("\033[92m", "Correct!", sep="")

        # Reset color, go to next line
        print("\033[0m\n")

    else:

        # Red color for incorrect answer
        print("\033[91m",
              f"Incorrect. Correct Answer: {tossup.answer_sanitized}", sep="")

        # Reset color, go to next line
        print("\033[0m\n")

# Clear the screen, end of program
print("\033c")
print("All done!")

# Print session summary
accuracy = num_correct / num_tossups * 100
print(f"Accuracy: {accuracy:.2f}%")
```