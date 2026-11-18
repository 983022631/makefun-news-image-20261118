// A news-image-daily entry (Node 22, standard library only).
//
// The entry image is the entry.png beside this file: a front page drawn
// programmatically by draw.py (Python + PIL) that sums up Wednesday
// 18 November 2026 in five stories. This program copies it to the output
// directory the grader provides, so the run is deterministic and offline.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(
  new URL('./entry.png', import.meta.url),
  join(outDir, 'entry.png'),
);
