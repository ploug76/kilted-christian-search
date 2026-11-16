# Kilted Christian Search: transcript and index audit, Nov 16, 2026

Site: https://ploug76.github.io/kilted-christian-search/ (repo ploug76/kilted-christian-search)
Source data left untouched: `/workspace/kilted-tags/all_shows_named.csv` and `/workspace/kilted-christian-index/transcripts/`.
Every correction is a display layer in `build.py`, which is now tracked in the repo at `tools/build.py`. The layer has four parts: TITLE_FIXES, EPISODE_FIXES, TRANSCRIPT_FIXES and loop cleanup. It writes `docs.json`, `t/*.txt.gz`, `idx/` and `bi/`.

## 1. Episode identity fixes (EPISODE_FIXES, keyed by audio URL)
Method: I fetched the Podbean page for every episode (1141 slugs) and read its JSON-LD (name, datePublished, audio contentUrl). Each of our transcripts was then matched to the page that owns **its own audio file**, and every remap was checked against what is said in the transcript.

**Eps 120–127, plus the 564–567 and 689–693 blocks, and 30/31/151.** A page list had shifted by one, so several transcripts showed a neighbouring episode's title or link. Each one was re-matched, and now the title, the transcript and the link all agree:
  - 2022-07-21: Ep 120 Brothers Sisters and a Bible
  - 07-22: Ep 121 Lyndon Lueders and Officer Jody. The intro says "episode 121 with Lyndon … and Officer Jody".
  - 07-25: Ep 122 The Conlee
  - 07-26: Ep 123 Livin and Duncan
  - 07-27: Ep 124 Brothers and a Bible with Evren
  - 07-28: Ep 125 MSMLIARS Thursday
  - 07-29: Ep 126 Chris and Raccoon
  - 07-30: Ep 127 Brothers and a Bible Saturday
  - Ep 30 Connecting the Dots, Ep 31 Know your enemy, Ep 151 The Conlee
  - Eps 564 (pt 1 and pt 2), 565, 566 and 567 American Idolatry. The transcript says "567 American Idolatry".
  - Eps 689 Little Red Rocking Chair (the transcript says so), 690, 691, 692 and 693 Stone of Scone
  - Durations for the 564–567 block had shifted along with the titles. They are now Podbean's values: 6614, 6336, 6658, 4170 and 2981 seconds.

**Links pointing at a neighbour's page, now fixed:** Eps 1018–1022, 958 and 959.

**Podbean page is gone (404):** Ep 1023 (Favorite Female Vocals) and Ep 960 (Peace or Prophesy?). The app now links the audio file instead, which plays.

**Ep 1093 "Jesus in the Old Testament".** The show tag is now Kilted Christian (regular), based on what the episode is about.

**Ep 884.** The date is now 2025-06-25, from Podbean.

**Ep 1061.** This page has no title on Podbean ("I hope everyone had a wonderful Holy weekend"). It now carries Ep 1061, because it sits between 1060 (Apr 3) and 1062 (Apr 7) and its content is the Book of Heaven study.

**Duplicate 694.** This was resolved by the remap: the real Ep 694 is "What is Real and What is illusion?". The other Podbean "694" page has no audio.

**Duplicate 863.** These are two **different recordings** with different audio. They are now labelled apart:
  - "(May 26, Memorial Day)", the Romans study, show Book of Heaven
  - "(May 27 upload, separate show)", show Kilted Christian (regular). It is possibly Ep 864, which has no Podbean page.

**Out-of-order dates, 1099 and 1091.** Our dates match Podbean: 1099 on 2026-07-07, and 1091 "(working Audio)" re-uploaded 2026-06-16/17. They look out of order only because the host uploaded them late. No change.

**Note on dates.** In 486 episodes, Podbean's publish date is one day after our date. Ours is the recording date (from the liveshow file name or the feed), so that is expected and was kept.

**Slug numbers that differ from the title:** 571 and 570 (slugs say 561/560), 349→347, 347→346, 346→345, 307→306. Our titles match the page titles and our links reach the right pages. These are the host's own slug typos, so they are noted only.

**Episode numbers Podbean itself uses twice:** 1122, 1004, 1000, 852, 798, 737, 670, 380, 374, 163 and 11, plus 568 in two parts. These are real separate episodes with correct links, so they are noted only. Two 568 pages share one audio file, and the 1096 plain page carries an older mp4 upload. Both are noted.

**Titles I was unsure about (left unchanged on purpose):**
- Ep 1 "Death Neigh Minds the Kirkyard"
- Ep 806 "Dezray"
- Ep 671 "Rene Serafini"
- Eps 586/631/984, BlackDragon spellings
- Ep 514 "onto"
- Ep 852 "Who's Line"
- Ep 1031 "Project Mockingbird"
- Ep 725 "Princes and the Paupers"

## 2. Transcript name and term corrections (TRANSCRIPT_FIXES)
Every rule is a regex that I checked against samples of real context before it was enabled. In total, 3,161 words were changed. The counts below are actual changes from the final build.

| Rule | Changes |
|---|---|
| Kilted Christian (Kylton / Kilton / Kilter / Kilda / Keltik / "Kilt the" …) | 776 |
| Kilted Christian ("killed the …", only before episode/show/family/studio/podcast) | 118 |
| Kilted Christian (after "this is / welcome to / joining") | 3 |
| Brothers and a Bible ("Brothers in a Bible") | 414 |
| MSM Liars ("MSN Liars") | 91 |
| Godcast ("God cast", excluding "cast out / down …") | 194 (+2 "God gas") |
| Livin and Duncan | 4 |
| Pains Angels ("Payne's / Pain's Angels") | 139 |
| Evren (Everon / Everyn / Evron / Evran) | 89 |
| Dustin Nemos | 44 |
| Podbean (pod bean, pod beam, podbeam, pot bean, paw bean, pa bean, Pahbeam) | 440, plus 7 "Podbean's" and 10 plural forms |
| Bards FM (Bard's FM, bards f m, bars fm, barge fm …) | 370 |
| Bards Fest ("bars fest") | 9 |
| Bible names: Ephesians 12, Corinthians 9, Isaiah 85, Ezekiel 4, Belshazzar 14, Enoch 16, Golgotha 6, Babylon 30, Babylonian 3, Shamgar 7, Jehovah 6, Lazarus 3 | 195 |
| Calvary ("Calgary", only beside cross/crucifixion/Christ, never Alberta/Canada/G7). All 10 were reviewed by hand. | 10 |
| Khazarian 54, Khazaria 16, Epstein 144, Rothschild 8, Rockefeller 3 | 225 |
| Scotland 10, Scottish 5, Culloden 6 | 21 |

**Not changed on purpose, because the right answer is uncertain:**
- "Conley" vs "Conlee": the co-host may really be named Conley. Search treats them as the same instead (see section 4).
- "Kitty to Karen", "Bard's Fest", "Ecclesiastius" (could be Ecclesiasticus), "Belsazar" (Belteshazzar), "samalia" (Somalia) and "Isiah" (a person's name).

## 3. Speech-to-text failures (loop cleanup plus a re-transcription recommendation)
I scanned all 1136 transcripts for repeat loops, long silences and very low words per minute.

**What changed.** Whisper sometimes gets stuck and writes the same line hundreds or thousands of times, and the real speech in that stretch is lost. In the display copy, any run of 15 or more identical lines in a row is now collapsed to one line plus a visible note: "[Transcription glitch: the line above repeated N times from A to B; the speech in that stretch is missing from this transcript.]" There were 23 runs in total. This stops the junk from flooding the reader and inflating search counts (for example, "I pray for you guys" no longer counts 207 times in Ep 1116).

**Badly damaged episodes.** In these episodes, a large part of the show is not in the transcript at all. **I recommend re-transcribing them.** That needs Peter's OK, because the source transcripts are off-limits.

| Ep | Title | Missing stretch |
|---|---|---|
| 1116 | End of Days Deception | 00:06:48–01:48:18 (101 min) |
| 65 | Convoy Talk with Gordon | 00:05:05–01:36:37 (92 min) |
| 68 | Brothers and a Bible, Times of Doubt | 00:04:39–01:36:22 (91 min) |
| 867 | Book of Heaven, Romans | 00:23:01–01:44:23 (81 min) |
| 509 | MSMLIARS Thursday | 00:31:54–01:45:55 (74 min) |
| 116 | Ali Graeff | 00:36:03–01:38:03 (62 min) |
| 1059 | What are Reptilians? | 00:58:08–01:53:50 (56 min) |
| 963 | Similarities of Hopi and Biblical Prophecy | 00:59:53–01:42:17 (42 min) |
| 707 | We are your Government… | 00:06:11–00:20:46 (15 min) |
| 687 | Book of Heaven, Colossians | 01:39:52–01:50:13 (10 min) |
| 828 | Governments Playing gods | 00:06:57–00:13:44 (7 min) |

**Minor runs** (under 3 minutes, collapsed and noted): 1094, 1089, 1004, 730, 719, 526, 513, 442, 431, 288 and 284.

**Long silences near the end of a show** (not verified; probably music, video or dead air, not missing speech):
- Early episodes 3–31: 11–27 minute gaps
- Ep 155: 23 min at 74 min
- Ep 181: 20 min at 91 min
- Ep 457: 16 min at 118 min
- Ep 459: 11 min at 119 min

Many short repeats (6–12 times) are real speech or song lyrics and were left alone.

## 4. Search and index
**Aliases.** "conlee" also finds and highlights "Conley" and "Connelly" (`aliases` in docs.json, with alias postings in the index).

**Exact phrases of 3 or more words.** Before, the app ranked these using word pairs only. That could put episodes at the top that don't contain the phrase (for example, "0 times as a phrase" on the first result). Now the app checks the actual transcripts of the best-ranked candidates. It shows only exact matches, with exact counts, and labels the rest as "possible match, checked as you scroll". Two-word phrases were already exact.

**Snippets** are now trimmed around the match, so very long transcript lines no longer push the highlighted word out of view.

**Exact index check** (`tools/verify_index.py`, rerun after re-transcription). I brute-force counted 411 words and 158 two-word phrases from the published transcripts and compared them with the index: **0 count mismatches**. Only 2 flags, both genuinely short audio: Ep 620 part 1 (31 s) and Ep 561 part 1 (520 s).

**Final build:** 1136 episodes, 74,887 terms, 1,876,653 phrase pairs, 19.1M words.

## 5. Links and audio
- All 1136 audio URLs return HTTP 200.
- Every episode now maps to the Podbean page that owns its audio, except 1023 and 960, whose pages are gone; they link the audio instead.
- Durations match Podbean within 2 s for every episode, now that the 564–567 block is fixed. The one exception is Ep 867, whose last timestamp runs 17 s past its duration, which is negligible.

## 6. Files
- `tools/build.py` holds all the correction tables and the build.
- `tools/verify_index.py`, `tools/test_site.py` and `tools/test_extra.py` are the checks.
- `tools/title-fixes-2026-11-16.md` and `tools/transcript-audit-2026-11-16.md` are the reports.
- The service worker cache is bumped to `kcs-v4`, so installed copies pick up the new data.

## 7. Re-transcription (update, Nov 16, 2026, afternoon)
Peter approved re-transcribing the episodes where speech was missing.
- **Setup.** Same as the original run: faster-whisper "small", CPU int8, English, with VAD. The one change is `condition_on_previous_text=False`, which stops one loop from feeding the next. Each episode got at most two attempts. Attempt 2 used beam 5, compression_ratio_threshold 2.0 and repetition_penalty 1.1.
- **Backups.** Every original .txt/.json/.meta.json was copied to `/workspace/kilted-transcripts-backup-2026-11-16/` before anything was replaced, and no original was deleted.
- **Checks before a new transcript was accepted:** no run of 15+ identical lines, at least 60 words a minute, and the transcript must reach 85% of the audio length.
- **Gap check on the slow episodes.** Eps 65, 867, 116, 963 and 687 came out at 69–133 words a minute. I measured the audio energy in each gap and re-transcribed the gaps with VAD off. Only Ep 65's first 3 minutes is the intro song. The other gaps were **real speech that Whisper had skipped** (normal loudness, clear talk when re-run). So every gap over 20 s in those 5 episodes was re-transcribed with VAD off and merged back in. A gap was left unfilled only when its re-run turned into a loop, which happened mostly in song or outro stretches.

| Ep | Before (words) | Now (words, wpm) | Status |
|---|---|---|---|
| 1116 | 115 (one line ×207) | 19,209, 175 | complete |
| 68 | 210 | 17,542, 172 | complete |
| 509 | | 19,199, 179 | complete |
| 1059 | | 19,711, 170 | complete |
| 707 | | 19,021, 175 | complete |
| 828 | | 18,891, 174 | complete |
| 65 | 159 | 13,780, 130 (27 min of skipped speech filled; 10 min outro/music not filled) | mostly complete |
| 867 | | 11,686, 112 (15 min filled) | complete; slow, conversational study |
| 116 | | 14,495, 144 (12.7 min filled) | complete |
| 687 | | 14,451, 127 (14.3 min filled) | complete |
| 963 | | 10,902, 105 (36 min filled) | **improved but probably still missing some speech** (attempt 1 had 15,125 words, but it failed the loop check) |
| 1089, 730, 526, 442, 288 (short loops) | | 168–181 wpm | complete |

**Still queued** (short loops; until they finish, these still show the collapsed-loop note): 1094, 1004, 719, 513, 431 and 284.

**Second publish.**
- **Gap-fill on the other 11 passed episodes.** The same no-VAD gap-fill was run on short gaps of 0.5–3 min in 1116, 68, 509, 1059, 707, 828, 1089, 730, 526, 442 and 288. Only a few dozen words were added per episode.
- **Six short-loop episodes failed and keep their originals.** Eps 1094, 1004, 719, 513, 431 and 284 failed both attempts: each new version had at least 10% fewer words than the original. Their originals are kept, with the short loop (under 1.5 minutes each) collapsed and noted on the site.
