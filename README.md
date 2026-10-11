# Slovenia — legislation as Markdown (LawCodex)

The Constitution and the legislation in force of the **Republic of Slovenia** (*Republika
Slovenija*), in Slovenian, converted to Markdown — one file per act.

Source: **PIS — Pravno-informacijski sistem Republike Slovenije** (Legal Information System of
the Republic of Slovenia, https://pisrs.si), operated by the Government Office for Legislation
(*Služba Vlade RS za zakonodajo*) and the Ministry of Justice. The texts come from the PIS
collection **Register predpisov** (register of regulations in force).

Retrieved: **2026-10-12**.

## Coverage

All *basic* acts (not amending acts / *novele*) of the kinds below that PIS lists in the
*Register predpisov*, i.e. acts that are in force (or no longer in force but still applied):

| Directory | Contents | Files |
|---|---|---:|
| `ustava/` | Ustava Republike Slovenije (URS) and the constitutional acts (*ustavni zakoni*), the Basic Constitutional Charter (*Temeljna ustavna listina*) and the 1991 constitutional amendment (*Ustavni amandma*) | 16 |
| `zakoni/<year>/` | acts of the National Assembly (*zakoni*), incl. codes (Obligacijski zakonik, Kazenski zakonik, Družinski zakonik, Stvarnopravni zakonik …) and 1,270 acts ratifying international treaties (*zakoni o ratifikaciji*) | 2,058 |
| `uredbe/<year>/` | government decrees (*uredbe* of the Vlada RS), incl. decrees ratifying international agreements | 2,365 |
| `pravilniki/<year>/` | rules issued by ministers (*pravilniki*) | 2,706 |
| **Total** | | **7,145** |
| `slike/` | images embedded in the texts (formulas, signs, forms), extracted from the source as PNG/JPG and linked from the Markdown | 313 |

`<year>` is the year of publication of the original act in the *Uradni list Republike
Slovenije* (Official Gazette; older acts: Uradni list SRS / SFRJ).

### Which text

For every act the **most recent text version already applicable today** is used:

- **NPB** (*neuradno prečiščeno besedilo*, unofficial consolidated text) where PIS has one —
  1,861 files. Front matter `text_version: "NPB n (…)"`. These texts start with the PIS
  disclaimer and the list of acts consolidated into the NPB, as published by PIS.
  `last_amended` is the latest publication date in that list.
- otherwise the **original text** (*Osnovni*, `text_version: "Osnovni (izvirno besedilo)"`) —
  5,284 files, mostly acts that were never amended (e.g. most ratification acts and many
  regulations). For an amended act with no NPB in PIS, the original text is not the current text;
  check `citation`, which lists all amendments.

NPBs are unofficial working aids; the legally binding text is the one published in the
*Uradni list RS* (see `citation` and `sop`). Note that PIS omits the preamble of the
Constitution in its NPB; it is therefore absent here too.

### Front matter

```yaml
title: "Obligacijski zakonik (OZ)"
identifier: "ZAKO1263"          # PIS identifier (ZAKO…, URED…, PRAV…, USTA…/USTZ…)
abbreviation: "OZ"              # kratica
type: code                      # constitution | constitutional_act | constitutional_amendment | code | act | ratification_act | decree | regulation
jurisdiction: si
language: sl
act_kind: "Zakon"               # vrsta akta as given by PIS
date: 2001-10-03                # adoption (sprejeto), else publication
published: 2001-10-25           # publication in the Official Gazette
in_force_from: 2002-01-01
last_amended: 2016-10-14        # NPB only: latest gazette date among consolidated acts
status: in_force                # in_force | repealed (not in force, still applied) | unknown
pis_status: "Veljaven predpis"  # PIS validity category (semafor)
text_version: "NPB 4 (neuradno prečiščeno besedilo)"
citation: "Uradni list RS, št. 97/07 – uradno prečiščeno besedilo, 64/16 – odl. US in 20/18 – OROZ631"
adopted_by: "Državni zbor Republike Slovenije"
eva: "…"; epa: "…"; sop: "2001-01-4287"   # government / parliament / gazette numbers, when present
source: "https://pisrs.si/pregledPredpisa?id=ZAKO1263"
retrieved: 2026-10-12
---
```

### Text structure

PIS delivers each text as a sequence of typed paragraphs. Divisions (*del*, *poglavje*,
*oddelek*, *pododdelek*, *odsek*) become headings (`##`, `###`, … — only the levels actually
used by the act are allocated), and every article (*N. člen*) is a heading one level below the
deepest division (bold if that would exceed `######`). Article titles (e.g. *(vsebina)*) follow
the article heading in bold. Indents (*alineje*) become `- ` list items; numbered and lettered
points are kept as written. Tables become Markdown tables when they have no merged cells,
otherwise cleaned HTML. Annexes and forms that PIS publishes as separate files (PDF, DOCX …)
are linked to `https://pisrs.si/api/datoteke/integracije/<id>` (≈1,960 files contain such links).
In older NPBs, the closing part after a horizontal rule (`---`) reproduces the transitional
and final provisions of the amending acts; there, divisions and article labels are rendered in
bold rather than as headings so that they do not disturb the act's outline.

## Not covered

- Amending acts (*novele*) as separate files — their changes are in the consolidated texts.
- Repealed acts and historical versions (PIS collections *Neveljavni predpisi* and
  *Obsoletni predpisi*).
- Other kinds of national acts in the Register: *odloki* (≈430), *odredbe* (≈710),
  *navodila* (≈80), other acts of state bodies, acts of public-law entities, collective
  agreements.
- Local (municipal) legislation, EU law, international treaties outside the ratification acts,
  case law and other PIS collections.
- 61 acts listed in the Register for which PIS has no text (only a reference to the gazette
  PDF or nothing):

| Category | PIS ID | Title | Note |
|---|---|---|---|
| ustava | USTZ43 | Ustavni zakon o spremembi 148. člena Ustave Republike Slovenije (UZ148) | no text in PIS (source: https://www.uradni-list.si/_pdf/2013/Ur/u2013047.pdf) |
| zakoni | ODLU215 | Zakon o ustanovitvi Društvenega sveta za upravno področje izvrševanja kazenskih sankcij | no text in PIS |
| zakoni | ZAKO6728 | Zakon o ratifikaciji Sprememb Sporazuma o ohranjanju kitov in delfinov Črnega morja, Sredozemskega morja in atlantskega območja ob njem (MSOKD-A) | no text in PIS (source: https://www.uradni-list.si/_pdf/2016/Mp/m2016023.pdf) |
| zakoni | ZAKO8488 | Zakon o ratifikaciji Sporazuma med Republiko Slovenijo in Mednarodnim kazenskim sodiščem o izvrševanju kazni Mednarodnega kazenskega sodišča (MSMKSIK) | no text in PIS (source: https://www.uradni-list.si/_pdf/2022/Mp/m2022018.pdf) |
| uredbe | URED1269 | Temeljna uredba o gradnji | no text in PIS |
| uredbe | URED50 | Uredba o klasifikaciji voda medrepubliških vodnih tokov, meddržavnih voda in voda obalnega morja Jugoslavije | no text in PIS |
| uredbe | URED1291 | Uredba o ugotavljanju onesnaženosti kmetijskih zemljišč in gozda | no text in PIS |
| uredbe | URED2543 | Uredba o ratifikaciji zapisnika o razgovorih med predstavniki Republike Slovenije in republike Avstrije o nadaljnih odnosih med obema državama na področju socialne varnosti | no text in PIS (source: https://www.uradni-list.si/_pdf/1992/Mp/m1992019.pdf) |
| uredbe | URED2098 | Uredba o ratifikaciji Sporazuma med Vlado Republike Slovenije in Vlado Republike Hrvaške o ustanovitvi in pristojnostih skupnih organov za ugotovitev ter označitev državne meje | no text in PIS (source: https://www.uradni-list.si/_pdf/1993/Mp/m1993055.pdf) |
| uredbe | URED6955 | Uredba o ratifikaciji sprememb Ustave, Konvencije in Splošnih pravil Mednarodne telekomunikacijske zveze (ITU), sprejetih na konferenci pooblaščenih predstavnikov držav članic v Guadajalari | no text in PIS (source: https://www.uradni-list.si/_pdf/2015/Mp/m2015099.pdf) |
| uredbe | URED7824 | Uredba o ratifikaciji Sporazuma med Uradom Republike Slovenije za preprečevanje pranja denarja (Republika Slovenija) in Zvezno službo za finančni nadzor (Ruska federacija) o sodelovanju na področju preprečevanja legalizacije (pranja) premoženjske koristi, pridobljene s kaznivimi dejanji, in financiranja terorizma | no text in PIS (source: https://www.uradni-list.si/_pdf/2019/Mp/m2019009.pdf) |
| pravilniki | PRAV2785 | Pravilnik o protestnih registrih | no text in PIS |
| pravilniki | PRAV988 | Pravilnik o določanju nadvodja za ladje trgovske mornarice, ki ne opravljajo mednarodnih potovanj | no text in PIS |
| pravilniki | PRAV3072 | Pravilnik o skladiščenju in hrambi karbida in o manipulaciji s kalcijevim karbidom | no text in PIS |
| pravilniki | PRAV334 | Pravilnik o varstvu pri nakladanju in razkladanju tovornih motornih vozil | no text in PIS |
| pravilniki | PRAV2832 | Pravilnik o varstvu gozdov in gozdnih zemljišč pred požarom | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-KUFOYL4S/375ecb23-5d68-460d-873e-69a70914120f/PDF) |
| pravilniki | PRAV12137 | Pravilnik o normativih za graditev in opremo osnovnih šol | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-WWCC74WN/c783bb33-6bf9-49cb-8057-88fc38fd9b64/PDF) |
| pravilniki | PRAV11780 | Pravilnik o zdravstveno-higienskih zahtevah, katerim morajo ustrezati poslopja in prostori osnovne šole | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-6P3BWOO3/c82fcb45-2c66-464f-aead-468fe3873ea5/PDF) |
| pravilniki | PRAV201 | Pravilnik o splošnih ukrepih in normativih za varstvo pri delu z dvigali | no text in PIS |
| pravilniki | PRAV2949 | Pravilnik o tehničnih ukrepih in pogojih za projektiranje in izvajanje betonskih in armiranobetonskih konstrukcij v okolicah, ki so izpostavljene agresivnemu delovanju vode in tal | no text in PIS |
| pravilniki | PRAV981 | Pravilnik o določanju tovornih črt morskim ladjam | no text in PIS |
| pravilniki | PRAV3204 | Pravilnik o gradnji naprav za vnetljive tekočine ter o uskladiščenju in pretakanju vnetljivih tekočin | no text in PIS |
| pravilniki | PRAV2950 | Pravilnik o tehničnih ukrepih in pogojih za prednapeti beton | no text in PIS |
| pravilniki | PRAV3559 | Pravilnik o strokovnih in tehničnih pogojih glede opreme in kadrov v zavodih v naravnih zdraviliščih | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-PRIGG9XT/f8e407de-873e-49af-b591-b09016e7c6a9/PDF) |
| pravilniki | PRAV3420 | Pravilnik o tehničnih normativih za elektroenergetske postroje nazivne napetosti nad 1000 V | no text in PIS |
| pravilniki | PRAV2367 | Pravilnik o preizkušanju in žigosanju oziroma zaznamovanju ročnega strelnega orožja, streliva, aparatov in naprav | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-ZL7C264K/536fda37-3b30-4bd5-92c1-78ee68eddf6c/PDF) |
| pravilniki | PRAV2796 | Pravilnik o strokovni izobrazbi in usposabljanju tehničnih vodij, vodij tehničnih služb in nadzorno-tehničnega osebja pri raziskovanju ali izkoriščanju rudnin ter o strokovnih izpitih in ustrezni praksi samostojnih projektantov rudarskih projektov | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-PZLKNANW/bc3f4e0e-f85e-4eed-8441-3b32b058f61e/PDF) |
| pravilniki | PRAV3832 | Pravilnik o načinu pošiljanja poročil in podatkov o pojavih rastlinskih bolezni in škodljivcev ter o ukrepih za preprečevanje njihovega širjenja in njihovo zatiranje | no text in PIS |
| pravilniki | PRAV40 | Pravilnik o vpisu ladij v določene vpisnike, o podatkih, ki se vpisujejo v list A glavne knjige vpisnika ladij, o zbirkah listin, o pomožnih knjigah, ki se vodijo poleg vpisnikov ladij, in o obrazcih teh listin in knjig | no text in PIS |
| pravilniki | PRAV2975 | Pravilnik o programu in načinu opravljanja izpitov na tečajih za osnovno znanje o živalskih kužnih boleznih in o predpisih | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-QKHO6IXZ/ca88f5ad-e998-4784-aa39-2866ab7bf343/PDF) |
| pravilniki | PRAV3520 | Pravilnik o minimalnih tehničnih, strokovnih in kadrovskih pogojih za delo zavodov za usposabljanje in validnih oseb | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-4GRHMHRP/133f5d6f-585d-4958-98a0-980866dc4cb8/PDF) |
| pravilniki | PRAV949 | Pravilnik o letenju letal | no text in PIS |
| pravilniki | PRAV49 | Pravilnik o varstvu pri delu v gozdarstvu | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-GUWWZTU4/21ae0eaf-5105-4789-87d3-25a76dbfc718/PDF) |
| pravilniki | PRAV3208 | Pravilnik o pogojih in postopku za izdajo dovoljenja za uvoz in izvoz mamil | no text in PIS |
| pravilniki | PRAV3206 | Pravilnik o vsebini in načinu vodenja evidenc in poročil, ter o rokih za pošiljanje podatkov o proizvodnji in prometu mamil | no text in PIS |
| pravilniki | PRAV3265 | Pravilnik o vsebini, obrazcih in načinu vodenja ladijskih listin in knjig ladij trgovske mornarice SFRJ | no text in PIS |
| pravilniki | PRAV935 | Pravilnik o načinu oddaje in vrnitve orožja in streliva v javnem prevozu v zračnem prometu | no text in PIS |
| pravilniki | PRAV980 | Pravilnik o zapisniku, ki ga sestavi poveljnik ladje o rojstvu ali smrti, in o sprejetju izjave poslednje volje na ladji trgovske mornarice | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-OQTRZUSM/3e586a7e-b7c2-453f-b293-2dec2864eb84/PDF) |
| pravilniki | PRAV3381 | Pravilnik o preverjanju in o ocenjevanju znanja v srednjem izobraževanju | no text in PIS (source: https://www.dlib.si/stream/URN:NBN:SI:doc-C58RNRFM/840b35df-c181-4e70-a6c2-524846510d4e/PDF) |
| pravilniki | PRAV3263 | Pravilnik o označbah na plovnih poteh v obalnem morju SFRJ | no text in PIS |
| pravilniki | PRAV3259 | Pravilnik o notranjih plovnih poteh | no text in PIS |
| pravilniki | PRAV3258 | Pravilnik o najmanjšem številu članov posadke, ki jih morajo imeti za varno plovbo ladje notranje plovbe trgovske mornarice | no text in PIS |
| pravilniki | PRAV3254 | Pravilnik o določanju imen, označb in razpoznavnih znamenj ladij in evidence o imenih ladij | no text in PIS |
| pravilniki | PRAV309 | Pravilnik o pogojih glede zdravstvene neoporečnosti predmetov splošne rabe, ki smejo v promet | no text in PIS |
| pravilniki | PRAV2786 | Pravilnik o racionalni rabi energije pri gretju in prezračevanju objektov ter pripravi tople vode | no text in PIS |
| pravilniki | PRAV3304 | Pravilnik o žičnicah in vlečnicah | no text in PIS |
| pravilniki | PRAV2985 | Pravilnik o ukrepih za zaščito živali pred mučenjem pri izvajanju zdravstvenega varstva živali | no text in PIS |
| pravilniki | PRAV3486 | Pravilnik o obliki in namestitvi oznak nepremičnih spomenikov in znamenitosti | no text in PIS |
| pravilniki | PRAV2996 | Pravilnik o gozdnobiološki reprodukciji | no text in PIS |
| pravilniki | PRAV346 | Pravilnik o ukrepih za preprečevanje škodljivih posledic zaradi ostankov zdravil v surovinah in proizvodih živalskega izvora | no text in PIS |
| pravilniki | PRAV3519 | Pravilnik o minimalnih tehničnih, strokovnih in kadrovskih pogojih za delo zavodov za usposabljanje invalidnih oseb pod posebnimi pogoji | no text in PIS |
| pravilniki | PRAV3160 | Pravilnik o uporabi kmetijskih zemljišč za gozdne plantaže | no text in PIS |
| pravilniki | PRAV3607 | Pravilnik za izvajanje zakona o preživninskem varstvu kmetov | no text in PIS |
| pravilniki | PRAV2523 | Pravilnik o notranjem poslovanju organov za postopek o prekrških | no text in PIS |
| pravilniki | PRAV274 | Pravilnik o ukrepih za zatiranje in izkoreninjanje atipične kokošje kuge | no text in PIS |
| pravilniki | PRAV3210 | Pravilnik o pogojih za lokacijo, graditev, poskusno obratovanje, zagon in uporabo jedrskih objektov | no text in PIS |
| pravilniki | PRAV3209 | Pravilnik o izdelavi in vsebini varnostnega poročila in druge dokumentacije, potrebe za ugotavljanje varnosti jedrskih objektov | no text in PIS |
| pravilniki | PRAV2510 | Pravilnik o postopku za popis in ocenitev premoženja oseb pod skrbništvom ter o pripravi skrbniških poročil | no text in PIS |
| pravilniki | PRAV3158 | Pravilnik o normativih, analitskih postopkih in metodah ugotavljanja onesnsženosti tal in vegetacije ter pogojih za uporabo nekaterih snovi v kmetijstvu in gozdarstvu | no text in PIS |
| pravilniki | PRAV917 | Pravilnik o pogojih, ki jih morajo izpolnjevati skladišča in drugi prostori za skladiščenje rastlin, in podjetja, ki se ukvarjajo z dezinfekcijo in dezinsekcijo rastlin ter z deratizacijo prostorov | no text in PIS |
| pravilniki | PRAV3174 | Pravilnik o vodenju zemljiške knjige | no text in PIS (source: https://www.uradni-list.si/_pdf/1995/Ur/u1995077.pdf) |

## Sources and licence

- PIS — https://pisrs.si (public JSON API used by the website:
  `POST /api/filter/filter` for listings, `GET /api/rezultat/zbirka/id/<ID>` for metadata and
  versions, `GET /api/rezultat/neuradno-precisceno-besedilo/<versionId>` for the text).
- Official gazette: Uradni list Republike Slovenije, https://www.uradni-list.si.

Under Article 9 of the Slovenian Copyright and Related Rights Act (*Zakon o avtorski in sorodnih
pravicah*, ZASP), laws, regulations and other official texts of legislative, administrative and
judicial bodies are not protected by copyright. PIS content is freely accessible public sector
information. The NPBs are unofficial; this repository is not an official publication.

## Regenerate

```sh
pip install -r scripts/requirements.txt
python scripts/si_fetch.py   --raw ../_raw/si     # list + download (cached; re-runs fetch only what is missing)
python scripts/si_convert.py --raw ../_raw/si --out .
```

`si_fetch.py` uses a descriptive User-Agent, 3 parallel workers with a pause after each request
and exponential back-off. pisrs.si's robots.txt has no Crawl-delay and only disallows
`/iskanje` (the search UI). The listing API refuses to page past 1,000 hits, so large
categories are listed year by year (publication date). To refresh, delete `_raw/si/list/`
(and `meta/` to pick up new NPB versions) before re-running.
