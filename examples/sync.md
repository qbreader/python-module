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

However, you are likely to get an error if you do not capitalize properly or make a spelling mistake. Instead, if you have some sort of LSP installed (or all-in-one extensions like VSCode Python), then figuring out what you want will be a lot easier through importing the QBReader module's `types`.
```py
from qbreader import types

# Type alias
Category = types.Category

for tossup in sync_client.random_tossup(number=3, categories=[Category.SCIENCE]):
    print(tossup)
```
This way, while typing (:smile:), your LSP should give an autocomplete on this. This is usually a better strategy than trying to guess the string that is right.

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
