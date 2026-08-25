#!/usr/bin/env node
/**
 * Cabinet Sutherland essay factory — human-voice problem/solution essays.
 * Writes markdown into site/src/content/blog from topics/topics-500.json
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const TOPICS = path.join(ROOT, 'topics', 'topics-500.json');
const OUT = process.env.OUT_DIR || path.join(ROOT, 'site', 'src', 'content', 'blog');
const START = Number(process.env.START || 0);
const LIMIT = Number(process.env.LIMIT || 9999);

const stakes = [
  'You feel it in the evening, when the day is gone and you cannot name what you did with your mind.',
  'Younger people feel it as a low-grade panic that never quite becomes a sentence.',
  'Parents feel it when they realize the house is full of screens and empty of unhurried talk.',
  'Workers feel it on Sunday night, already bracing for a week that will not remember them.',
  'Neighbors feel it when they stop knowing the names of the people who share their air.',
  'Students feel it as a performance that never clocks out.',
  'The body keeps the score even when the feed resets the mood.',
];

const sceneBits = [
  'Someone unlocks a phone before their eyes have fully opened.',
  'A group sits together, each face lit from below, laughing at different jokes.',
  'A calendar is packed, yet the week feels strangely uninhabited.',
  'A young person can explain a crisis in the abstract and still not know who to text.',
  'A policy PDF exists. A habit still wins.',
  'The advice is everywhere. The defaults have not moved.',
];

const closes = [
  'Start smaller than your pride wants. That is usually where the door actually is.',
  'If it only works when you feel inspired, it does not work.',
  'Put the better behavior where status already lives — or move status.',
  'The next generation does not need another sermon. They need a redesigned room.',
  'Ask what the tired version of you will still do. Build for that person.',
  'Leave one cleaner default behind you this week. Then another.',
];

function esc(s) {
  return String(s).replace(/"/g, '\\"');
}

function para(...parts) {
  return parts.filter(Boolean).join(' ');
}

function essay(t, idx) {
  const stake = stakes[idx % stakes.length];
  const scene = sceneBits[idx % sceneBits.length];
  const close = closes[idx % closes.length];
  const year = 2026;
  const month = String((idx % 12) + 1).padStart(2, '0');
  const day = String((idx % 27) + 1).padStart(2, '0');
  const pubDate = `${year}-${month}-${day}`;

  const p1 = para(
    t.opening,
    stake,
    `The problem shows up as ${t.problem} — ordinary, almost respectable, until you notice what it quietly spends.`,
  );

  const p2 = para(
    scene,
    `We keep treating ${t.problem} like a personal failure of will.`,
    `Willpower is a thin currency. Environments print their own money.`,
  );

  const p3 = para(
    `Here is the flip Cabinet Sutherland cares about: ${t.reframe}`,
    `Information rarely loses to laziness. It loses to whatever feels easier, safer, or higher-status in the moment.`,
  );

  const p4 = para(
    `A workable move is not a TED slogan. It is ${t.solution}.`,
    `Make it visible. Make it slightly inconvenient to skip. Make it feel like taste when you keep it.`,
  );

  const p5 = para(
    `For younger generations especially, lectures about character bounce off interfaces built to harvest impulse.`,
    `If you want different people, change what the room rewards — then practice the new ritual until it is boring.`,
  );

  const p6 = para(
    `None of this requires you to become a monk.`,
    `It asks you to stop romanticizing heroics and start redesigning defaults.`,
    close,
  );

  const description = `${t.problem[0].toUpperCase() + t.problem.slice(1)} is a human problem with a workable door: ${t.solution}.`;

  const body = `---
title: "${esc(t.title)}"
description: "${esc(description)}"
pubDate: ${pubDate}
tags: ${JSON.stringify(t.tags)}
category: "${t.category}"
draft: false
thesis: "${esc(t.thesis)}"
---

${p1}

${p2}

## The reframe

${p3}

## A door that opens

${p4}

${p5}

${p6}
`;

  return body;
}

function main() {
  const data = JSON.parse(fs.readFileSync(TOPICS, 'utf8'));
  fs.mkdirSync(OUT, { recursive: true });
  const slice = data.topics.slice(START, START + LIMIT);
  let written = 0;
  for (let i = 0; i < slice.length; i++) {
    const t = slice[i];
    const file = path.join(OUT, `${t.slug}.md`);
    fs.writeFileSync(file, essay(t, START + i));
    written++;
  }
  console.log(`Wrote ${written} essays to ${OUT} (start=${START})`);
}

main();
