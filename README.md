<p align="center"><img src="/.github/poster.jpg"></p>

<h1 align="center">SuperHero Quotes</h1>
<p align="center">An api consisting huge collection of handpicked Marvel & DC SuperHeros and Supervillains quotes!:zap:</p>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Base API URL:
`https://superhero-quotes.herokuapp.com/`

## Endpoints:

- `/grab?banner=mcu` or `/grab?banner=dcu`: Returns 10 random quote for the given banner. You can also fetch more than 10 quote at a time by passing `size` parameter, like: `/grab?banner=mcu&size=2`
will return two quotes from Marvel's collection.

- Note: Max size limit is `50` (fifty)

**Example response**:
```json
{
    "StatusCode": 200,
    "Banner": "Marvel Cinematic Universe (MCU)",
    "TotalQuotes": 2,
    "Items": [
        {
            "id": "6SYjJebRR8fCF9SnvFZBKQ",
            "data": {
                "author": "Iron Man",
                "quote": "You know what, give me a break, Steve. I just got hit in the head with a Hulk."
            }
        },
        {
            "id": "2cquLZiJsUbg5jtQrdwLkM",
            "data": {
                "author": "Thanos",
                "quote": "You have my respect, stark. When I'm done, half of humanity will still be alive. I hope they remember you."
            }
        }
    ]
}
```

- `/random`: Will return single randomly chosen quote from either Marvel or DC collection.

**Example response**:
```json
{
    "StatusCode": 200,
    "Banner": "DC Universe (DCU)",
    "Stuff": {
        "id": "c4ZuUeSUzjGiCEVUmsrYWN",
        "data": {
            "author": "Wonder Woman",
            "quote": "Death is necessary. It is part of life, and if we say life is a blessing, we must say that death is a blessing, as well."
        }
    }
}
```

- `/quoteId/<quote_id>` will return specific quote for the given `quote_id`. Like: `/quoteId/k3fhzAKsvCeuFhXPHPQcnT`.

**Example response**:
```json
{
    "StatusCode": 200,
    "Stuff": {
        "id": "k3fhzAKsvCeuFhXPHPQcnT",
        "data": {
            "author": "The Joker",
            "quote": "The pen, is truly mightier than the sword! "
        }
    }
}
```

## Collection updates:
Quotes collection will be updated frequently from new movie releases from both Marvel & DCU or whenever i have some great findings!

## Contribute

Have an idea? Found a bug? Create [a new issue](https://github.com/starry69/SuperHero-Quotes/issues) with detailed description.

## License

[MIT][license] © [Stɑrry Shivɑm][github]

[license]: /LICENSE
[github]: https://github.com/starry69
