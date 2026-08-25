# War Room 09 — Research & Citations

## Mission

Every factual claim in a Mjidea draft must be checkable. Philosophy can argue; it cannot invent studies, laws, or quotes.

## Standing order

1. **Web search / fetch** reputable sources before locking the angle. Prefer primary sources, standards bodies, peer-reviewed or major publishers, official docs.
2. Write a **research pack** to:
   - `reports/research/YYYY-MM-DD-<slug>.md`
   - (optional mirror) `war-room/output/<slug>.research.md`
3. Draft goes to **`drafts/pending/<slug>.md` only** — never auto-publish.
4. Draft must include a **References** section (or footnotes) with URL + title + date accessed for each cited fact.

## Who owns this

- **CN-06 Drew Fontaine** — claim inventory & citation completeness  
- Topic lead from `team/TOPIC-ROUTING.md`  
- **AU-01 Helena Orth** — “would a reader trust this?” gate before pending is marked READY

## Research pack template

```markdown
# Research — <slug>

- Date: YYYY-MM-DD
- Topic pack: <from TOPIC-ROUTING>
- Search queries used:
  - …

## Key findings
1. Claim … — Source: [Title](URL) — Accessed: YYYY-MM-DD — Notes: …

## Disputed / weak
- …

## Quotes worth using (verbatim only if sourced)
- “…” — Source …

## AGENT MUST FILL via web search
_(If offline or search failed — leave this banner and do not invent URLs.)_
```

## Draft citation rules

- Every empirical claim → reference.  
- Opinions and lived sparks (CEO voice) need no URL — mark as *lived* if helpful.  
- No fabricated DOIs, dead links, or “according to experts” without names + links.  
- If network fails: leave research pack with **AGENT MUST FILL via web search** and a pending draft scaffold; do not fake citations.

## Phase order (approval-gated publish)

| Step | Output |
|------|--------|
| Research | `reports/research/YYYY-MM-DD-<slug>.md` |
| Expert war room | brief + output packs |
| Draft | `drafts/pending/<slug>.md` + `war-room/output/<slug>.draft.md` |
| **Mj approve** | `./pipeline/approve.sh <slug>` or say “approve \<slug\>” |
| Publish | `site/src/content/blog/<slug>.md` |

**Never** skip approve. `execute` / `complete pending` stop at pending draft.
