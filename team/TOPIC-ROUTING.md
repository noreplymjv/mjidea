# Topic → Expert Squad Routing

When `pipeline/execute.sh` (or an agent on “execute”) opens an idea, match **keywords** in the title/body to a topic pack. Always include **PM + War Room Director + Genius Panel (≥5)** plus the listed field squads (≥5 each unless noted).

Default if no match: **philosophy** pack.

---

## Always on every job

| Role | IDs |
|------|-----|
| PM / CoS | EX-02 Mira Vance, EX-04 Jules Haber |
| War Room Director | EX-03 Kai Ortega |
| Genius Panel (min 5) | GP-01 Rowan Quill, GP-02 Selene Park, GP-03 Theo Marsh, GP-04 Iris Cole, GP-05 Jonah Reed |
| Research citations | Follow `team/war-rooms/09-research-citations.md` — Drew Fontaine (CN-06) + topic fact-checker |
| Content core | CN-01 Elena Voss, CN-02 Marcus Hale, CN-03 Priya Nair, CN-04 Sam Ortiz, CN-05 Leah Kim |
| SEO core | SE-01…SE-05 |
| Growth core | GR-01…GR-05 |
| Security (3+) | SC-01, SC-02, SC-03 |
| Audit (3+) | AU-01, AU-03, AU-05 |

---

## Topic packs (keyword → emphasis)

### philosophy | belief | meaning | essay | truth | moral

**Keywords:** philosophy, meaning, moral, belief, essay, loneliness, attention, truth, human, wisdom  
**Emphasize:** Content (full), Genius GP-05 + GP-02, Audit AU-03 voice  
**Extra:** GP-07 Nix (contrarian), CN-02 Marcus  
**Angle:** Lived claim → flip → residual question. Citations for any sociological/psych claim.

### trust | certify | badge | stamp | verified | provenance | honesty

**Keywords:** trust, certified, certificate, badge, stamp, verified, provenance, honesty, label, organic  
**Emphasize:** Security SC-03 Paige (privacy theater vs real trust), Content CN-06 Drew, Genius GP-01 + GP-04  
**Extra:** GP-06 Ava (craft), GR-02 Eli (shareability without seal-worship)  
**Angle:** Paper ≠ relationship; verification still matters — stamps don’t replace chain.

### privacy | local-first | cookies | consent | data | surveillance

**Keywords:** privacy, local-first, local first, cookie, consent, data, surveillance, track  
**Emphasize:** Security full SC-01…SC-05, Engineering EN-01 + EN-03, Genius GP-04  
**Extra:** Paige SC-03 lead lens  
**Angle:** Respect as product feature; cite regs/standards carefully with dates.

### marketing | rory | perception | behavioral | signalling | placebo | psychology of

**Keywords:** marketing, rory, perception, behavioral, behaviour, signalling, placebo, satnav, stopwatch, irrational  
**Emphasize:** Genius GP-01 Rowan (lead), GP-03 Theo, GP-06 Ava; Growth full; Content Priya  
**Extra:** SEO SE-03 Gia (SERP psychology)  
**Angle:** Perception as product; cite studies/books with URLs — no fake Rory quotes.

### product | ux | design | interface | craft | shipping

**Keywords:** product, ux, design, interface, craft, shipping, feature, roadmap  
**Emphasize:** Design DS-01…DS-05, Engineering EN-01…EN-03, Genius GP-03  
**Extra:** Don-Norman-mode via DS + CN-04 clarity  
**Angle:** Human-centered; cite Nielsen/NN/g or primary product research when claiming UX facts.

### ai | verify | agent | model | hallucination | seed | self-check

**Keywords:** ai, agent, verify, verification, hallucination, llm, model, seed, self-check, parallel minds  
**Emphasize:** Security SC-02 Omar, Content CN-06 Drew, Genius GP-07 + GP-02, Engineering EN-04 Jamie  
**Extra:** Audit AU-01 trust-of-reader  
**Angle:** Two gates / verify everything; cite papers or vendor docs for capability claims.

### health | spice | nature’s pinch | natures pinch | supplement | wellness | food | taste

**Keywords:** health, spice, nature, pinch, supplement, wellness, food, taste, organic, label  
**Emphasize:** Content CN-02 + CN-05, Genius GP-01, Growth GR-06 Zoe, Audit AU-03  
**Extra:** Drew CN-06 — **no medical claims without citations**; prefer food-label / provenance framing  
**Angle:** Taste beats wallpaper certificates; companion to trust pack.

### seo | discover | search | ranking | serp

**Keywords:** seo, discover, search, ranking, serp, google, index  
**Emphasize:** SEO full SE-01…SE-06, Growth GR-05 Quinn, Content Elena  
**Angle:** Truth first; SEO sharpens findability only.

### growth | distribution | newsletter | share | community

**Keywords:** growth, distribution, newsletter, share, community, viral, outreach  
**Emphasize:** Growth full, Genius GP-03, SEO SE-02  
**Angle:** Permission + remarkable; no paid spend without CEO ask.

### security | threat | csp | xss | dependency | headers

**Keywords:** security, threat, csp, xss, dependency, headers, vulnerability  
**Emphasize:** Security full SC-01…SC-06, Engineering EN-02, Audit AU-02  
**Angle:** Threat realism; cite advisories with CVE/URL when relevant.

---

## Routing algorithm (scripts + agents)

1. Lowercase the idea title + body.  
2. Score each topic by keyword hits.  
3. Pick the highest-scoring topic (ties → philosophy).  
4. Staff = Always-on + that topic’s **Emphasize** + **Extra**.  
5. Write the chosen IDs into `war-room/briefs/<slug>.md` under `## Expert squad`.  
6. Research pack + citations are mandatory before pending draft is marked ready for Mj.

Agents may add experts; they may not drop below ≥5 Genius + ≥5 Content + ≥5 SEO + ≥5 Growth + Security 3+ + Audit 3+.
