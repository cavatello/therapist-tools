#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The hero illustration, inline so the page has no image request and nothing to
break when a CDN is slow. It is drawn rather than decorative: the four risers
are the four BBS gates in the order they actually close, and the flag heights
are to scale against the 3,000."""

HERO_ART = r"""
<svg class="aart" viewBox="0 0 520 300" role="img"
     aria-label="A staircase of four steps rising to 3,000 supervised hours, with the 500 relational-hours step marked as the one most associates finish last.">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#0F2A20"/><stop offset="1" stop-color="#17392C"/>
    </linearGradient>
    <linearGradient id="riser" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#4FB08C"/><stop offset="1" stop-color="#2C6350"/>
    </linearGradient>
    <linearGradient id="riserlast" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#F6C560"/><stop offset="1" stop-color="#B08430"/>
    </linearGradient>
  </defs>
  <rect width="520" height="300" rx="12" fill="url(#sky)"/>
  <g opacity=".13" stroke="#8FD9B6" stroke-width="1">
    <path d="M0 60h520M0 110h520M0 160h520M0 210h520M0 260h520"/>
  </g>

  <!-- the four gates, as risers. Heights are proportional to how far into the
       two years each one typically closes, not to the hour counts, which are
       on different scales and would draw a misleading picture. -->
  <g>
    <rect x="44"  y="212" width="92" height="56"  rx="7" fill="url(#riser)"/>
    <rect x="146" y="176" width="92" height="92"  rx="7" fill="url(#riser)"/>
    <rect x="248" y="140" width="92" height="128" rx="7" fill="url(#riser)"/>
    <rect x="350" y="86"  width="92" height="182" rx="7" fill="url(#riserlast)"/>
  </g>

  <!-- labels sit ON the risers, so the picture survives being 260px wide -->
  <g font-family="Inter,system-ui,sans-serif" font-weight="800" fill="#fff">
    <text x="90"  y="236" font-size="17" text-anchor="middle">104</text>
    <text x="90"  y="252" font-size="8.5" text-anchor="middle" opacity=".8">WEEKS</text>
    <text x="192" y="212" font-size="17" text-anchor="middle">500</text>
    <text x="192" y="228" font-size="8.5" text-anchor="middle" opacity=".8">RELATIONAL</text>
    <text x="294" y="184" font-size="17" text-anchor="middle">1,750</text>
    <text x="294" y="200" font-size="8.5" text-anchor="middle" opacity=".8">DIRECT</text>
    <text x="396" y="132" font-size="19" fill="#2A1F08" text-anchor="middle">3,000</text>
    <text x="396" y="148" font-size="8.5" fill="#2A1F08" text-anchor="middle" opacity=".8">TOTAL</text>
  </g>

  <!-- the climber: a small figure two steps up, because that is where most
       people reading this actually are -->
  <g transform="translate(178,140)">
    <circle cx="0" cy="0" r="9" fill="#FBF9F3"/>
    <path d="M0 10v20M0 16l-11 9M0 16l11 9M0 30l-8 14M0 30l8 14" stroke="#FBF9F3"
          stroke-width="4.5" stroke-linecap="round" fill="none"/>
  </g>

  <!-- the flag at the top -->
  <g transform="translate(396,58)">
    <path d="M0 28V0" stroke="#FBF9F3" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M2 2h26l-7 8 7 8H2z" fill="#FBF9F3"/>
  </g>

  <text x="44" y="290" font-family="'IBM Plex Mono',ui-monospace,monospace" font-size="10"
        fill="#8FD9B6" opacity=".75">FOUR GATES &#183; ALL FOUR MUST CLOSE</text>
</svg>
"""
