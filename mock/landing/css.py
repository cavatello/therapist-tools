# -*- coding: utf-8 -*-
"""Landing-page CSS. Namespaced under .lp, every class prefixed l-.

The build asserts the namespace holds and that no bare rule collides with the
lifted site chrome. Four silent failures on this site came from exactly that.
"""

CSS = """
.lp{--paper:#FBF9F3;--white:#FFFFFF;--ink:#26241E;--muted:#6E695E;--line:#E7E2D6;
  --field:#FBF6E9;--fieldline:#E4D9BE;--pine:#2C6350;--pinedeep:#1F4C3C;
  --brick:#8E4B45;--gold:#B08430;--indigo:#4B3B93;--pop:#F6C560;
  --pos:#3F9577;--neg:#B5483F;
  color:var(--ink);font-family:Inter,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;background:var(--white)}
.lp *,.lp *::before,.lp *::after{box-sizing:border-box}
.lp p{margin:0 0 1em}
.lp h1,.lp h2,.lp h3{font-family:Fraunces,Georgia,serif;font-weight:700;margin:0 0 .5em;
  line-height:1.1;letter-spacing:-.014em}
.lp a{color:inherit}
.lp :focus-visible{outline:3px solid var(--gold);outline-offset:3px;border-radius:6px}

.lwrap{max-width:1120px;margin:0 auto;padding:0 24px}
.lnarrow{max-width:760px}
@media (max-width:520px){.lwrap{padding:0 18px}}

.leyebrow{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 12px}
.llede{font-size:clamp(16.5px,1.35vw,19.5px);line-height:1.62;color:var(--muted);
  max-width:62ch}

.lcta{display:inline-flex;align-items:center;gap:.5em;min-height:50px;padding:0 26px;
  border-radius:999px;background:var(--pine);color:#fff;font-weight:700;font-size:16px;
  text-decoration:none;border:0;cursor:pointer;transition:background .15s ease}
.lcta:hover{background:var(--pinedeep)}
.lcta.lgold{background:var(--pop);color:#26241E}
.lcta.lgold:hover{background:#EFB63F}
.lghost{display:inline-flex;align-items:center;min-height:50px;padding:0 22px;
  border-radius:999px;border:1.5px solid var(--line);background:transparent;
  font-weight:600;font-size:15.5px;text-decoration:none;color:var(--muted)}
.lghost:hover{border-color:var(--muted);color:var(--ink)}

/* --- hero. Deliberately NOT a calculator: the brief was that the page must
   explain itself before it does anything. --------------------------------- */
.lhero{background:linear-gradient(165deg,#2C6350 0%,#20503F 70%,#1B4536 100%);
  color:#F4F1E8;padding:clamp(48px,7vw,104px) 0 clamp(44px,6vw,88px)}
.lhero .leyebrow{color:#9FC4B4}
.lhero h1{font-size:clamp(33px,4.8vw,62px);color:#FFFDF6;max-width:19ch;
  margin-bottom:.36em}
.lhero .llede{color:#C9DED5;max-width:54ch;font-size:clamp(17px,1.5vw,21px)}
.lacts{display:flex;gap:12px;flex-wrap:wrap;margin-top:30px}
.lhero .lghost{border-color:rgba(255,255,255,.32);color:#D7E7E0}
.lhero .lghost:hover{border-color:#fff;color:#fff}
.lfor{display:flex;gap:8px 22px;flex-wrap:wrap;margin:34px 0 0;padding-top:22px;
  border-top:1px solid rgba(255,255,255,.18);font-size:14px;color:#9FC4B4}
.lfor b{color:#F4F1E8;font-weight:600}

/* --- sections ------------------------------------------------------------ */
.lsec{padding:clamp(48px,6vw,84px) 0}
.lsec.lpaper{background:var(--paper);border-top:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.lsec h2{font-size:clamp(26px,2.8vw,38px)}
.lhead{max-width:70ch;margin:0 0 34px}
.lhead .llede{margin-top:.2em}

/* THE ANSWER GRID - what replaced the "why this exists" prose.
   That block was three paragraphs about the author's motive, set in a narrow
   column with the whole right half of the page empty, and it promoted nothing.
   Same slot, spent on the reader's four questions, each one a route to the tool
   that answers it. One line of the old prose survives as the lede, because the
   "scattered, and never California-specific" point was the only part of it the
   reader had any use for. */
.lwhy .llede{font-size:clamp(15px,1.2vw,17px);line-height:1.66;max-width:64ch;
  color:var(--muted);margin:10px 0 30px}
.lans{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
@media (max-width:820px){.lans{grid-template-columns:minmax(0,1fr)}}
.lansc{display:block;background:var(--white);border:1px solid var(--line);
  border-radius:18px;padding:24px 26px 21px;text-decoration:none;color:inherit;
  border-left:3px solid var(--pine);
  transition:transform .12s,box-shadow .12s,border-color .12s}
.lansc:nth-child(2){border-left-color:var(--gold)}
.lansc:nth-child(3){border-left-color:var(--indigo)}
.lansc:nth-child(4){border-left-color:var(--brick)}
.lansc:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(38,36,30,.09)}
.lansc:focus-visible{outline:3px solid var(--pine);outline-offset:3px}
/* a <q> so the question is marked up as the reader's words, not ours. The UA
   quote marks are suppressed - the typography already reads as a question. */
.lansq{display:block;font-family:Fraunces,Georgia,serif;font-size:clamp(18px,1.55vw,21px);
  font-weight:600;letter-spacing:-.016em;line-height:1.25;quotes:none;margin:0 0 8px}
.lansb{display:block;font-size:13.6px;line-height:1.6;color:var(--muted);margin:0 0 14px}
.lansg{display:block;font-size:13.4px;font-weight:700;color:var(--pine)}
.lansc:nth-child(2) .lansg{color:#8A6318}
.lansc:nth-child(3) .lansg{color:var(--indigo)}
.lansc:nth-child(4) .lansg{color:var(--brick)}
.lansc:hover .lansg{text-decoration:underline}

.lgrid{display:grid;gap:20px}
.lg3{grid-template-columns:repeat(3,minmax(0,1fr))}
.lg2{grid-template-columns:repeat(2,minmax(0,1fr))}
@media (max-width:900px){.lg3{grid-template-columns:minmax(0,1fr)}}
@media (max-width:700px){.lg2{grid-template-columns:minmax(0,1fr)}}

.lpromise{border-top:3px solid var(--pine);padding:18px 0 0}
.lpromise:nth-child(2){border-top-color:var(--gold)}
.lpromise:nth-child(3){border-top-color:var(--indigo)}
.lpromise h3{font-size:20px;margin-bottom:.35em}
.lpromise p{font-size:15px;line-height:1.62;color:var(--muted);margin:0}

/* who this is for */
.laud{display:flex;flex-direction:column;background:var(--white);
  border:1px solid var(--line);border-radius:14px;padding:24px;text-decoration:none;
  color:inherit;transition:border-color .16s ease,box-shadow .16s ease,transform .16s ease}
.laud:hover{border-color:#CFC7B3;box-shadow:0 10px 26px rgba(38,36,30,.08);
  transform:translateY(-2px)}
.laud b{font-family:Fraunces,Georgia,serif;font-size:20px;font-weight:700;
  line-height:1.2;display:block;margin-bottom:.4em}
.laud span{font-size:15px;line-height:1.6;color:var(--muted)}
.laud em{font-style:normal;margin-top:auto;padding-top:16px;font-weight:700;
  font-size:14.5px;color:var(--pine)}

/* tools */
.ltool{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,260px);
  gap:clamp(18px,2.5vw,34px);align-items:start;background:var(--white);
  border:1px solid var(--line);border-top:3px solid var(--pine);border-radius:14px;
  padding:clamp(22px,2.6vw,30px);text-decoration:none;color:inherit;
  transition:border-color .16s ease,box-shadow .16s ease}
.ltool:hover{box-shadow:0 12px 30px rgba(38,36,30,.09)}
.ltool[data-accent="gold"]{border-top-color:var(--gold)}
.ltool[data-accent="indigo"]{border-top-color:var(--indigo)}
.ltool[data-accent="brick"]{border-top-color:var(--brick)}
@media (max-width:760px){.ltool{grid-template-columns:minmax(0,1fr)}}
.ltag{font-family:'IBM Plex Mono',monospace;font-size:10.5px;font-weight:600;
  letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.ltool h3{font-size:clamp(21px,2vw,27px);margin-bottom:.32em}
.ltool .lbody{font-size:15.5px;line-height:1.62;color:var(--muted);margin:0}
.lname{font-family:'IBM Plex Mono',monospace;font-size:11px;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase;color:var(--pine);margin:14px 0 0}
.lfig{text-align:left}
.lfig b{display:block;font-family:Fraunces,Georgia,serif;
  font-size:clamp(28px,2.8vw,36px);line-height:1;letter-spacing:-.02em}
.lfig em{display:block;font-style:normal;font-size:12.5px;color:var(--muted);
  margin-top:6px;line-height:1.45}
.lbul{list-style:none;margin:16px 0 0;padding:0}
.lbul li{position:relative;padding:6px 0 6px 18px;font-size:14px;color:var(--muted);
  border-top:1px dotted var(--line)}
.lbul li::before{content:"";position:absolute;left:1px;top:14px;width:5px;height:5px;
  border-radius:50%;background:var(--gold)}
@media (max-width:760px){.lfig{border-top:1px solid var(--line);padding-top:14px}}

/* reading */
.lread{display:block;background:var(--paper);border:1px solid var(--line);
  border-radius:14px;padding:22px;text-decoration:none;color:inherit}
.lread:hover{background:#F4F0E4}
.lread b{font-family:Fraunces,Georgia,serif;font-size:19px;font-weight:700;
  display:block;margin-bottom:.35em;line-height:1.22}
.lread span{font-size:14.5px;line-height:1.6;color:var(--muted)}

/* how it works */
.lhow{list-style:none;margin:0;padding:0;counter-reset:lh}
.lhow li{counter-increment:lh;display:grid;grid-template-columns:auto minmax(0,1fr);
  gap:16px;padding:16px 0;border-top:1px solid var(--line)}
.lhow li::before{content:counter(lh,decimal-leading-zero);
  font-family:'IBM Plex Mono',monospace;font-size:12px;font-weight:600;
  color:var(--gold);padding-top:4px}
.lhow b{display:block;font-size:16px;margin-bottom:3px}
.lhow span{font-size:14.8px;line-height:1.6;color:var(--muted)}

/* about + disclaimer */
.labout{max-width:66ch}
.labout p{font-size:16.5px;line-height:1.66}
.lnote{margin-top:20px;padding:16px 18px;background:var(--paper);
  border-left:3px solid var(--fieldline);border-radius:0 10px 10px 0;
  font-size:14px;line-height:1.6;color:var(--muted)}

/* newsletter */
.lnews{background:var(--paper);border-top:1px solid var(--line);padding:44px 0}
.lnewsrow{display:flex;gap:12px;flex-wrap:wrap;align-items:center;margin-top:16px}
.lnews input[type=email]{flex:1 1 260px;min-height:50px;padding:0 16px;
  border:1.5px solid var(--fieldline);background:var(--field);border-radius:10px;
  font:inherit;font-size:16px;color:var(--ink)}
.lconsent{display:flex;gap:10px;align-items:flex-start;margin-top:14px;font-size:13.5px;
  color:var(--muted);line-height:1.5;max-width:64ch}
.lconsent input{margin-top:2px;width:18px;height:18px;flex:0 0 auto}

/* ============================ HERO VARIANTS ============================
   Same page below the fold in all three; only the hero changes. AIDA is the
   frame: ATTENTION is the h1, INTEREST is the deck plus the three proof
   figures, DESIRE is the who-this-is-for strip, ACTION is one primary CTA and
   at most one secondary. Nothing above the fold asks the reader to type. */

/* --- A. Calm authority. Pine, generous, the site explaining itself. ------ */
.lheroA{background:linear-gradient(165deg,#2C6350 0%,#20503F 70%,#1B4536 100%);
  color:#F4F1E8;padding:clamp(46px,6.5vw,96px) 0 clamp(40px,5vw,72px)}
.lheroA .leyebrow{color:#9FC4B4}
.lheroA h1{font-size:clamp(32px,4.6vw,58px);color:#FFFDF6;max-width:20ch;margin-bottom:.32em}
.lheroA .ldeck{color:#C9DED5;max-width:56ch;font-size:clamp(17px,1.5vw,20.5px);
  line-height:1.58}
.lheroA .lproof{border-color:rgba(255,255,255,.18)}
.lheroA .lproof b{color:#F6C560}
.lheroA .lproof em{color:#9FC4B4}
.lheroA .lghost{border-color:rgba(255,255,255,.32);color:#D7E7E0}
.lheroA .lghost:hover{border-color:#fff;color:#fff}

/* --- B. The bold chapter. Carries the purple slab energy from the old
       "bonus level" hero, which is the most striking thing this site has. --- */
.lheroB{background:#2B2150;color:#EFEAFA;padding:clamp(48px,7vw,104px) 0 clamp(44px,6vw,84px);
  position:relative;overflow:hidden}
.lheroB::before{content:"";position:absolute;inset:0;opacity:.5;
  background:repeating-linear-gradient(115deg,transparent 0 22px,rgba(255,255,255,.028) 22px 44px)}
.lheroB > *{position:relative}
.lheroB .leyebrow{color:#F6C560;border:1px solid rgba(246,197,96,.45);border-radius:999px;
  display:inline-block;padding:6px 13px;margin-bottom:20px}
.lheroB h1{font-size:clamp(34px,5.4vw,70px);color:#FFFDF6;max-width:17ch;
  margin-bottom:.3em;letter-spacing:-.022em}
.lheroB h1 em{font-style:normal;color:#F6C560}
.lheroB .ldeck{color:#C4BBE4;max-width:56ch;font-size:clamp(17px,1.5vw,21px);line-height:1.56}
.lheroB .lproof{border-color:rgba(255,255,255,.16)}
.lheroB .lproof b{color:#F6C560}
.lheroB .lproof em{color:#A79ACB}
.lheroB .lcta{background:#F6C560;color:#241B44;box-shadow:0 3px 0 rgba(0,0,0,.35)}
.lheroB .lcta:hover{background:#FFD37A}
.lheroB .lghost{border-color:rgba(255,255,255,.26);color:#C4BBE4}
.lheroB .lghost:hover{border-color:#fff;color:#fff}

/* --- D. Light hero, coloured panel. THE ONE THAT SHIPS. -----------------
   Three measured defects in the hero that preceded it, taken at real usable
   heights with browser chrome subtracted:

     every desktop width   the h1 used 43% of the column. 644px of dead space
                           to the right of it on a 1440 screen, carrying nothing.
     laptop 1440x780       the proof figures were cut off at the fold.
     laptop 1280x700       they were below it entirely.
     phone 375x600         THE CTA WAS BELOW THE FOLD.

   The fix is structural, not cosmetic: two columns from 900px up, so the dead
   space carries the proof panel - which also lifts a figure above the fold on
   every laptop. Colour is the second decision and was made separately: paper
   ground, ink type, and the colour concentrated in the panel, so the hero
   matches the rest of the site instead of announcing itself. */
.lheroD{background:var(--paper);color:var(--ink);
  padding:clamp(34px,4.4vw,62px) 0 clamp(30px,3.8vw,54px);
  border-bottom:1px solid var(--line)}
.lhd{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(300px,.95fr);
  gap:clamp(26px,4vw,60px);align-items:center}
@media (max-width:900px){.lhd{grid-template-columns:minmax(0,1fr);gap:24px}}
.lheroD .leyebrow{color:var(--muted)}
/* 15ch wrapped this to five lines in a column that is 60% of the grid, leaving
   a gap between the h1 and the panel. 19ch fills the column it was given. */
.lheroD h1{font-size:clamp(29px,3.6vw,46px);max-width:19ch;margin-bottom:.3em;
  letter-spacing:-.022em}
/* the highlight carries the hook that the dark background used to carry */
.lheroD h1 em{font-style:normal;color:var(--pine);
  background:linear-gradient(transparent 62%,#F6C56055 62%)}
.lheroD .ldeck{color:#3A362E;max-width:44ch;font-size:clamp(15.5px,1.25vw,18px);
  line-height:1.55;margin-bottom:22px}
.lheroD .lcta{background:var(--pine);color:#fff}
.lheroD .lcta:hover{background:#245244}
.lheroD .lghost{border-color:var(--line);color:var(--ink);background:var(--white)}
.lheroD .lghost:hover{border-color:var(--pine);color:var(--pine)}
/* display:block, explicitly. The base .lwho is a flex row, which made every <b>
   a flex item and every bare comma an anonymous one - so the commas floated off
   the words they belong to. It is a sentence; let it set as a sentence. */
.lheroD .lwho{display:block;color:var(--muted);margin:18px 0 0;font-size:13px;
  line-height:1.6;max-width:34em}
.lheroD .lwho b{color:var(--ink);font-weight:600}

/* the panel. Every figure in it is the engine's own output for one stated
   scenario, named in the header line - not an illustrative round number. */
.lhdp{background:var(--pinedeep);border-radius:16px;padding:20px 24px 22px;color:#DCEAE3}
.lhdph{font-family:'IBM Plex Mono',monospace;font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:#8FBBA8;margin:0 0 6px;
  padding-bottom:12px;border-bottom:1px solid rgba(255,255,255,.16)}
.lhdr{display:flex;align-items:baseline;justify-content:space-between;gap:14px;
  padding:11px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.lhdr:last-child{border-bottom:0;padding-bottom:0}
.lhdr .lhdlab{font-size:13.4px;font-weight:600;color:#F4F1E8}
.lhdr .lhdval{text-align:right}
.lhdr b{display:block;font-family:Fraunces,Georgia,serif;font-weight:600;
  font-size:clamp(22px,2.1vw,28px);line-height:1;color:var(--pop);white-space:nowrap}
.lhdr em{display:block;font-style:normal;font-size:12.4px;line-height:1.4;color:#9FC4B4}
/* the "Nothing saved / no account / 2026 rates" bar is GONE. Two of its three
   facts were already in the deck and the audience line directly above it, and
   it spent a full-width row restating them. The one fact that was not said
   twice - 2026 rates - moved into the eyebrow. */

/* 375x600 was the last failure: stacked, the panel pushed the CTA 35px past the
   fold. Three mobile-only changes - a smaller h1, a tighter rhythm, and the
   panel promoted ABOVE the audience line showing ONE figure, because a number
   earns that space and a list of licence types does not. */
@media (max-width:560px){
  /* 375x600 measured: the masthead alone eats 173px of the 600, which left the
     CTA 19px past the fold. Reclaimed from padding and rhythm, not from the
     content - nothing above the fold is dropped. */
  .lheroD{padding-top:16px}
  .lhd{display:flex;flex-direction:column;gap:12px}
  .lheroD h1{font-size:26px;line-height:1.08;max-width:none}
  .lheroD .ldeck{font-size:15px;line-height:1.5;margin-bottom:12px}
  .lheroD .lacts{margin-top:0}
  .lheroD .leyebrow{margin-bottom:8px}
  .lhdp{order:-1;padding:14px 16px}
  .lhdph{font-size:9.6px;padding-bottom:9px}
  /* stacked side-by-side the label wrapped to two lines and the caption to two
     more, making one row 140px tall. Stack it and it fits in a third of that. */
  .lhdr{display:block;padding:8px 0 0;border-bottom:0}
  .lhdr .lhdval,.lhdr em{text-align:left}
  .lhdr b{font-size:20px;margin:2px 0}
  .lhdr:nth-of-type(n+2){display:none}
  .lheroD .lwho{margin-top:14px;font-size:12.2px}
}

/* --- C. Recognition first. Opens on the reader's own sentence, on paper,
       and only then says what this is. Quietest, most disarming. --------- */
.lheroC{background:var(--paper);color:var(--ink);
  padding:clamp(44px,6vw,88px) 0 clamp(38px,5vw,68px);
  border-bottom:1px solid var(--line)}
.lheroC .lquote{font-family:Fraunces,Georgia,serif;font-size:clamp(24px,3.4vw,44px);
  font-weight:400;font-style:italic;line-height:1.24;color:#4A453B;max-width:22ch;
  margin:0 0 26px;padding-left:20px;border-left:4px solid var(--pop)}
.lheroC h1{font-size:clamp(26px,2.9vw,38px);max-width:24ch}
.lheroC .ldeck{max-width:58ch;font-size:clamp(16.5px,1.4vw,19px);line-height:1.62;
  color:var(--muted)}
.lheroC .lproof b{color:var(--pine)}

/* shared inside every hero */
.ldeck{margin:0 0 4px}
.lproof{display:flex;gap:clamp(18px,3vw,44px);flex-wrap:wrap;margin:30px 0 0;
  padding-top:22px;border-top:1px solid var(--line)}
.lproof div{min-width:0}
.lproof b{display:block;font-family:Fraunces,Georgia,serif;
  font-size:clamp(24px,2.4vw,32px);line-height:1;letter-spacing:-.02em}
.lproof em{display:block;font-style:normal;font-size:12.5px;margin-top:6px;
  color:var(--muted);max-width:22ch;line-height:1.45}
.lwho{display:flex;gap:8px 20px;flex-wrap:wrap;margin:26px 0 0;font-size:14px;
  color:var(--muted)}
.lwho b{color:var(--ink);font-weight:600}

/* .lwho and .lproof em inherit --muted, which is a LIGHT-theme token. On the two
   dark heroes that renders grey-brown on deep purple / deep pine and effectively
   disappears - it looked fine in the markup and was invisible on screen. Every
   dark hero has to restate every inherited colour it uses. */
.lheroA .lwho{color:#9FC4B4}
.lheroA .lwho b{color:#F4F1E8}
.lheroB .lwho{color:#A79ACB}
.lheroB .lwho b{color:#EFEAFA}
.lheroB .lproof em,.lheroA .lproof em{opacity:1}
.lwho{margin-top:22px}
/* the bold h1 was eating the whole fold at 900px, pushing the three proof
   figures - the interest half of AIDA - below it */
.lheroB h1{font-size:clamp(32px,4.4vw,56px)}

/* ================= BLOCKS THAT PROMOTE OTHER BLOCKS =================
   Help Scout's most useful habit: no section is a dead end. Every heading gets
   a link to all of it, every card says what KIND of thing it is, and every tool
   ends by handing the reader the piece of reading that pairs with it. */
.lkick{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;
  flex-wrap:wrap;margin:0 0 26px}
.lkick > div{max-width:60ch}
.lkick h2{margin:0}
.lkick .llede{margin:.4em 0 0}
/* A standalone link is a tap target, not prose - 21px high was the whole
   control. The underline is drawn on an inner span so the box can be 44px
   without a rule floating below the text. */
.lkicka{flex:none;display:inline-flex;align-items:center;min-height:44px;
  padding:0 2px;font-weight:700;font-size:14.5px;color:var(--pine);
  text-decoration:none}
.lkicka > span{border-bottom:2px solid transparent;padding-bottom:2px}
.lkicka:hover > span{border-bottom-color:var(--pine)}

/* the category chip. One word, mono, so a grid can be scanned by type. */
.lkind{display:inline-block;font-family:'IBM Plex Mono',monospace;font-size:9.5px;
  font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--pine);
  border:1px solid #CFE0D8;background:#F1F7F4;border-radius:999px;padding:4px 9px;
  margin:0 0 12px}
.lkind[data-kind="notes"]{color:var(--gold);border-color:#EBDCBF;background:#FBF6E9}
.lkind[data-kind="ref"]{color:var(--indigo);border-color:#D8D2EE;background:#F3F1FB}
.lkind[data-kind="guide"]{color:var(--brick);border-color:#EBD5D3;background:#FBF2F1}

/* the pair foot: what to read after this tool */
.lpair{display:flex;gap:12px;align-items:flex-start;margin:18px 0 0;padding:14px 0 0;
  border-top:1px dashed var(--line);text-decoration:none;color:inherit}
.lpair i{font-style:normal;flex:none;color:var(--gold);font-size:15px;line-height:1.4}
.lpair b{display:block;font-size:14.5px;font-weight:700;line-height:1.35;
  margin-bottom:2px}
.lpair span{display:block;font-size:13.2px;line-height:1.5;color:var(--muted)}
.lpair:hover b{text-decoration:underline}

/* the mid-page band - the second of the three binary CTAs */
.lmid{background:#20503F;color:#F4F1E8;padding:clamp(38px,5vw,64px) 0}
.lmid .leyebrow{color:#9FC4B4}
.lmid h2{color:#FFFDF6;max-width:22ch;font-size:clamp(24px,2.6vw,34px)}
.lmid p{color:#C9DED5;max-width:56ch;font-size:16px;line-height:1.6}
.lmid .lghost{border-color:rgba(255,255,255,.32);color:#D7E7E0}
.lmid .lghost:hover{border-color:#fff;color:#fff}
.lmid .lcta{background:var(--pop);color:#1B4536}
.lmid .lcta:hover{background:#FFD37A}

/* the named hub */
.lkit{border:1px solid var(--line);border-top:4px solid var(--gold);border-radius:16px;
  background:var(--white);padding:clamp(24px,3vw,36px)}
.lkit h2{font-size:clamp(24px,2.6vw,34px);margin-bottom:.28em}
.lkit > p{font-size:16.5px;line-height:1.62;color:var(--muted);max-width:62ch}
.lkitrows{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;
  margin:24px 0 22px;border-top:1px solid var(--line)}
@media (max-width:820px){.lkitrows{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.lkitrows{grid-template-columns:minmax(0,1fr)}}
.lkitrows div{padding:14px 16px 14px 0;border-bottom:1px solid var(--line)}
.lkitrows b{display:block;font-family:Fraunces,Georgia,serif;font-size:17px;
  margin-bottom:3px}
.lkitrows span{font-size:13.4px;line-height:1.5;color:var(--muted)}
"""
