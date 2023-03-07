![coverage badge](./coverage.svg)


![serply logo](./images/serply_logo.png)

# Serply Python SDK

Serply is a Python SDK for the Serply API. It provides a simple interface to the API, and handles all the authentication and request signing for you.

## Installation

Using PyPi

```bash
pip install serply
```

From source

```bash
git clone https://github.com/serply-inc/serply-python.git
cd serply-python
pip install .
```

## Usage

### Web Search

Basic search for `iphone 15 specs`
```python
from serply import Serply

serply = Serply('your_api_key')
results = serply.search('iphone 15 specs')
```

The library also supports async requests using `aiohttp` for more efficient high volume queries.

```python
import asyncio
from serply import Serply

serply = Serply('your_api_key')
results = asyncio.run(serply.search_async('iphone 15 specs'))
```

### Web Search with options

Web search results (100 results, default is 10)

```python
results = serply.search('iphone 15 specs', num=100)
```

Paging results (start at 20th result, default to 0)

```python
results = serply.search('iphone 15 specs', start=20)
```

Perform search in a [specific language](#search-language-codes--lr-) (Spanish) 

```python
results = serply.search(keyword="iphone", lr="lang_es")
```

### Video Search

Basic video search for `smart phone reviews`

```python
results = serply.video('smart phone reviews')
```

### Image Search

Basic image search for `coffee drinks`

```python
results = serply.image('coffee drinks')
```

### Product Search

Basic image search for `iphones`

```python
results = serply.product('coffee drinks')
```

### Jobs Search

Basic Job search for `nurse practitioner`

```python
resources = serply.job('nurse practitioner')
```

### News Search

Basic News search for `bitcoin`

```python
results = serply.news('bitcoin')
```


## Advance Parameters

### Web Interface Language Codes (hl)

Web Interface Language Codes
```
hl=af          Afrikaans
hl=ak          Akan
hl=sq          Albanian
hl=am          Amharic
hl=ar          Arabic
hl=hy          Armenian
hl=az          Azerbaijani
hl=eu          Basque
hl=be          Belarusian
hl=bem         Bemba
hl=bn          Bengali
hl=bh          Bihari
hl=xx-bork     Bork, bork, bork!
hl=bs          Bosnian
hl=br          Breton
hl=bg          Bulgarian
hl=km          Cambodian
hl=ca          Catalan
hl=chr         Cherokee
hl=ny          Chichewa
hl=zh-CN       Chinese (Simplified)
hl=zh-TW       Chinese (Traditional)
hl=co          Corsican
hl=hr          Croatian
hl=cs          Czech
hl=da          Danish
hl=nl          Dutch
hl=xx-elmer    Elmer Fudd
hl=en          English
hl=eo          Esperanto
hl=et          Estonian
hl=ee          Ewe
hl=fo          Faroese
hl=tl          Filipino
hl=fi          Finnish
hl=fr          French
hl=fy          Frisian
hl=gaa         Ga
hl=gl          Galician
hl=ka          Georgian
hl=de          German
hl=el          Greek
hl=gn          Guarani
hl=gu          Gujarati
hl=xx-hacker   Hacker
hl=ht          Haitian Creole
hl=ha          Hausa
hl=haw         Hawaiian
hl=iw          Hebrew
hl=hi          Hindi
hl=hu          Hungarian
hl=is          Icelandic
hl=ig          Igbo
hl=id          Indonesian
hl=ia          Interlingua
hl=ga          Irish
hl=it          Italian
hl=ja          Japanese
hl=jw          Javanese
hl=kn          Kannada
hl=kk          Kazakh
hl=rw          Kinyarwanda
hl=rn          Kirundi
hl=xx-klingon  Klingon
hl=kg          Kongo
hl=ko          Korean
hl=kri         Krio (Sierra Leone)
hl=ku          Kurdish
hl=ckb         Kurdish (Soranî)
hl=ky          Kyrgyz
hl=lo          Laothian
hl=la          Latin
hl=lv          Latvian
hl=ln          Lingala
hl=lt          Lithuanian
hl=loz         Lozi
hl=lg          Luganda
hl=ach         Luo
hl=mk          Macedonian
hl=mg          Malagasy
hl=ms          Malay
hl=ml          Malayalam
hl=mt          Maltese
hl=mi          Maori
hl=mr          Marathi
hl=mfe         Mauritian Creole
hl=mo          Moldavian
hl=mn          Mongolian
hl=sr-ME       Montenegrin
hl=ne          Nepali
hl=pcm         Nigerian Pidgin
hl=nso         Northern Sotho
hl=no          Norwegian
hl=nn          Norwegian (Nynorsk)
hl=oc          Occitan
hl=or          Oriya
hl=om          Oromo
hl=ps          Pashto
hl=fa          Persian
hl=xx-pirate   Pirate
hl=pl          Polish
hl=pt-BR       Portuguese (Brazil)
hl=pt-PT       Portuguese (Portugal)
hl=pa          Punjabi
hl=qu          Quechua
hl=ro          Romanian
hl=rm          Romansh
hl=nyn         Runyakitara
hl=ru          Russian
hl=gd          Scots Gaelic
hl=sr          Serbian
hl=sh          Serbo-Croatian
hl=st          Sesotho
hl=tn          Setswana
hl=crs         Seychellois Creole
hl=sn          Shona
hl=sd          Sindhi
hl=si          Sinhalese
hl=sk          Slovak
hl=sl          Slovenian
hl=so          Somali
hl=es          Spanish
hl=es-419      Spanish (Latin American)
hl=su          Sundanese
hl=sw          Swahili
hl=sv          Swedish
hl=tg          Tajik
hl=ta          Tamil
hl=tt          Tatar
hl=te          Telugu
hl=th          Thai
hl=ti          Tigrinya
hl=to          Tonga
hl=lua         Tshiluba
hl=tum         Tumbuka
hl=tr          Turkish
hl=tk          Turkmen
hl=tw          Twi
hl=ug          Uighur
hl=uk          Ukrainian
hl=ur          Urdu
hl=uz          Uzbek
hl=vi          Vietnamese
hl=cy          Welsh
hl=wo          Wolof
hl=xh          Xhosa
hl=yi          Yiddish
hl=yo          Yoruba
hl=zu          Zulu
```


## Search Language Codes (lr)

```
lr=lang_af    Afrikaans
lr=lang_ar    Arabic
lr=lang_hy    Armenian
lr=lang_be    Belarusian
lr=lang_bg    Bulgarian
lr=lang_ca    Catalan
lr=lang_zh-CN Chinese (Simplified)
lr=lang_zh-TW Chinese (Traditional)
lr=lang_hr    Croatian
lr=lang_cs    Czech
lr=lang_da    Danish
lr=lang_nl    Dutch
lr=lang_en    English
lr=lang_eo    Esperanto
lr=lang_et    Estonian
lr=lang_tl    Filipino
lr=lang_fi    Finnish
lr=lang_fr    French
lr=lang_de    German
lr=lang_el    Greek
lr=lang_iw    Hebrew
lr=lang_hi    Hindi
lr=lang_hu    Hungarian
lr=lang_is    Icelandic
lr=lang_id    Indonesian
lr=lang_it    Italian
lr=lang_ja    Japanese
lr=lang_ko    Korean
lr=lang_lv    Latvian
lr=lang_lt    Lithuanian
lr=lang_no    Norwegian
lr=lang_fa    Persian
lr=lang_pl    Polish
lr=lang_pt    Portuguese
lr=lang_ro    Romanian
lr=lang_ru    Russian
lr=lang_sr    Serbian
lr=lang_sk    Slovak
lr=lang_sl    Slovenian
lr=lang_es    Spanish
lr=lang_sw    Swahili
lr=lang_sv    Swedish
lr=lang_th    Thai
lr=lang_tr    Turkish
lr=lang_uk    Ukrainian
lr=lang_vi    Vietnamese
```

## Credits

This package was created and maintained by [Serply Inc](https://github.com/serply-inc).


## Report Bugs

Report bugs at https://github.com/serply-inc/serply-python/issues.

If you are reporting a bug, please include:

*   Your operating system name and version.
*   Any details about your workflow that might be helpful in troubleshooting.
*   Detailed steps to reproduce the bug.