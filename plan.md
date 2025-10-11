# Poetry Collection App - Enhanced Features Plan

## Project Overview
Building enhanced features for the poetry collection app including section tabs (Before/After the Break), preamble poem display, contextual navigation, refined reading experience, and footer elements.

---

## Phase 1: Section Tabs & Preamble Poem Display ✅
- [ ] Add "section" field support to Notion data processing (pre/post values)
- [ ] Create tab component with "Before the Break" and "After the Break" options
- [ ] Style active tab with #B7926F underline, inactive with dimmed text
- [ ] Implement smooth fade transition when switching tabs
- [ ] Filter poems by section based on active tab
- [ ] Create special highlighted preamble card for "Lost" poem at the top
- [ ] Style preamble card differently (no border, italic "preamble" subtitle)
- [ ] Add fade-in effect for preamble card on site load
- [ ] Position preamble outside/above the tabs section
- [ ] Make preamble card clickable to open in reading view

---

## Phase 2: Contextual Poem Navigation & Progress
- [ ] Add previous/next navigation arrows to poem detail pages
- [ ] Calculate previous/next poems based on Notion ordering
- [ ] Display poem titles in navigation (e.g., "← Pieces" or "Next → MTA")
- [ ] Add progress indicator showing position (e.g., "7 of 22")
- [ ] Implement crossfade transitions between poems
- [ ] Handle edge cases (first/last poem in collection)
- [ ] Respect section filtering when navigating

---

## Phase 3: Refined Poem Page & Reading Mode Enhancement
- [ ] Remove box/card background from poem content area
- [ ] Let poems float directly over gradient background
- [ ] Increase font size to 20px with 1.8 line-height for poem text
- [ ] Enhance Reading Mode icon to hide all UI elements
- [ ] Center poem vertically in Reading Mode
- [ ] Keep back navigation subtle in corner
- [ ] Add smooth transitions for Reading Mode toggle
- [ ] Test readability with new typography settings

---

## Phase 4: Footer & Closing Message
- [ ] Add minimal footer to homepage with copyright text
- [ ] Add footer to poem pages as well
- [ ] Style footer: "© Nikhil Rao — The Privilege of Boredom" centered, 50% opacity
- [ ] Implement scroll detection for last poem in collection
- [ ] Add "Thank you for staying." fade-in message on last poem scroll
- [ ] Position closing message elegantly at end of content
- [ ] Test footer visibility across different viewport sizes

---

## Current Status
Ready to begin Phase 1: Section Tabs & Preamble Poem Display