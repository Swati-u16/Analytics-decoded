# Analytics Decoded

Code behind the *Analytics Decoded* series on Towards Data Science: the commercial
analytics work that happens before the algorithm, explained for people starting out.

Every article uses simulated data with a fixed random seed, so every number printed in
the article reproduces exactly. No real person, company or programme is described.

| Folder | Article | What it covers |
| --- | --- | --- |
| `01-six-first-cuts` | Six Problems, One First Cut | The one number to compute first, across healthcare, banking, technology, e-commerce, consumer goods and government |

## Run it

```bash
pip install -r requirements.txt
cd 01-six-first-cuts
python first_cut.py     # prints every number in the article
python figures.py       # redraws the article figures into figures/
```

Figures use the Poppins and Lora typefaces (Google Fonts). Install them, or edit the
`FONTS` path at the top of `figures.py`.

## Licence

Code: MIT. Article text and figures © the author.
