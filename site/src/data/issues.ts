/** Curated issue seeds from team/IDEA-BANK.md — expandable by Mj. */

export type Issue = {
  id: string;
  title: string;
  summary: string;
  angle: string;
  tags: string[];
};

/** Active prompts — top floats + pressure-ready themes. */
export const currentIssues: Issue[] = [
  {
    id: 'trust-isnt-certified',
    title: 'Trust isn’t certified',
    summary:
      'Paper stamps prove a day; taste and named origins prove a relationship.',
    angle: 'Genius + Brand: proof theater vs lived truth',
    tags: ['trust', 'brand', 'proof'],
  },
  {
    id: 'perception-beats-the-stopwatch',
    title: 'Perception beats the stopwatch',
    summary: 'Fix the felt wait before building a faster train.',
    angle: 'Rory reframe before rebuild — High Line vs subway',
    tags: ['perception', 'behavior', 'leverage'],
  },
  {
    id: 'verify-everything',
    title: 'Verify everything',
    summary:
      'No automatically trusted content — pre-AI or post-AI; verification is the moral stance.',
    angle: 'Audit + Security + Philosophy',
    tags: ['verification', 'AI', 'ethics'],
  },
  {
    id: 'commodity-to-diamond',
    title: 'Commodity → Diamond',
    summary:
      'Heritage + perception turn bulk SKUs into lifestyle diamonds without fake luxury.',
    angle: 'Kill Step: zero-cost perception shift',
    tags: ['brand', 'perception', 'commodity'],
  },
  {
    id: 'local-first-is-respect',
    title: 'Local-first is respect',
    summary:
      'Private emotion data staying on-device is dignity, not a missing feature.',
    angle: 'Privacy as character; growth without betrayal',
    tags: ['privacy', 'product', 'dignity'],
  },
  {
    id: 'trust-is-the-real-supplement',
    title: 'Trust is the real supplement',
    summary:
      'In claim-heavy categories, trust is the scarce nutrient — not the capsule.',
    angle: 'Brand epistemics; avoid medical claims',
    tags: ['trust', 'supplements', 'brand'],
  },
  {
    id: 'perception-is-the-real-product',
    title: 'Perception is the real product',
    summary:
      'Humans buy framed perception; craft is changing the game board, not shouting louder.',
    angle: 'Writing craft + ethical reframe (not manipulation)',
    tags: ['perception', 'craft', 'ethics'],
  },
  {
    id: 'two-gates-infinite-agents',
    title: 'Two gates, infinite agents',
    summary:
      'Human touches idea-approve and money/go-live; war rooms do the middle.',
    angle: 'Agent-company design',
    tags: ['agents', 'ops', 'venture'],
  },
];

/** Later seeds — still sharp, not yet in the active queue. */
export const futureIssues: Issue[] = [
  {
    id: 'catharsis-then-breath',
    title: 'Catharsis, then breath',
    summary: 'Anger needs cartoon discharge and a calm landing.',
    angle: 'Philosophy + product ethics',
    tags: ['emotion', 'product', 'ethics'],
  },
  {
    id: 'cartoon-zero-harm',
    title: 'Cartoon violence, zero harm',
    summary: 'Symbolic heat is a third script between suppress and escalate.',
    angle: 'Product morals; symbol ≠ endorsement',
    tags: ['vent', 'symbol', 'morals'],
  },
  {
    id: 'no-lectures-just-play',
    title: 'No lectures, just play',
    summary: 'Some truths arrive as motion first; play can be a serious instrument.',
    angle: 'Anti-wellness-sermon voice',
    tags: ['play', 'product', 'voice'],
  },
  {
    id: 'build-the-ad-not-the-warehouse',
    title: 'Build the ad, not the warehouse',
    summary: 'Cheap demand proof before inventory — respect for time, not cynicism.',
    angle: 'Antifragile product essays',
    tags: ['venture', 'demand', 'antifragile'],
  },
  {
    id: 'honest-near-zero-downside',
    title: 'Near-zero downside',
    summary: 'Kill criteria and recoverability beat theatrical certainty.',
    angle: 'Ethics of systems pitching',
    tags: ['risk', 'venture', 'honesty'],
  },
  {
    id: 'the-seed-must-self-check',
    title: 'The seed must self-check',
    summary: 'Portable intelligence is method + verify, not cargo hope.',
    angle: 'Agent/ops philosophy',
    tags: ['agents', 'method', 'verify'],
  },
  {
    id: 'single-path-of-truth',
    title: 'Single path of truth',
    summary: 'One canonical path per job — clarity as where work can be found.',
    angle: 'Multi-machine life essays',
    tags: ['ops', 'clarity', 'systems'],
  },
  {
    id: 'parallel-minds-one-synthesis',
    title: 'Parallel minds, one synthesis',
    summary:
      'Disagreement is fuel; the product is the sentence that survives rivals.',
    angle: 'Mechanism essay for Genius Panel',
    tags: ['war-room', 'synthesis', 'debate'],
  },
  {
    id: 'sell-story-not-commodity',
    title: 'Sell the story, not the commodity',
    summary: 'Provenance and craft beat commodity price wars.',
    angle: 'Brand storytelling without romanticizing poverty',
    tags: ['story', 'brand', 'craft'],
  },
  {
    id: 'one-problem-micro-saas',
    title: 'One-problem Micro SaaS',
    summary: 'Tiny tools, one job, subscription — no VC theater.',
    angle: 'Case-study pipeline',
    tags: ['saas', 'product', 'focus'],
  },
  {
    id: 'long-and-short-of-brand',
    title: 'Long and short of brand',
    summary: 'Separate activation clicks from equity that compounds.',
    angle: 'Growth: refuse equity-burning hacks',
    tags: ['brand', 'growth', 'equity'],
  },
  {
    id: 'kill-step-and-strike-rate',
    title: 'Kill Step & strike-rate honesty',
    summary:
      'End with the bold move competitors fear; reject polite nonsense.',
    angle: 'Close every war room with a Kill Step',
    tags: ['kill-step', 'war-room', 'honesty'],
  },
  {
    id: 'content-empire-vs-human-philosophy',
    title: 'Content empire vs human philosophy',
    summary: 'Keep systems tooling; never let SEO farms eat the voice.',
    angle: 'Strategy tension made explicit',
    tags: ['voice', 'SEO', 'strategy'],
  },
  {
    id: 'philosophy-war-room',
    title: 'Philosophy needs a war room',
    summary: 'Pressure that makes a thought clearer, stranger, more itself.',
    angle: 'Ancestor of shipped essays — deepen or retire',
    tags: ['philosophy', 'war-room'],
  },
];

/** Inbox-ready titles surfaced on /ideas as seeds (not published essays). */
export const inboxSeeds: { title: string; summary: string }[] = [
  ...currentIssues.slice(0, 5).map((i) => ({
    title: i.title,
    summary: i.summary,
  })),
];
