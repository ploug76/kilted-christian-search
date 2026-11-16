# Kilted Christian Search: title fixes (Nov 16, 2026)

These fixes are applied at build time from `TITLE_FIXES` in build.py. The source CSV and the transcripts were not changed. Titles are not part of the search index (only the transcript text is), so docs.json was the only data file that needed patching.

## Changes (36)

- **Ep 1122**: `KC Ep 1122 Nusic that Starts with D` → `KC Ep 1122 Music that Starts with D`. typo flagged by Peter
- **Ep 1112**: `KC Ep 1112: What id the Fruit?` → `KC Ep 1112: What is the Fruit?`. typo flagged by Peter
- **Ep 1092**: `KC ep 1092: Lebor Gabal Erenn` → `KC ep 1092: Lebor Gabála Érenn`. title of the medieval Irish "Book of Invasions"; transcript: "labor of Gabala Aaron which is the book of invasions"
- **Ep 1078**: `KC Ep1078: Churches meet about UFO discloser.` → `KC Ep1078: Churches meet about UFO disclosure.`. misspelling; host says "Churches Meet About UFO Disclosure"
- **Ep 1047**: `KC Ep1047:   Celts, Caileigh, and Pibroch Sounds.` → `KC Ep1047:   Celts, Ceilidh, and Pibroch Sounds.`. host explains "the Kayleigh part... traditional Irish dancing" = ceilidh (Gaelic dance); Caileigh is a girl's name
- **Ep 1023**: `KC Ep1023 : Â Favorite Female Vocals.` → `KC Ep1023 :  Favorite Female Vocals.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 1011**: `KC Ep1011 :  Iâm Beginning to Think Clintons are Crooks.` → `KC Ep1011 :  I’m Beginning to Think Clintons are Crooks.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 984**: `KC Ep984 : Iâm No Black Dragon or GJR Radio but Iâll Try .` → `KC Ep984 : I’m No Black Dragon or GJR Radio but I’ll Try .`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 960**: `KC Ep960: Â Peace or Prophesy?` → `KC Ep960:  Peace or Prophesy?`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 920**: `KC Ep920:     Whatâs Your Favorite? Chat Interactive.` → `KC Ep920:     What’s Your Favorite? Chat Interactive.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 906**: `KC Ep906:  Revolation Timeline.` → `KC Ep906:  Revelation Timeline.`. misspelling; host says "Revelation Timeline"
- **Ep 893**: `KC Ep893: Conlees not on Epsteinâs non existent list.` → `KC Ep893: Conlees not on Epstein’s non existent list.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 852**: `KC Ep852: Whoâs Line is it Anyway?.` → `KC Ep852: Who’s Line is it Anyway?.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 824**: `KC Ep824:  21 hours of Corey Booker. .` → `KC Ep824:  21 hours of Cory Booker. .`. Senator Cory Booker (public record); transcript "Cory Booker"
- **Ep 796**: `KC Ep796:   Canada, we arenât your enemy .` → `KC Ep796:   Canada, we aren’t your enemy .`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 783**: `KC Ep783: Church by theFire:Confrontation 2 Conversation.` → `KC Ep783: Church by the Fire: Confrontation 2 Conversation.`. missing spaces
- **Ep 770**: `KC Ep770: What a Long Strange Trip itâs Been.` → `KC Ep770: What a Long Strange Trip it’s Been.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 750**: `KC Ep750: Official Godcast, Kutrina Chapman.` → `KC Ep750: Official Godcast, Katrina Chapman.`. host intro: "our special guest Katrina Chapman all the way from Canada"; guest: "I'm Katrina from Vancouver BC" (25 hits)
- **Ep 725**: `KC Ep725:  Pains Angels premier,The Princes and the Paupers.` → `KC Ep725:  Pains Angels premiere,The Princes and the Paupers.`. misspelling; host: "First, I got a premiere"
- **Ep 724**: `KC Ep724:   Church by the Fire, Whatâs your calling?.` → `KC Ep724:   Church by the Fire, What’s your calling?.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 702**: `KC Ep702:  Storms, War, Economy, and Preperation .` → `KC Ep702:  Storms, War, Economy, and Preparation .`. misspelling
- **Ep 664**: `KC Ep664:  PTV, Steven, itâs a Mad Mad Mad World.` → `KC Ep664:  PTV, Steven, it’s a Mad Mad Mad World.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 645**: `KC Ep645:  Book of Heaven: Phillipians 4` → `KC Ep645:  Book of Heaven: Philippians 4`. Bible book misspelled (other titles use Philippians)
- **Ep 629**: `KC Ep629:  PTV , Mary Flynn OâNeill.` → `KC Ep629:  PTV , Mary Flynn O’Neill.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 575**: `Kilted Christian Ep575: Big olâ Rabbit Hole.` → `Kilted Christian Ep575: Big ol’ Rabbit Hole.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 469**: `Kilted Christian Ep469: Jeffâs words from God.` → `Kilted Christian Ep469: Jeff’s words from God.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 397**: `Kilted Christian Ep397: You canât serve two masters.` → `Kilted Christian Ep397: You can’t serve two masters.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 257**: `Kilted Christian Ep257:  MSMLIARS Crampus.` → `Kilted Christian Ep257:  MSMLIARS Krampus.`. host: "this show is about Krampus"
- **Ep 144**: `Kilted Christian Ep 144: Sometimes Good Guys Donât Wear White.` → `Kilted Christian Ep 144: Sometimes Good Guys Don’t Wear White.`. text-encoding garbage (mojibake) for an apostrophe/space
- **Ep 116**: `Kilted Christian Ep 116: Ali Graef.` → `Kilted Christian Ep 116: Ali Graeff.`. matches Ep 539 title; guest is the Missouri election-integrity advocate Ali Graeff (Show Me Sentinel interview, LinkedIn); Ep 116 transcript is about the EAC/elections
- **Ep 88**: `Kilted Christian Ep 88:  Chris Wilson, Rockafellers.` → `Kilted Christian Ep 88:  Chris Wilson, Rockefellers.`. host: "talking about Rockefellers"; Rockefeller Foundation
- **Ep 78**: `Kilted Christian Ep 78: Gorden Talk: WHO.` → `Kilted Christian Ep 78: Gordon Talk: WHO.`. guest is Gordon (transcript "Gordon, how are you doing buddy?"; Ep 65 and Ep 130 titles say Gordon)
- **Ep 58**: `Kilted Christian Ep 58: Brothers and a Bible, Mount Olive` → `Kilted Christian Ep 58: Brothers and a Bible, Mount of Olives`. topic is the conversation on the Mount of Olives (Olivet Discourse); host: "the conversation that took place on the Mountain of Olives"; Ep 347 title uses "Mount of Olives"
- **Ep 51**: `Kilted Christian ep 51:  SnakeOil, Stu Paters, and Dr Bryon Ardis` → `Kilted Christian ep 51:  SnakeOil, Stew Peters, and Dr Bryan Ardis`. host plays an interview with "Stu Peters and Dr. Brian Artis"; the real people are broadcaster Stew Peters and Dr. Bryan Ardis
- **Ep 38**: `Kilted Christian Ep 38: Occams Razer` → `Kilted Christian Ep 38: Occams Razor`. misspelling; host: "Occam's razor"
- **Ep 18**: `Kilted Christian Ep 18: Donât believe your lying eyes` → `Kilted Christian Ep 18: Don’t believe your lying eyes`. text-encoding garbage (mojibake) for an apostrophe/space

## Unsure: left unchanged

- **Ep 1** `Death Neigh Minds the Kirkyard`: The host says "Death, Nay, Minds the Kirkyard" and calls it an old Scots saying. I couldn't verify the proverb, and "Neigh" might be meant as "ne'er" or "nigh".
- **Ep 806** `Official Godcast; Dezray`: The transcript says "Desiree", but Dezray could be the guest's own spelling or TikTok handle.
- **Ep 671** `Official Godcast: Rene Serafini`: The transcript says "Renee Serafini" (the guest is a woman). The spelling can't be confirmed from audio.
- **Ep 586 / 631 / 984** `BlackDragonsRadio vs BlackDragonRadio vs Black Dragon`: The guest's handle is spelled inconsistently across titles. The audio says both "Black Dragons Radio" and "Black Dragon Radio".
- **Ep 514** `Charity onto others`: This may be meant as "unto others", but the host says "onto" on air.
- **Ep 852** `Who’s Line is it Anyway?`: The TV show is "Whose Line Is It Anyway?". This may just be the host's wording.
- **Ep 1031** `Project Mockingbird Still Operational`: The historical name is "Operation Mockingbird" (Ep 48 uses that name). This one is the host's own title.
- **Ep 725** `The Princes and the Paupers`: Probably intentional wordplay, so I left it.

Intentional wordplay left alone: Ep 666 "Ep66VI", 1036 SQTU (the host explains it's State of the Union), 926 "Product Re (Blanding)" (a pun on rebranding and the bland Cracker Barrel food), 754 "Center of the Word" (the host says "not the world, the word"), 646 "Conversation with He" (the host explains it), 344 "Putin out the Truth", 917, 713, 698, 1076, 298 "Superb Owl", 608 and 173 "Punky Pewster".

## Episode-number and data issues: flagged, not changed

- **Transcript and link don't match the title around Eps 120–126 (July 2022 liveshow files).** The titled episode, its transcript and its episode-page link point to different episodes:
  - "Ep 121 Lyndon Lueders and Officer Jody" has the Ep 123 Livin and Duncan transcript and the ep-123 page link.
  - "Ep 123 Livin and Duncan" has the Ep 122 Conlee transcript and link.
  - "Ep 122 The Conlee" links to ep-124.
  - "Ep 120 Brothers Sisters and a Bible" links to ep-121.
  - "Ep 125 MSMLIARS Thursday" links to ep-126.
  - This needs a re-mapping of audio files to episodes in the source index, not a title edit.
- **Podbean page slugs disagree with title numbers:**
  - Ep 571 is posted as ep561, and Ep 570 as ep560 (the audio intros also say 561 and 560).
  - Ep 349 is posted as ep347, Ep 347 as ep346, Ep 346 as ep345, and Ep 307 as ep306.
- **Duplicate numbers on different episodes:** 1122 (Music that Starts with D / What is Hell), 1004, 1000, 852, 798, 737, 670, 380, 374, 163, 11. Ep 694 and Ep 863 each appear twice with identical titles.
- **Out of order:** Ep 1099 is dated between 1102 and 1101. Ep 1091 (working audio) is dated after 1098.
- **Show tag:** Ep 1093 "Jesus in the Old Testament" is tagged Music night.

## Duration display fix

app.js `fmtDur` rounded the minutes separately from the hours, so 7,187 s (Ep 1121) showed as "1h 60m". It now rounds to total minutes first, so Ep 1121 shows "2h 0m". The service worker cache was bumped from kcs-v2 to kcs-v3 so installed phones update.
