# Date fixes, November 24, 2026

## Cause

Most episode dates in the search app come from `liveshow_YYYY_MM_DD_HHMM.mp3` filenames and match the live show day (1,008 episodes). Starting around June 2026, later episodes were uploaded to Podbean in batches and no longer used those filenames. For those, the app used the Podbean RSS / JSON-LD `pubDate`, which is the **upload** day, not the air date.

That is why several recent shows share one date:

- 7 episodes dated 2026-08-03 (Eps 1121–1127, including two titled 1122)
- 8 dated 2026-07-22 (Eps 1113–1120)
- 10 dated 2026-07-07
- 8 dated 2026-06-08
- plus smaller June/July clusters

The official Podbean feed (`https://feed.podbean.com/kiltedchristian/feed.xml`) still has those same batch dates, and the newest item is still KC Ep 1127.

## Verified air dates (this update)

RumbleRankings (`https://rumblerankings.com/channel/kiltedchristian`, page updated 2026-11-24) lists Rumble upload/air dates for its last 10 videos. Eight of those disagree with the Podbean batch date and are applied as `DATE_FIXES` in `build.py`:

| Episode | Title | Old (Podbean upload) | New (Rumble air date) |
| --- | --- | --- | --- |
| 1121 | What is Heaven | 2026-08-03 | 2026-07-23 |
| 1119 | Book by the Fire | 2026-07-22 | 2026-07-21 |
| 1118 | 80s Music Night | 2026-07-22 | 2026-07-18 |
| 1117 | Weaponization of Church | 2026-07-22 | 2026-07-17 |
| 1116 | End of Days Deception | 2026-07-22 | 2026-07-16 |
| 1115 | Political Deaths | 2026-07-22 | 2026-07-15 |
| 1114 | Anything but Nirvana | 2026-07-22 | 2026-07-11 |
| 1113 | Mandela Effect | 2026-07-22 | 2026-07-10 |

1112 (2026-07-09) and 1120 (2026-07-22) already matched Rumble, so they were left alone.

## Not changed (no verified air date yet)

RumbleRankings, refreshed 2026-11-24, shows the channel's last Rumble upload as 2026-07-23 (Ep 1121). Eps 1122–1127 (the rest of the Aug 3 Podbean batch) are not in that last-10 list, and Rumble itself is blocked from this box by Cloudflare, so those six (seven catalog rows, two titled 1122) stay on 2026-08-03 for now. The June 8, June 16, July 7, and July 9 clusters are also still Podbean upload dates.

The source CSV and transcripts were not modified.

## New episodes

As of 2026-11-24, the live Podbean feed and homepage still end at Ep 1127. No newer episodes were available to transcribe from Podbean. Book of Heaven and Church by the Fire tags were left unchanged.
