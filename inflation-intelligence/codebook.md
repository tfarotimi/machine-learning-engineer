# Labeling codebook

**Status:** frozen — updated after the pilot (2026-11-17) and after dev labeling (2026-11-19); open decisions D1–D3 settled before freezing.
**Frozen on:** 2026-11-25 (test labels finished and frozen)
**Corpus:** BCCh RPM **minutes**, 2016–2026. Comunicados are out of scope for the gold set (possible out-of-domain check later).
**Unit of analysis:** one sentence, read with the previous sentence as context
**Labels are made from:** the English translation (`sentence_en`). The Spanish original is the authority and is checked (`s` in the CLI) whenever the wording is decisive: *podría* vs *se estima*, *al alza / a la baja*, or English that reads oddly.

Every sentence gets one **stance** and one **sentiment**.
**Coupling rule:** sentiment is `na` **if and only if** stance is `na`.

---

## Dimension 1 — stance

The question: **what time does the sentence's main claim refer to?** Decide by content, not verb tense.

### `forward`

_Definition:_ The main claim concerns the future: projections, forecasts, expectations of a future value, the expected policy path, bias/guidance, future implications or risks.

_Example:_ Ello se debía a que, como señalaban las opciones de la División Estudios, se había tendido a acumular una seguidilla de noticias que, en su conjunto, habían reducido de forma material y por un tiempo prolongado las perspectivas de inflación dentro del horizonte habitual de política.
_(Past-tense grammar, but the claim is about the inflation outlook → forward.)_

### `backward`

_Definition:_ The main claim concerns past or current conditions: data already released, current state of the economy or markets, confidence surveys, the decision taken at this meeting.

_Example:_ Con esto, la evolución de los precios permanecía en línea con lo previsto en el IPoM.

### `na`

_Definition:_ No economic or policy content: logistics, publication dates, purely procedural statements about the deliberation.

_Example:_ Sobre la decisión de política monetaria, varios Consejeros coincidieron en que las opciones planteadas eran las correctas.

### Stance rules

- **S1. Mixed past and future.** Label by the main claim. When past evidence supports a conclusion about the outlook ("X has happened, so Y is expected"), the stance is `forward`. Use `backward` only when the sentence describes without concluding about what comes next.
- **S2. Decisions and options at this meeting → `backward`.** The decision taken now, votes, and the options evaluated at this meeting (including arguments for or against them).
- **S2b. Decision and guidance in one sentence → `forward`.** When a sentence states this meeting's decision *and* guidance about future moves ("keep the TPM unchanged and communicate that normalization would be more gradual"), the guidance is the new information → `forward` (S3). A decision or vote with no guidance stays `backward` (S2). _(Decided 2026-11-23, D3.)_
- **S3. Bias and guidance → `forward`.** Signals about future rate moves (*sesgo*), the expected TPM path, how the cutting/hiking cycle will continue.
- **S4. Expectations.**
  - Expectations of a **future value** (inflation, TPM, GDP over a horizon; EEE, EOF, asset prices, IMCE cost outlook, planned investment) → `forward`, even when the survey was taken in the past. Test: *is the number about a date in the future?*
  - **Confidence surveys** (IPEC, IMCE; "expectativas de consumidores/empresas") measure current sentiment → `backward`.
  - The **track record** of expectations (re-anchored, misaligned for months) used as evidence about current conditions → `backward`.
- **S5. Projections and their revisions** (IPoM scenario, "projections were revised down") → `forward`. "The news reaffirmed the baseline scenario" / "data in line with the scenario" → `backward` (an evaluation of data).
- **S6. Timeless statements of policy principle or framework** → `forward` (they describe how policy will be conducted).
- **S7. Size comparisons are not forecasts.** "Efforts that would exceed those of 2008–09" quantifies what is already done → `backward`. Future-sounding wording is forward only if it forecasts an economic variable or a policy move.
- **S8. Foreign economies, markets and pandemic/health developments are economic content.** They get a normal stance, never `na`.

---

## Dimension 2 — sentiment

The question: **as the Consejo would read it, does this sentence point the TPM up, down, or neither?** Not whether the news is good or bad.

### `hawkish`

_Definition:_ Points toward tighter policy: a tightening decision, or content arguing for it (inflation pressure rising or persistent, gaps closing, strong demand, expectations above target, arguments against easing).

_Example:_ Todos los Consejeros concordaron en que la opción de aumentar el estímulo monetario había dejado de ser relevante, pues los riesgos a la baja para la convergencia de la inflación —que había sido un tópico de preocupación en los últimos trimestres— habían perdido fuerza.

### `dovish`

_Definition:_ Points toward looser policy: a loosening decision, or content arguing for it (weak activity, widening slack, inflation or its outlook falling below target, downward bias, arguments against tightening).

_Examples:_
- Más aún, la nueva información disponible confirmaba el carácter transitorio del repunte de la inversión observado en el tercer trimestre del año pasado y revelaba una reversión del crecimiento que venían experimentando ciertos sectores, lo que dejaba escasos factores de dinamismo económico al inicio del 2016.
- A juicio de uno de estos Consejeros, era necesario añadir un mensaje inequívoco de sesgo a la baja en la TPM.

### `neutral`

_Definition:_ Has economic or policy content but no direction: bare data reports, "in line with forecast", framing questions, strategy statements, conditionals that state a test.

_Example:_ Con esto, la evolución de los precios permanecía en línea con lo previsto en el IPoM.

### `risk_highlighting`

_Definition:_ Draws attention to risk or uncertainty — what **could** happen — without stating a direction for policy.

_Example:_ En particular, varios Consejeros comentaron acerca de la incertidumbre respecto de la fecha en que se materializaría el próximo ajuste de la tasa de instancia por parte de la Reserva Federal.

### `confidence_building`

_Definition:_ Reassurance that **conditions** are on track: inflation converging to target, expectations anchored, market expectations aligning with the Bank's projections, past policy having worked. Not statements of strategy (those are neutral).

_Example:_ Además, el escenario base suponía que más allá del movimiento de algunas medidas de expectativas de inflación de mediano plazo, estas seguían bien ancladas.

### `na`

_Definition:_ No economic or policy content. Used if and only if stance is `na`.

_Example:_ Sobre la decisión de política monetaria, varios Consejeros coincidieron en que las opciones planteadas eran las correctas.

### Sentiment rules

**Direction**
- **T1. Good/bad news ≠ the label.** Good news about growth, demand, employment or the external scenario → hawkish. Good news about inflation falling toward target → confidence_building or dovish. Ask: *good news about what?*
- **T2. Decisions.** Hike → hawkish, cut → dovish, hold → neutral, unless the sentence adds directional reasoning ("hold while evaluating further cuts" → dovish).
- **T3. Direction beats risk.** If a sentence states a direction, label the direction. Will/could test: *will / is / estimates that* → hawkish/dovish; *could / risks / uncertainty* → risk_highlighting.
- **T4. A risk that is materializing** (*materializándose*) is happening → label its direction.
- **T5. Changes in the balance of risks are directional.** Downside → balanced, or balanced → upside = hawkish. Upside → balanced, or balanced → downside = dovish. A static "risks are balanced" → neutral or confidence_building.
- **T5b. Revisions to guidance:** label the direction of the change. Slower hikes or faster cuts than previously signaled (or than the market prices) → dovish. Faster hikes or slower cuts → hawkish.
- **T5c. Decision vs revision in opposite directions** (cut, but at a slower pace): the decision sets the label.
- **T6. Convergence is direction-free until you know the side.** "Convergence compromised" from above (inflation too high) → hawkish; from below → dovish. Check whether inflation/its outlook is above or below 3%.

**Arguments**
- **T7. Options: label the argument, not the option.** A sentence laying out the case for an option takes that case's direction. A sentence naming an option's cost or drawback argues against it ("holding goes against the market, which expects a cut" → dovish).
- **T7b. An option only reported as ruled out → label by what is left standing.** When a sentence's whole content is that one or more options were discarded, label it as a statement about the decision (T2) judged by the option(s) still on the table: only a cut left → dovish, only a hold left → neutral, only a hike left → hawkish. _(Decided 2026-11-25, D2.)_
- **T8. Discounting flips the direction.** Calling a data point transitory, one-off, unsustainable or limited in effect argues against what it signals. Discounting hawkish data → dovish; discounting dovish data → hawkish. Applies only when the sentence *contradicts* the data; "not yet clear" or "hard to read" is neutral.
- **T9. "Not yet" is neutral.** Conditionals that state when a move would be justified, without asserting the condition holds, and "will become clearer soon" sentences → neutral. A conditional that states a **consequence/cost** of an option is an argument (T7).
- **T10. Framing sentences are neutral.** "There were two questions…", "the following elements had to be considered" → neutral; the content comes in the next sentences.

**Scope**
- **T11. Foreign economies and central banks.** Reported facts → neutral. Label a direction only when the sentence states an implication for Chile (financial conditions, capital flows, the peso, copper, external demand). The external scenario improving/worsening for emerging economies counts as an implication for Chile. Uncertainty explicitly highlighted by the Consejo → risk_highlighting. Broad external scenario for EMs/Chile → direction; a specific indicator in a specific foreign economy or region ("la región" = the rest of Latin America, discussed in the external section) → neutral.
- **T12. Inflation components.** The signal is in non-tradables and core; tradables, exchange-rate effects and one-off factors are looked through.
- **T12b. Supply vs demand.** Activity driven by supply factors (mining output, export sectors, weather, one-off production) is looked through; label by what the sentence says about demand.
- **T13. Data sentences.** A bare number → neutral. A number characterized ("weakening", "fall", "strong", "above expected") → label the direction described.
- **T14. Strategy vs conditions.** How policy is conducted (communication, medium-term orientation, flexibility) → neutral. Reassurance about conditions → confidence_building. Assessments that past policy worked → confidence_building, unless used to argue for a direction.
- **T15. Measurement caveats** (new methodology, short history, revisions) → neutral.
- **T16. Pandemic/health** developments are economic: worsening → weaker activity → dovish; faster reopening → hawkish lean.
- **T17. Individual and minority views** are labeled by what they say. Attribution ("un Consejero") doesn't change the label.
- **T17b. Inflation expectations at/around 3% (anchored, re-anchored)** → confidence_building, unless another clause carries the point (a significant rise in short-term expectations, "only recently" re-anchored in a cautionary argument, measures below 3%).
- **T18. "En línea con lo previsto" / "news reaffirmed the scenario"** with no further comment → neutral.
- **T19. Mixed risk and reassurance** in one sentence → label the clause that carries the point (usually after *sin embargo / pero / no obstante*, or the one answering the previous sentence).

---

## Context rules

- **C1.** The previous sentence resolves **what this sentence refers to** (*esto, ello, hacerlo, con esto*, "the latter"). The label comes from **this sentence's own claim**. Never copy the previous sentence's sentiment.
- **C2.** A sentence that opens a new topic ("En el plano externo…") gets no help from the previous one.
- **C3.** Some sentences need knowledge the text does not contain (e.g. where the TPM stood relative to neutral, which direction a past "deviation" went). Look it up as needed and label with full knowledge. **Decided (2026-11-18):** no `context_dependent` flag.

---

## Glossary

- **Sorpresa al alza / upside surprise:** the number came in **higher** than forecast. *Negativa / a la baja / downside:* **lower** than forecast. For inflation: upside → hawkish lean, downside → dovish lean.
- **Riesgo a la baja (downside risk) for inflation:** risk of **undershooting** the target. Undershooting is a failure too: it signals weak demand, can de-anchor expectations downward and raises real rates.
- **Brecha de actividad (activity gap):** in BCCh usage, slack. *Se amplía* = more slack = dovish. *Se cierra* = less slack = hawkish.
- **Sesgo (bias):** forward guidance on direction. *A la baja* → dovish; *al alza* → hawkish; removing a downward bias → hawkish shift.
- **Neutralidad / retorno a la neutralidad:** moving the TPM toward the neutral rate. Below neutral (2016–19, 2020–21) → hikes; above neutral (2023–25) → cuts. Check the cycle.
- **Real rates:** real ≈ nominal − expected inflation. Falling inflation expectations with an unchanged TPM raise real rates and tighten policy passively.
- **Exchange rate:** peso appreciation → cheaper imports, weaker exports → dovish. Depreciation → imported inflation → hawkish.
- **Market rates vs the TPM:** the Bank raising the TPM is hawkish. Market lending rates rising on their own tighten financial conditions → dovish.
- **Financial asset prices and conditions** (equity prices, credit spreads, the sovereign risk premium): looser conditions → more demand → **hawkish**; tighter → **dovish**. Stocks rising, spreads or the sovereign premium narrowing = looser; the reverse = tighter. A bare report of the move with no characterization → neutral (T13). If the sentence's point is volatility or uncertainty → risk_highlighting. When effects in opposite directions are named (e.g. spreads widen *and* the peso depreciates), label the one that carries the point (T19). For foreign markets, T11 still applies. _(Decided 2026-11-23, D1.)_
- **confidence_building vs good news:** reassurance about inflation, expectations or stability → confidence_building. Good news about growth, recovery or the pandemic → hawkish (T1).
- **Higher rates → less spending → lower inflation. Lower rates → more spending → higher inflation.**

---

## Labeling procedure

- **Test** is labeled **blind**, with this codebook frozen, before any model is run on any split. Record the commit of the frozen codebook in `data/gold/README.md`.
- **Dev** was labeled blind (decided 2026-11-18; originally it could be pre-labeled and verified). Every method is tuned on dev, so model-influenced dev labels would pull all methods toward the model's reading of this codebook.
- **Train** was hand-labeled and then reviewed with Claude (see pilot log).
- During blind labeling, questions about **rules in general** are fine; asking a model about a **specific sentence** is not. Hard cases are noted (`doc_id`, `sent_idx`) and discussed as rules afterwards.
- Sessions of **≤ 50 sentences**, with breaks. After each session, look at the label distribution: a long streak of one label is a fatigue warning (the pilot had 31 consecutive `backward` labels, 12 of them wrong).
- The CLI shows English; type `s` to see the Spanish.

---

## Known limitations

- No intensity scale: "we are hiking now" and "easing is off the table" are both `hawkish`.
- Labels are made from a machine translation; nuance can be lost (mitigated by `s`).
- Single annotator; reliability measured by self-agreement only.
- Train labels were reviewed with Claude, so they partly reflect annotator+Claude conventions; dev and test reflect the annotator alone.
- Rare classes are thin: dev has 7 `confidence_building`, 5 `risk_highlighting` and 0 `na`. Per-class dev scores for these are noisy, and dev says nothing about `na`.

---

## Pilot log

Pilot: 400 train stances and 50 train sentiments, 2026-11-16/17. Stance review changed 63 of 400 (~16%); the error rate rose in long sessions. Most frequent stance errors: options at this meeting labeled forward (S2); expectations/projections labeled backward (S4, S5); foreign/pandemic content labeled `na` (S8).

| # | Sentence (trimmed) | Problem | Resolution | Rule |
|---|---|---|---|---|
| 1 | La inflación anual del IPC se ubicó en 4,2%… | Is inflation data policy content? | content → backward + neutral | `na` definition |
| 2 | …habían reducido de forma material… las perspectivas de inflación… | past grammar, outlook content | forward + dovish | S1 |
| 3 | …la única opción en esta Reunión era mantener la TPM | stance of decisions | backward + neutral | S2, T2 |
| 4 | …añadir un mensaje inequívoco de sesgo a la baja… | is "bias" an error? | forward + dovish | S3, glossary |
| 5 | las expectativas de consumidores y empresas seguían en niveles pesimistas | "expectations" = confidence | backward + dovish | S4 |
| 6 | expectativas de crecimiento de la EEE… cambios menores | survey taken in the past | forward + neutral | S4 |
| 7 | La decisión fue adoptada por la unanimidad… / las opciones planteadas eran las correctas | procedural? | na | `na` definition |
| 8 | …dar el mensaje en el IPoM de septiembre… estrategia anclada en una visión de mediano plazo | strategy vs reassurance | neutral | T14 |
| 9 | …el escenario externo del IPoM ya estaba por debajo de lo que proyectaba el mercado | "below" read as negative | hawkish lean | T1, comparisons |
| 10 | …mantener el sesgo y la tasa… iba en contra del consenso de mercado… | option vs argument | dovish | T7 |
| 11 | la velocidad de expansión del cuarto trimestre… no podía sostenerse | discounting | dovish | T8 |
| 12 | Solo lo sería si iba asociado a menor crecimiento… | conditional | neutral | T9 |
| 13 | Ello sería válido si… retorno a la neutralidad más rápido… / ello no era así | needs outside knowledge | dovish (full knowledge) | C3, glossary |
| 14 | …había sorprendido al alza en enero… / …en línea con lo previsto | surprise direction confused | neutral | glossary, T18 |
| 15 | La brecha de actividad se ampliaría… | "gap" read as excess demand | dovish | glossary |
| 16 | El Banco de Japón… el Riksbank… el Banco de Canadá… | foreign central banks | neutral | T11 |
| 17 | Quizás la única diferencia era que el escenario de corto plazo… lucía balanceado y no a la baja | balance of risks changed | hawkish | T5 |
| 18 | El aumento del segmento comercial estaba influido por una operación puntual | discounting | dovish | T8 |
| 19 | …la medición de la actividad de construcción… nuevas fuentes… | measurement caveat | neutral | T15 |
| 20 | …el objetivo de la política monetaria era la inflación y su instrumento la TPM | timeless principle | forward + neutral | S6, T14 |

---

## Dev log

Dev: 150 sentences, labeled blind 2026-11-19 in three sessions of 50 (sample is ordered by period: 2016–19, then 2020–21, then 2022–23). No review of individual labels. Fatigue check after each session: longest runs were 10 `backward` (stance) and 6 `hawkish` (sentiment), against 31 in the pilot.

| Stance | n | Sentiment | n |
|---|---|---|---|
| backward | 89 | hawkish | 51 |
| forward | 61 | neutral | 44 |
| na | 0 | dovish | 43 |
| | | confidence_building | 7 |
| | | risk_highlighting | 5 |

Batch-level sentiment swung with the period (dovish-heavy in 2016–19, hawkish-heavy in 2021), consistent with the policy cycle rather than drift.

Corrections, both at the annotator's own request: `minutes_2017_07_13`/89 stance forward → backward (S2); `minutes_2022_07_13`/66 sentiment neutral → dovish. Hard cases raised: D1–D3 above.

---

## Self-agreement check

_Re-label a sample of the test set after all other labeling is complete, without looking at the first pass, and record Cohen's kappa here. This is the ceiling on what any model can achieve against these labels, and it belongs in the results._

Procedure:
- Wait **at least one week** after finishing test, so the second pass isn't recall of the first.
- Do it **before seeing any model output**, so the second pass is not influenced by a model.
- Draw the sample with a fixed seed; label it with the CLI into a separate file; never edit `test_labels.jsonl` from it.
- Use ~60 sentences. With 30, the confidence interval on kappa is too wide to say much.
- Compute kappa with the project's own evaluation code; report stance and sentiment separately, plus the confusion matrix of first vs. second pass.

- Sample size:
- Date of second pass:
- Cohen's kappa (stance):
- Cohen's kappa (sentiment):
