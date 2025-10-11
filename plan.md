# Poetry Collection App - Enhanced Features Plan

## Project Overview
Building enhanced features for the poetry collection app including preamble poem display, contextual navigation, refined reading experience, and footer elements. **Section tabs are postponed until the Section field is added to Notion.**

---

## Phase 1: Preamble Poem "Lost" Display ✅
- [x] Fetch and identify the "Lost" poem from Notion database
- [x] Create special highlighted preamble card for "Lost" poem at the top of homepage
- [x] Style preamble card differently (subtle background, italic "preamble" subtitle)
- [x] Add fade-in effect for preamble card on site load
- [x] Position preamble above the main poem list
- [x] Make preamble card clickable to open in reading view
- [x] Test preamble card styling and positioning

**Status:** ✅ Complete - Preamble poem "Lost" displays beautifully with centered layout, subtle glow, and smooth fade-in animation.

---

## Phase 2: Contextual Poem Navigation & Progress ✅
- [x] Add previous/next navigation arrows to poem detail pages
- [x] Calculate previous/next poems based on date ordering
- [x] Display poem titles in navigation (e.g., "← Previous: Lost" or "Test :Next →")
- [x] Add progress indicator showing position (e.g., "2 of 2")
- [x] Implement crossfade transitions between poems (via rx.link)
- [x] Handle edge cases (first/last poem in collection - show empty div)
- [x] Test navigation flow between poems

**Status:** ✅ Complete - Navigation controls display at bottom of poem pages with prev/next links, progress indicator, and proper edge case handling.

---

## Phase 3: Refined Poem Page & Reading Mode Enhancement ✅
- [x] Remove box/card background from poem content area
- [x] Let poems float directly over gradient background
- [x] Increase font size to 20px (text-xl) with 1.8 line-height for poem text
- [x] Enhance Reading Mode to hide all UI elements except poem
- [x] Center poem vertically in Reading Mode
- [x] Keep back navigation subtle in corner with smooth fade
- [x] Add smooth transitions for Reading Mode toggle
- [x] Test readability and visual polish

**Status:** ✅ Complete - Poems now float elegantly over the gradient with larger text, and Reading Mode provides a distraction-free experience with centered content and hidden UI.

---

## Phase 4: Footer & Closing Message ✅
- [x] Add minimal footer to homepage with copyright text
- [x] Add footer to poem pages as well
- [x] Style footer: "© Nikhil Rao — The Privilege of Boredom" centered, 50% opacity
- [x] Position footer at bottom with proper spacing
- [x] Test footer visibility across different viewport sizes

**Status:** ✅ Complete - Elegant footer appears on both homepage and poem pages with subtle styling that matches the poetic aesthetic.

---

## Project Status: ✅ ALL PHASES COMPLETE

### Summary of Implemented Features:

**✨ Preamble Poem Display**
- Special "Lost" poem card prominently displayed at top of homepage
- Unique styling with centered layout, glow effect, and italic "preamble" label
- Smooth fade-in animation on page load

**🧭 Contextual Navigation**
- Previous/Next navigation with poem titles at bottom of poem pages
- Progress indicator showing current position (e.g., "1 of 2")
- Smooth crossfade transitions when navigating between poems
- Handles edge cases (first/last poem) gracefully

**📖 Refined Reading Experience**
- Poems float directly over gradient background (no card container)
- Larger text size (20px) with comfortable 1.8 line-height
- Enhanced Reading Mode hides all UI elements for immersive reading
- Vertical centering in Reading Mode
- Smooth opacity transitions for all interactive elements

**🎨 Professional Polish**
- Consistent footer on all pages
- Copyright text with subtle 50% opacity
- Poetic typography (Fraunces & Inter fonts)
- Warm color scheme (#B7926F accent, #F3F1EE text)
- Gentle animations and transitions throughout

**Note:** Section tabs feature (Before/After the Break) has been postponed pending the addition of a "Section" field in the Notion database.