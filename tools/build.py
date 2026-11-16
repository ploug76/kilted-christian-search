#!/usr/bin/env python3
"""Build static search site data from Kilted Christian transcripts (read-only on sources)."""
import csv, json, os, re, gzip, unicodedata, collections, math, shutil
SRC_CSV='/workspace/kilted-tags/all_shows_named.csv'
OUT='/workspace/kilted-christian-search/site'
TS=re.compile(r'^\[\d\d:\d\d:\d\d\]\s*', re.M)
TOK=re.compile(r"[^\W_]+(?:['’][^\W_]+)*")
def norm(s): return unicodedata.normalize('NFC', s).casefold().replace('’',"'")
def toks(text): return TOK.findall(norm(TS.sub('',text)))
# Title corrections (Nov 16, 2026 review). Key: (episode number, original title as in the CSV, stripped).
# Applied at build time only; the source CSV and transcripts are not modified. See title-fixes-2026-11-16.md.
TITLE_FIXES={
    ('1122', 'KC Ep 1122 Nusic that Starts with D'): 'KC Ep 1122 Music that Starts with D',
    ('1112', 'KC Ep 1112: What id the Fruit?'): 'KC Ep 1112: What is the Fruit?',
    ('1092', 'KC ep 1092: Lebor Gabal Erenn'): 'KC ep 1092: Lebor Gabála Érenn',
    ('1078', 'KC Ep1078: Churches meet about UFO discloser.'): 'KC Ep1078: Churches meet about UFO disclosure.',
    ('1047', 'KC Ep1047:   Celts, Caileigh, and Pibroch Sounds.'): 'KC Ep1047:   Celts, Ceilidh, and Pibroch Sounds.',
    ('1023', 'KC Ep1023 : Â\xa0Favorite Female Vocals.'): 'KC Ep1023 :  Favorite Female Vocals.',
    ('1011', 'KC Ep1011 :  Iâ\x80\x99m Beginning to Think Clintons are Crooks.'): 'KC Ep1011 :  I’m Beginning to Think Clintons are Crooks.',
    ('984', 'KC Ep984 : Iâ\x80\x99m No Black Dragon or GJR Radio but Iâ\x80\x99ll Try .'): 'KC Ep984 : I’m No Black Dragon or GJR Radio but I’ll Try .',
    ('960', 'KC Ep960: Â\xa0Peace or Prophesy?'): 'KC Ep960:  Peace or Prophesy?',
    ('920', 'KC Ep920:     Whatâ\x80\x99s Your Favorite? Chat Interactive.'): 'KC Ep920:     What’s Your Favorite? Chat Interactive.',
    ('906', 'KC Ep906:  Revolation Timeline.'): 'KC Ep906:  Revelation Timeline.',
    ('893', 'KC Ep893: Conlees not on Epsteinâ\x80\x99s non existent list.'): 'KC Ep893: Conlees not on Epstein’s non existent list.',
    ('852', 'KC Ep852: Whoâ\x80\x99s Line is it Anyway?.'): 'KC Ep852: Who’s Line is it Anyway?.',
    ('824', 'KC Ep824:  21 hours of Corey Booker. .'): 'KC Ep824:  21 hours of Cory Booker. .',
    ('796', 'KC Ep796:   Canada, we arenâ\x80\x99t your enemy .'): 'KC Ep796:   Canada, we aren’t your enemy .',
    ('783', 'KC Ep783: Church by theFire:Confrontation 2 Conversation.'): 'KC Ep783: Church by the Fire: Confrontation 2 Conversation.',
    ('770', 'KC Ep770: What a Long Strange Trip itâ\x80\x99s Been.'): 'KC Ep770: What a Long Strange Trip it’s Been.',
    ('750', 'KC Ep750: Official Godcast, Kutrina Chapman.'): 'KC Ep750: Official Godcast, Katrina Chapman.',
    ('725', 'KC Ep725:  Pains Angels premier,The Princes and the Paupers.'): 'KC Ep725:  Pains Angels premiere,The Princes and the Paupers.',
    ('724', 'KC Ep724:   Church by the Fire, Whatâ\x80\x99s your calling?.'): 'KC Ep724:   Church by the Fire, What’s your calling?.',
    ('702', 'KC Ep702:  Storms, War, Economy, and Preperation .'): 'KC Ep702:  Storms, War, Economy, and Preparation .',
    ('664', 'KC Ep664:  PTV, Steven, itâ\x80\x99s a Mad Mad Mad World.'): 'KC Ep664:  PTV, Steven, it’s a Mad Mad Mad World.',
    ('645', 'KC Ep645:  Book of Heaven: Phillipians 4'): 'KC Ep645:  Book of Heaven: Philippians 4',
    ('629', 'KC Ep629:  PTV , Mary Flynn Oâ\x80\x99Neill.'): 'KC Ep629:  PTV , Mary Flynn O’Neill.',
    ('575', 'Kilted Christian Ep575: Big olâ\x80\x99 Rabbit Hole.'): 'Kilted Christian Ep575: Big ol’ Rabbit Hole.',
    ('469', 'Kilted Christian Ep469: Jeffâ\x80\x99s words from God.'): 'Kilted Christian Ep469: Jeff’s words from God.',
    ('397', 'Kilted Christian Ep397: You canâ\x80\x99t serve two masters.'): 'Kilted Christian Ep397: You can’t serve two masters.',
    ('257', 'Kilted Christian Ep257:  MSMLIARS Crampus.'): 'Kilted Christian Ep257:  MSMLIARS Krampus.',
    ('144', 'Kilted Christian Ep 144: Sometimes Good Guys Donâ\x80\x99t Wear White.'): 'Kilted Christian Ep 144: Sometimes Good Guys Don’t Wear White.',
    ('116', 'Kilted Christian Ep 116: Ali Graef.'): 'Kilted Christian Ep 116: Ali Graeff.',
    ('88', 'Kilted Christian Ep 88:  Chris Wilson, Rockafellers.'): 'Kilted Christian Ep 88:  Chris Wilson, Rockefellers.',
    ('78', 'Kilted Christian Ep 78: Gorden Talk: WHO.'): 'Kilted Christian Ep 78: Gordon Talk: WHO.',
    ('58', 'Kilted Christian Ep 58: Brothers and a Bible, Mount Olive'): 'Kilted Christian Ep 58: Brothers and a Bible, Mount of Olives',
    ('51', 'Kilted Christian ep 51:  SnakeOil, Stu Paters, and Dr Bryon Ardis'): 'Kilted Christian ep 51:  SnakeOil, Stew Peters, and Dr Bryan Ardis',
    ('38', 'Kilted Christian Ep 38: Occams Razer'): 'Kilted Christian Ep 38: Occams Razor',
    ('18', 'Kilted Christian Ep 18: Donâ\x80\x99t believe your lying eyes'): 'Kilted Christian Ep 18: Don’t believe your lying eyes',
}
# Episode identity/display corrections (Nov 16, 2026 audit), keyed by the episode's audio URL.
# Evidence: each Podbean episode page's JSON-LD (name, datePublished, audio contentUrl) matched to our audio,
# plus the transcript intro/content. See transcript-audit-2026-11-16.md. Source CSV/transcripts untouched.
EPISODE_FIXES={
    # Podbean episode page for this audio is a 404; link the audio file instead
    'https://mcdn.podbean.com/mf/web/ik93ks3lhsl9bqn5/liveshow_2026_02_06_2058.mp3': {'url': ''},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/o0xvz0rjd5nh00mm/liveshow_2026_02_05_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep1022-god-will-not-be-mocked/'},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/6c9539dh1qc5ii54/liveshow_2026_02_04_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep1021-conlee-never-went-to-the-island/'},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/qe0390b9mbki4nd5/liveshow_2026_02_03_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep1020-as-bad-as-we-thought/'},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/ckajbbylsctoies9/liveshow_2026_02_02_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep1019-book-of-heaven/'},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/hqweuehntk1a80w7/liveshow_2026_01_23_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep1018-best-male-vocals/'},
    # Podbean episode page for this audio is a 404; link the audio file instead
    'https://mcdn.podbean.com/mf/web/n9vpi4br15xt8mee/liveshow_2025_10_14_2058.mp3': {'url': ''},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/4ny40s9o9yk8uvtu/liveshow_2025_10_09_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep959-lower-case-gods/'},
    # episode link pointed at a neighbouring episode's page; now the Podbean page whose audio matches
    'https://mcdn.podbean.com/mf/web/nam9x98d2rmb54w5/liveshow_2025_10_08_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep958-dangers-of-ai/'},
    # transcript audio belongs to Podbean page 'KC Ep693:  Stone of Scone.' (was labelled '694' 'KC Ep694:  What is Real and What is illusion?'); intro/content verified
    'https://mcdn.podbean.com/mf/web/olxe6vntta20mkkl/liveshow_2024_09_18_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep693-stone-of-scone/', 'title': 'KC Ep693:  Stone of Scone.', 'ep': '693', 'show': 'Kilted Christian (regular)'},
    # transcript audio belongs to Podbean page 'KC Ep692:  God only knows .' (was labelled '693' 'KC Ep693:  Stone of Scone.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/vu2gerli0ug64gho/liveshow_2024_09_17_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep692-god-only-knows/', 'title': 'KC Ep692:  God only knows .', 'ep': '692', 'show': 'Kilted Christian (regular)'},
    # transcript audio belongs to Podbean page 'KC Ep691:  Church by the Fire. .' (was labelled '692' 'KC Ep692:  God only knows .'); intro/content verified
    'https://mcdn.podbean.com/mf/web/qivijy197jdxtfow/liveshow_2024_09_14_1758.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep691-church-by-the-fire/', 'title': 'KC Ep691:  Church by the Fire. .', 'ep': '691', 'show': 'Church by the Fire'},
    # transcript audio belongs to Podbean page 'KC Ep690:  Sin, Transgression, Iniquity.' (was labelled '691' 'KC Ep691:  Church by the Fire. .'); intro/content verified
    'https://mcdn.podbean.com/mf/web/pzivp1o47exuhbyt/liveshow_2024_09_12_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep690-sin-transgression-iniquity/', 'title': 'KC Ep690:  Sin, Transgression, Iniquity.', 'ep': '690', 'show': 'Kilted Christian (regular)'},
    # transcript audio belongs to Podbean page 'KC Ep689:  Little Red Rocking Chair.' (was labelled '690' 'KC Ep690:  Sin, Transgression, Iniquity.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/2olr4cvpzcoymobt/liveshow_2024_09_11_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kc-ep689-little-red-rocking-chair/', 'title': 'KC Ep689:  Little Red Rocking Chair.', 'ep': '689', 'show': 'Guest interview (Kilted Christian)'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep567: American Idolatry .' (was labelled '568' 'Kilted Christian Ep568: Sling and Stone.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/0zwfjh/liveshow_2024_03_19_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kilted-christian-ep567-american-idolatry/', 'title': 'Kilted Christian Ep567: American Idolatry .', 'ep': '567', 'show': 'Kilted Christian (regular)', 'dur': 6614},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep566: Royal Pains .' (was labelled '567' 'Kilted Christian Ep567: American Idolatry .'); intro/content verified
    'https://mcdn.podbean.com/mf/web/2i4y47/liveshow_2024_03_18_2228.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kilted-christian-ep566-royal-pains/', 'title': 'Kilted Christian Ep566: Royal Pains .', 'ep': '566', 'show': 'Kilted Christian (regular)', 'dur': 6336},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep565: Going Forward .' (was labelled '566' 'Kilted Christian Ep566: Royal Pains .'); intro/content verified
    'https://mcdn.podbean.com/mf/web/m1spyu/liveshow_2024_03_14_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kilted-christian-ep565-going-forward/', 'title': 'Kilted Christian Ep565: Going Forward .', 'ep': '565', 'show': 'Kilted Christian (regular)', 'dur': 6658},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep564:  9 gifts of the Holy Spirit.part 2' (was labelled '565' 'Kilted Christian Ep565: Going Forward .'); intro/content verified
    'https://mcdn.podbean.com/mf/web/9sq0pc/liveshow_2024_03_13_2148.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kilted-christian-ep564-9-gifts-of-the-holy-spiritpart-2/', 'title': 'Kilted Christian Ep564:  9 gifts of the Holy Spirit.part 2', 'ep': '564', 'show': 'Kilted Christian (regular)', 'dur': 4170},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep564:  9 gifts of the Holy Spirit part 1' (was labelled '564' 'Kilted Christian Ep564:  9 gifts of the Holy Spirit.part 2'); intro/content verified
    'https://mcdn.podbean.com/mf/web/d66v90/liveshow_2024_03_13_2058.mp3': {'url': 'https://kiltedchristian.podbean.com/e/kilted-christian-ep564-9-gifts-of-the-holy-spirit-part-1/', 'title': 'Kilted Christian Ep564:  9 gifts of the Holy Spirit part 1', 'ep': '564', 'show': 'Kilted Christian (regular)', 'dur': 2981},
    # transcript audio belongs to Podbean page 'Brothers and a Bible Saturday EP 127.' (was labelled '126' 'Kilted Christian Ep 126: Chris and Raccoon, survival.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/sl1acn/liveshow_2022_07_30_1856.mp3': {'title': 'Brothers and a Bible Saturday EP 127.', 'ep': '127', 'show': 'Brothers and a Bible'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep 126: Chris and Raccoon, survival.' (was labelled '125' 'Kilted Christian Ep 125: MSMLIARS Thursday.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/zhry4w/liveshow_2022_07_29_2128.mp3': {'title': 'Kilted Christian Ep 126: Chris and Raccoon, survival.', 'ep': '126', 'show': 'Raccoon nights'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep 125: MSMLIARS Thursday.' (was labelled '124' 'Kilted Christian ep 124: Brothers and a Bible with Evren.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/besgje/liveshow_2022_07_28_2128.mp3': {'title': 'Kilted Christian Ep 125: MSMLIARS Thursday.', 'ep': '125', 'show': 'MSMLIARS'},
    # transcript audio belongs to Podbean page 'Kilted christian Ep: 122.The Conlee.' (was labelled '123' 'Kilted Christian Ep 123: Livin and Duncan'); intro/content verified
    'https://mcdn.podbean.com/mf/web/x3qhw9/liveshow_2022_07_25_2128.mp3': {'title': 'Kilted christian Ep: 122.The Conlee.', 'ep': '122', 'show': 'The Conlee'},
    # transcript audio belongs to Podbean page 'Kilted Christian ep 124: Brothers and a Bible with Evren.' (was labelled '122' 'Kilted christian Ep: 122.The Conlee.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/1zbotb/liveshow_2022_07_27_2128.mp3': {'title': 'Kilted Christian ep 124: Brothers and a Bible with Evren.', 'ep': '124', 'show': 'Brothers and a Bible'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep 123: Livin and Duncan' (was labelled '121' 'Kilted Christian Ep 121:  Lyndon Lueders and Officer Jody.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/1zdmns/liveshow_2022_07_26_2128.mp3': {'title': 'Kilted Christian Ep 123: Livin and Duncan', 'ep': '123', 'show': 'Livin and Duncan'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep 121:  Lyndon Lueders and Officer Jody.' (was labelled '120' 'Kilted Christian Ep 120: Brothers Sisters and a Bible.'); intro/content verified
    'https://mcdn.podbean.com/mf/web/zaic7y/liveshow_2022_07_22_2128.mp3': {'title': 'Kilted Christian Ep 121:  Lyndon Lueders and Officer Jody.', 'ep': '121', 'show': 'Guest interview (Kilted Christian)'},
    # transcript audio belongs to Podbean page 'kilted christian ep 31:  know your enemy' (was labelled '30' 'Kilted Christian Ep 30: Connecting the Dots, Save the Children'); intro/content verified
    'https://mcdn.podbean.com/mf/web/2bxl9j/liveshow_202203112128.mp3': {'title': 'kilted christian ep 31:  know your enemy', 'ep': '31', 'show': 'Kilted Christian (regular)'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep 30: Connecting the Dots, Save the Children' (was labelled '' 'liveshow_202203102128'); intro/content verified
    'https://mcdn.podbean.com/mf/web/vsag0a/liveshow_202203102128.mp3': {'title': 'Kilted Christian Ep 30: Connecting the Dots, Save the Children', 'ep': '30', 'show': 'Kilted Christian (regular)'},
    # transcript audio belongs to Podbean page 'Kilted Christian Ep 120: Brothers Sisters and a Bible.' (was labelled '120 (untitled; intro says Ep 120)' 'liveshow_2022_07_21_2128'); intro/content verified
    'https://mcdn.podbean.com/mf/web/p44bsv/liveshow_2022_07_21_2128.mp3': {'title': 'Kilted Christian Ep 120: Brothers Sisters and a Bible.', 'ep': '120', 'show': 'Brothers and a Bible'},
    # transcript audio belongs to Podbean page 'kilted christian ep 151:  The Conlee.' (was labelled '151 (untitled; from intro)' 'liveshow_2022_08_29_2128'); intro/content verified
    'https://mcdn.podbean.com/mf/web/osgrsu/liveshow_2022_08_29_2128.mp3': {'title': 'kilted christian ep 151:  The Conlee.', 'ep': '151', 'show': 'The Conlee'},
    # teaching episode on Jesus in the Old Testament (music talk is only a plug for the next night's music show); was tagged Music night
    'https://mcdn.podbean.com/mf/web/xgxa5bk2akkxkg7q/KC_Ep_1093_Jesus_in_the_Old_testamentb5f7j.mp3': {'show': 'Kilted Christian (regular)'},
    # no date in source; Podbean page datePublished 2025-06-25
    'https://mcdn.podbean.com/mf/web/vaah8pvrssukhgd8/KC_884ao4k8.mp3': {'date': '2025-06-25'},
    # Podbean title has no number; Book of Heaven recorded Mon Apr 6 2026 between Ep 1060 (Apr 3) and Ep 1062 (Apr 7), so Ep 1061
    'https://mcdn.podbean.com/mf/web/pftlr4l2hot3oj42/liveshow_2026_04_06_2058.mp3': {'ep': '1061'},
    # second recording also titled Ep863 on Podbean, but it is a different show (news and Revelation talk, no Romans study); possibly Ep 864, which has no page on Podbean
    'https://mcdn.podbean.com/mf/web/los1f8pgpzrejcxd/liveshow_2025_05_27_2058.mp3': {'title': 'KC Ep863: Book of Heaven. (May 27 upload, separate show)', 'show': 'Kilted Christian (regular)'},
    # two different recordings are both titled Ep863 on Podbean; this one is the Memorial Day Book of Heaven (Romans study)
    'https://mcdn.podbean.com/mf/web/gr4bz83me7gndag1/liveshow_2025_05_26_2100.mp3': {'title': 'KC Ep863: Book of Heaven. (May 26, Memorial Day)'},
}

# Transcript name/term corrections (Nov 16, 2026 audit). Applied to the published copy of each transcript
# (site/t/*.txt.gz) and to the search index; the source transcripts are not modified. Only unambiguous
# speech-to-text errors are fixed (non-words or show names); each rule was checked against samples in context.
def _calvary(m, text):
    w=text[max(0,m.start()-160):m.end()+160].lower()
    if re.search(r'alberta|g7|stampede|university|flames|canad|quebec|sidewalk|bangkok|independence|summit', w): return m.group(0)
    return 'Calvary' if re.search(r'cross|crucif|christ|jesus|blood|golgotha|hill', w) else m.group(0)
TRANSCRIPT_FIXES=[
    # (label, regex, replacement, flags)
    ('show name: Kilted Christian (non-word variants)', r"\b(?:Kilt (?:the|of|to)|Kylton|Kylta|Kilton|Kilter|Kilda|Keltik)\s+Christian\b", 'Kilted Christian', re.I),
    ('show name: Kilted Christian (before episode/show/family)', r"\b(?:killed (?:the|to)|kill (?:the|to)|skilled to|tilted|guilty)\s+Christian(?=,?\s+(?:episode|show|family|studio|podcast)\b)", 'Kilted Christian', re.I),
    ('show name: Kilted Christian (after this is/welcome to/joining)', r"\b(this is|welcome (?:back )?to|joining(?: us)?(?: for| on)?) (?:killed (?:the|to)|kill (?:the|to))\s+Christian\b", r'\1 Kilted Christian', re.I),
    ('show name: Brothers and a Bible', r"\bBrothers in a Bible\b", 'Brothers and a Bible', re.I),
    ('show name: MSM Liars', r"\bMSN Liars\b", 'MSM Liars', re.I),
    ('show name: Godcast', r"\b(official|the) God ?cast\b(?!\s+(?:out|down|away|them|him|her|it|us|me|into|his|their|upon|off|forth|lots?)\b)", r'\1 Godcast', re.I),
    ('show name: Godcast (God gas)', r"\bGod gas\b", 'Godcast', re.I),
    ('show name: Livin and Duncan', r"\bLiving and Duncan\b", 'Livin and Duncan', re.I),
    ('show name: Pains Angels', r"\b(?:Payne'?s|Pain's) Angels\b", 'Pains Angels', re.I),
    ('name: Evren', r"\b(?:Everon|Everyn|Evron|Evran)\b", 'Evren', re.I),
    ('name: Dustin Nemos', r"\bDustin Nem(?:o's|us)\b", 'Dustin Nemos', re.I),
    ('name: Podbean', r"\b(?:pod ?bean|pod ?beam|pot ?bean|paw ?bea[nm]|pa ?bean|pahbeam)\b", 'Podbean', re.I),
    ("name: Podbean's", r"\b(?:pod|pot) ?beans(?= (?:been|got|gonna|going|just|done|having|has)\b)", "Podbean's", re.I),
    ('name: Podbean (plural form)', r"\b(?:pod|pot) ?beams?\b|\b(?:pod|pot) ?beans\b", 'Podbean', re.I),
    ('name: Bards FM', r"\b(?:bard's|bards|bars|bar's|barge) ?f\.? ?m\b", 'Bards FM', re.I),
    ('name: Bards Fest', r"\bbars fest\b", 'Bards Fest', re.I),
    ('Bible: Ephesians', r"\baphesians\b", 'Ephesians', re.I),
    ('Bible: Corinthians', r"\b(?:carinthians|chrithians)\b", 'Corinthians', re.I),
    ('Bible: Isaiah', r"\b(?:isaia|isaah)\b", 'Isaiah', re.I),
    ('Bible: Ezekiel', r"\ba zekiel\b", 'Ezekiel', re.I),
    ('Bible: Belshazzar', r"\bbelchazar\b", 'Belshazzar', re.I),
    ('Bible: Enoch', r"\benoc\b", 'Enoch', re.I),
    ('Bible: Golgotha', r"\bgalgotha\b", 'Golgotha', re.I),
    ('Bible: Babylon', r"\bbab[ae]lon\b", 'Babylon', re.I),
    ('Bible: Babylonian', r"\bbabelonian\b", 'Babylonian', re.I),
    ('Bible: Shamgar', r"\bshamkar\b", 'Shamgar', re.I),
    ('Bible: Jehovah', r"\bjahovah\b", 'Jehovah', re.I),
    ('Bible: Lazarus', r"\blazareth\b", 'Lazarus', re.I),
    ('Bible: Calvary (only beside cross/crucifixion/Christ, never the Canadian city)', r"\bCalgary\b", _calvary, re.I),
    ('name: Khazarian', r"\bkazarian(s?)\b", r'Khazarian\1', re.I),
    ('name: Khazaria', r"\bkazaria\b", 'Khazaria', re.I),
    ('name: Epstein', r"\b(?:ebstein|eppstein|edstein)\b", 'Epstein', re.I),
    ('name: Rothschild', r"\brothchild(s?)\b", r'Rothschild\1', re.I),
    ('name: Rockefeller', r"\brockerfeller\b", 'Rockefeller', re.I),
    ('place: Scotland', r"\bscottland\b", 'Scotland', re.I),
    ('place: Scottish', r"\bscotish\b", 'Scottish', re.I),
    ('place: Culloden', r"\bcolloden\b", 'Culloden', re.I),
]
_TF=[(lab,re.compile(p,fl),rep) for lab,p,rep,fl in TRANSCRIPT_FIXES]
FIX_STATS=collections.Counter()
def fix_text(text):
    for lab,rx,rep in _TF:
        if callable(rep):
            out=[];last=0;n=0
            for m in rx.finditer(text):
                r=rep(m,text)
                if r!=m.group(0): out.append(text[last:m.start()]); out.append(r); last=m.end(); n+=1
            out.append(text[last:]); text=''.join(out)
        else:
            cnt=[0]
            def _sub(m,rep=rep,cnt=cnt):
                new=m.expand(rep)
                if new!=m.group(0): cnt[0]+=1
                return new
            text=rx.sub(_sub,text); n=cnt[0]
        FIX_STATS[lab]+=n
    return text

# Speech-to-text loop cleanup (Nov 16, 2026 audit): Whisper sometimes gets stuck and emits the same line
# dozens or thousands of times (e.g. "I" x2337) while the real speech in that stretch is lost. Runs of 15+
# identical consecutive lines are collapsed to one line plus a visible note, so they don't flood the reader
# or inflate search counts. Nothing real is removed: those lines are artifacts, not speech.
LOOP_MIN=15
# Loops that sit on a song being played (confirmed by re-transcribing just that clip, Nov 16, 2026):
# the speech-to-text cannot follow the music, so say so instead of "speech missing".
LOOP_NOTES={
    ('1094','00:34:02'): '[Song playing here ("The Safety Dance", per the host right after); the lyrics could not be transcribed reliably.]',
    ('1004','00:18:31'): '[A worship song is playing here ("Will you ride with me"); the lyrics could not be transcribed reliably.]',
}
LOOP_STATS=[]
_LINE=re.compile(r'^\[(\d\d:\d\d:\d\d)\]\s*(.*)$')
def collapse_loops(text, label=''):
    lines=text.split('\n'); out=[]; i=0
    while i<len(lines):
        m=_LINE.match(lines[i]); j=i+1
        if m and m.group(2).strip():
            key=m.group(2).strip()
            while j<len(lines):
                mj=_LINE.match(lines[j])
                if mj and mj.group(2).strip()==key: j+=1
                else: break
        if j-i>=LOOP_MIN:
            last=_LINE.match(lines[j-1]).group(1)
            out.append(lines[i])
            note=LOOP_NOTES.get((label.split()[1] if label else '', m.group(1)))
            out.append(f'[{last}] '+(note or f'[Transcription glitch: the line above repeated {j-i} times from {m.group(1)} to {last}; the speech in that stretch is missing from this transcript.]'))
            LOOP_STATS.append((label,m.group(1),last,j-i,key[:40]))
        else: out.extend(lines[i:j])
        i=j
    return '\n'.join(out)
# Search aliases: the co-host's name is "The Conlee" in titles but is heard/transcribed as Conley or Connelly
# (his surname may genuinely be Conley), so the text is left alone and searching "conlee" also finds those.
SEARCH_ALIASES={'conlee':['conley','connelly']}
ALIAS_OF={v:k for k,vs in SEARCH_ALIASES.items() for v in vs}
rows=list(csv.DictReader(open(SRC_CSV)))
docs=[]; post=collections.defaultdict(list); bpost=collections.defaultdict(list); gaps=[]
for _d in ('t','idx','bi'): shutil.rmtree(f'{OUT}/{_d}',ignore_errors=True)  # build outputs only
os.makedirs(OUT+'/t',exist_ok=True); os.makedirs(OUT+'/idx',exist_ok=True); os.makedirs(OUT+'/bi',exist_ok=True)
def sortkey(x): return (x['date'] or '0000', int(x['ep']) if x['ep'].isdigit() else 0)
rows=[r for r in rows if r['has_transcript']=='yes']
for r in rows:
    o=EPISODE_FIXES.get(r['audio_url'])
    if o:
        for k in ('ep','title','show','date'):
            if k in o: r[k]=o[k]
        if 'url' in o: r['_url']=o['url']
        if 'dur' in o: r['_dur']=o['dur']
rows.sort(key=sortkey, reverse=True)
for i,r in enumerate(rows):
    base=r['transcript'][:-5]
    m=json.load(open(base+'.meta.json'))
    text=collapse_loops(fix_text(open(base+'.txt',encoding='utf-8').read()), f"Ep {r['ep']} {r['title'].strip()}")
    with open(f'{OUT}/t/{i}.txt.gz','wb') as raw, gzip.GzipFile(fileobj=raw,mode='wb',compresslevel=9,mtime=0) as f: f.write(text.encode('utf-8'))
    t=toks(text)
    ta=[ALIAS_OF.get(w,w) for w in t]
    c=collections.Counter(t)+collections.Counter(a for w,a in zip(t,ta) if a!=w)
    for w,n in c.items(): post[w].append((i,n))
    bg=collections.Counter(a+' '+b for a,b in zip(t,t[1:]))
    if ta!=t: bg+=collections.Counter(x+' '+y for (a,b),(x,y) in zip(zip(t,t[1:]),zip(ta,ta[1:])) if (a,b)!=(x,y))
    for w,n in bg.items(): bpost[w].append((i,n))
    url=r['_url'] if '_url' in r else (m.get('url') or '')
    if not url: gaps.append(f"Ep {r['ep']} ({r['title']}): no episode page URL; linked audio file instead")
    if not r['date']: gaps.append(f"Ep {r['ep']} ({r['title']}): no date")
    docs.append({'id':i,'ep':r['ep'],'show':r['show'],'title':TITLE_FIXES.get((r['ep'],r['title'].strip()),r['title'].strip()),'date':r['date'],
                 'url':url,'audio':m.get('audio_url') or r['audio_url'],'words':len(t),'dur':r.get('_dur') or m.get('duration')})
# shard by prefix, adaptive: split any shard over LIMIT by a longer prefix
LIMIT=400_000
def emit(P,words):
    d={}
    for w in sorted(words):
        flat=[]; prev=0
        for i,n in P[w]: flat+=[i-prev,n]; prev=i
        d[w]=flat
    return json.dumps(d,separators=(',',':'),ensure_ascii=False)
def shard(P,words,n,out):
    g=collections.defaultdict(list)
    for w in words: g[w[:n]].append(w)
    for k,ws in g.items():
        s=emit(P,ws)
        if len(s)>LIMIT and any(len(w)>n for w in ws) and len(ws)>1:
            exact=[w for w in ws if len(w)<=n]; longer=[w for w in ws if len(w)>n]
            if exact: out[k+'\u0000']=emit(P,exact)
            shard(P,longer,n+1,out)
        else: out[k]=s
def write(P,sub,prefix):
    out={}; shard(P,list(P),2,out); names={}
    for n,(k,s) in enumerate(sorted(out.items())):
        fn=f'{prefix}{n}.json'; names[k]=fn
        open(f'{OUT}/{sub}/{fn}','w',encoding='utf-8').write(s)
    print(sub,'shards',len(out),'max',max(len(s) for s in out.values()),'bytes',sum(len(s.encode()) for s in out.values()))
    return names
names=write(post,'idx','s'); bnames=write(bpost,'bi','b')
total_words=sum(d['words'] for d in docs)
json.dump({'docs':docs,'aliases':SEARCH_ALIASES,'shards':names,'bshards':bnames,'N':len(docs),'avgdl':total_words/len(docs),'totalWords':total_words},
          open(f'{OUT}/docs.json','w',encoding='utf-8'),separators=(',',':'),ensure_ascii=False)
json.dump(gaps,open('/workspace/kilted-christian-search/gaps.json','w'),indent=1)
print('docs',len(docs),'terms',len(post),'bigrams',len(bpost),'words',total_words)
print('\n'.join(gaps))
json.dump(dict(FIX_STATS),open('/workspace/kilted-christian-search/audit/transcript_fix_stats.json','w'),indent=1)
print('transcript fixes',dict(FIX_STATS))
json.dump(LOOP_STATS,open('/workspace/kilted-christian-search/audit/loop_stats.json','w'),indent=0,ensure_ascii=False)
print('loops collapsed',len(LOOP_STATS))
