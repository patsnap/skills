# HOQ Symbols and Scores

Use this file when explaining the relationship or roof matrices.

## Relationship Strengths

| Symbol | Value | Meaning |
| --- | ---: | --- |
| `◎` | 9 | strong driver of the requirement |
| `○` | 3 | meaningful but secondary driver |
| `△` | 1 | weak relationship |
| blank | 0 | no material relationship |

## Roof Correlations

| Symbol | Meaning |
| --- | --- |
| `++` | strong positive correlation |
| `+` | positive correlation |
| blank | no material correlation |
| `-` | negative correlation |
| `--` | strong negative correlation / conflict |

## Practical Reading Rules

- High feature score means the feature influences many high-importance requirements.
- A top-ranked feature with repeated `--` correlations is usually a priority with implementation tension.
- Do not describe a relationship as strong unless the artifact actually assigns `9` or `◎`.
