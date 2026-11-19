# Labeling codebook

**Status:** draft — not yet frozen
**Frozen on:** _(date the test set was first labeled)_
**Corpus:** BCCh RPM minutes and press releases, 2016–2026
**Unit of analysis:** one sentence

---

## Dimension 1 — stance

### `forward`

_Definition:_ The content of the sentence has to do with future events. 

_Examples:_ Las expectativas de inflación a fines del horizonte de proyección se ubican en torno a la meta, aunque para los próximos meses se sitúan en la parte baja del rango de tolerancia.

### `backward`

_Definition:_ The content of the sentence has to do with past or current conditions. 

_Examples:_ En noviembre, la variación mensual del IPC estuvo en línea con lo previsto, con lo que la inflación anual alcanzó a 2,9%.


### `na`

_Definition:_ The content of the sentence does not contain economic or policy information.

_Examples:_ La minuta correspondiente a esta Reunión de Política Monetaria se publicará a las 8:30 horas del viernes 16 de febrero de 2018.

### Edge cases

---

## Dimension 2 — sentiment

### `hawkish`

_Definition:_ The sentence describes a decision to tighten monetary policy or conditions that suggest a tightening of monetary policy. 

_Examples:_ A pesar del retroceso reciente en algunas economías, las presiones inflacionarias a nivel mundial continúan elevadas.

### `dovish`

_Definition:_  The sentence describes a decision to loosen monetary policy or conditions that suggest a loosening of monetary policy conditions .

_Examples:_ En su Reunión de Política Monetaria, el Consejo del Banco Central de Chile acordó reducir la tasa de interés de política monetaria en 50 puntos base, hasta 0,50%.

### `neutral`

_Definition:_ The sentence describes conditions without indicating sentiment.

_Examples:_ En noviembre, la variación mensual del IPC estuvo en línea con lo previsto, con lo que la inflación anual alcanzó a 2,9%.

### `risk_highlighting`

_Definition:_  The sentence communicates the risk inherent in certain conditions without suggesting a direction for monetary policy. 

_Examples:_ En particular, varios Consejeros comentaron acerca de la incertidumbre respecto de la fecha en que se materializaría el próximo ajuste de la tasa de instancia por parte de la Reserva Federal.

### `confidence_building`

_Definition:_ The content of the sentence is related to conditions that reassusre (converegence to target, anchored inflation epectations) 

_Examples:_ Además, el escenario base suponía que más allá del movimiento de algunas medidas de expectativas de inflación de mediano plazo, estas seguían bien ancladas.

### `na`

_Definition:_ The sentence does not communicate economic or policy information. sentiment is na if and only if stance is na. 

_Examples:_ La próxima Reunión de Política Monetaria se efectuará el miércoles 13 de junio de 2018 y el comunicado respectivo será publicado a partir de las 18 horas de ese día.


### Edge cases

---

## Pilot log

Sentences the rules above could not decide, and how the rules were revised.

| # | Sentence (trimmed) | Problem | Resolution | Rule changed |
|---|---|---|---|---|
| 1 | | | | |

---

## Self-agreement check

- Sample size:
- Date of second pass:
- Cohen's kappa (stance):
- Cohen's kappa (sentiment):
