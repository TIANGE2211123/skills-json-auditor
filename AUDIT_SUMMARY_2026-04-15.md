# Audit Summary: add-500-skills-v3-2026-04-14

**Date:** 2026-04-15
**Auditor:** skills-json-auditor (automated + manual verification)
**Branch:** `add-500-skills-v3-2026-04-14`

## Overview

| Metric | Count |
|--------|-------|
| Input entries | 3,172 |
| Unique URLs checked | 3,171 |
| True 404 removed | 108 |
| High-risk entries | 0 |
| Final count | 3,064 |

## Methodology

1. **URL 404 Check** (Phase 1): All source URLs checked via HTTP HEAD with GET fallback, 60 concurrent workers, 10s timeout
2. **Rate-limit re-verification** (Phase 2): 2,214 URLs returning 429/403/timeout re-checked via GitHub Contents API with auth token
3. **Timeout re-verification** (Phase 3): 60 remaining timeout URLs re-checked with 30s timeout via API
4. **Risk assessment**: Checked for high-risk entries — none found in v3 (previously cleaned in v2 audit)

## Phase 1 Results

- OK (2xx/3xx): 948
- 404 (dead): 9
- Rate-limited (429): 987
- Forbidden (403): 988
- Timeout/other (-1): 239

## Phase 2 Re-verification (2,214 error URLs)

- Now OK: 2,053
- Newly confirmed 404: 98
- Still erroring: 63 (60 timeout + 3 non-GitHub 429)

## Phase 3 Final Re-verification (63 remaining)

- Timeout URLs now OK: 59
- New 404 found: 1 (perplexity-search)
- Convex URLs (429) now OK: 3

## Removed Entries by Repository (108 total)


### CharlesWiltgen/Axiom (82 entries)

- `axiom-accessibility` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-accessibility-diag
- `axiom-app-composition` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-app-composition
- `axiom-app-discoverability` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-app-discoverability
- `axiom-app-store-submission` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-app-store-submission
- `axiom-background-processing` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-background-processing
- `axiom-build-performance` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-build-performance
- `axiom-camera-capture` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-camera-capture
- `axiom-cloud-sync` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-cloud-sync
- `axiom-codable` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-codable
- `axiom-code-signing` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-code-signing
- `axiom-combine-patterns` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-combine-patterns
- `axiom-concurrency-profiling` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-concurrency-profiling
- `axiom-core-data` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-core-data
- `axiom-core-location` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-core-location
- `axiom-database-migration` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-database-migration
- `axiom-deep-link-debugging` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-deep-link-debugging
- `axiom-display-performance` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-display-performance
- `axiom-energy` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-energy
- `axiom-extensions-widgets` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-extensions-widgets
- `axiom-foundation-models` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-foundation-models
- `axiom-grdb` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-grdb
- `axiom-hang-diagnostics` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-hang-diagnostics
- `axiom-haptics` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-haptics
- `axiom-hig` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-hig
- `axiom-in-app-purchases` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-in-app-purchases
- `axiom-ios-accessibility` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-accessibility
- `axiom-ios-ai` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-ai
- `axiom-ios-build` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-build
- `axiom-ios-concurrency` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-concurrency
- `axiom-ios-data` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-data
- `axiom-ios-games` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-games
- `axiom-ios-graphics` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-graphics
- `axiom-ios-integration` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-integration
- `axiom-ios-ml` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-ml
- `axiom-ios-networking` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-networking
- `axiom-ios-performance` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-performance
- `axiom-ios-testing` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-testing
- `axiom-ios-ui` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-ui
- `axiom-ios-vision` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ios-vision
- `axiom-liquid-glass` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-liquid-glass
- `axiom-lldb` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-lldb
- `axiom-localization` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-localization
- `axiom-mapkit` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-mapkit
- `axiom-memory-debugging` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-memory-debugging
- `axiom-metal-migration` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-metal-migration
- `axiom-networking-migration` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-networking-migration
- `axiom-now-playing` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-now-playing
- `axiom-objc-block-retain-cycles` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-objc-block-retain-cycles
- `axiom-ownership-conventions` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ownership-conventions
- `axiom-performance-profiling` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-performance-profiling
- `axiom-photo-library` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-photo-library
- `axiom-privacy-ux` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-privacy-ux
- `axiom-push-notifications` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-push-notifications
- `axiom-realitykit` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-realitykit
- `axiom-scenekit` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-scenekit
- `axiom-sf-symbols` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-sf-symbols
- `axiom-spritekit` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-spritekit
- `axiom-sqlitedata` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-sqlitedata
- `axiom-storage` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-storage
- `axiom-swift-concurrency` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swift-concurrency
- `axiom-swift-modern` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swift-modern
- `axiom-swift-performance` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swift-performance
- `axiom-swift-testing` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swift-testing
- `axiom-swiftdata` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftdata
- `axiom-swiftdata-migration` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftdata-migration
- `axiom-swiftui-architecture` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftui-architecture
- `axiom-swiftui-debugging` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftui-debugging
- `axiom-swiftui-gestures` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftui-gestures
- `axiom-swiftui-layout` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftui-layout
- `axiom-swiftui-nav` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftui-nav
- `axiom-swiftui-performance` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-swiftui-performance
- `axiom-synchronization` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-synchronization
- `axiom-testflight-triage` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-testflight-triage
- `axiom-testing-async` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-testing-async
- `axiom-tvos` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-tvos
- `axiom-ui-recording` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ui-recording
- `axiom-ui-testing` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ui-testing
- `axiom-uikit-animation-debugging` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-uikit-animation-debugging
- `axiom-uikit-bridging` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-uikit-bridging
- `axiom-ux-flow-audit` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-ux-flow-audit
- `axiom-xcode-debugging` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-xcode-debugging
- `axiom-xctest-automation` — https://github.com/CharlesWiltgen/Axiom/tree/main/.claude-plugin/plugins/axiom/skills/axiom-xctest-automation

### JuliusBrussee/caveman (2 entries)

- `caveman-cn` — https://github.com/JuliusBrussee/caveman/tree/main/caveman-cn
- `caveman-es` — https://github.com/JuliusBrussee/caveman/tree/main/skills/caveman-es

### K-Dense-AI/claude-scientific-skills (4 entries)

- `perplexity-search` — https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/perplexity-search
- `uniprot-database` — https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/uniprot-database
- `uspto-database` — https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/uspto-database
- `zinc-database` — https://github.com/K-Dense-AI/claude-scientific-skills/tree/main/scientific-skills/zinc-database

### P4nda0s/reverse-skills (2 entries)

- `rev-struct` — https://github.com/P4nda0s/reverse-skills/tree/main/plugins/reverse-engineering/skills/rev-struct
- `rev-symbol` — https://github.com/P4nda0s/reverse-skills/tree/main/plugins/reverse-engineering/skills/rev-symbol

### binance/binance-skills-hub (1 entries)

- `spot` — https://github.com/binance/binance-skills-hub/tree/main/skills/binance/spot

### chujianyun/skills (2 entries)

- `openclaw-wiki` — https://github.com/chujianyun/skills/tree/main/skills/openclaw-wiki
- `sync-skills` — https://github.com/chujianyun/skills/tree/main/skills/sync-skills

### code-yeongyu/oh-my-openagent (2 entries)

- `frontend-ui-ux` — https://github.com/code-yeongyu/oh-my-openagent/tree/main/src/features/builtin-skills/frontend-ui-ux
- `git-master` — https://github.com/code-yeongyu/oh-my-openagent/tree/main/src/features/builtin-skills/git-master

### figma/mcp-server-guide (1 entries)

- `figma-code-connect-components` — https://github.com/figma/mcp-server-guide/tree/main/skills/figma-code-connect-components

### getsentry/skills (1 entries)

- `create-pr` — https://github.com/getsentry/skills/tree/main/plugins/sentry-skills/skills/create-pr

### heroui-inc/heroui (2 entries)

- `heroui-native` — https://github.com/heroui-inc/heroui/tree/master/skills/heroui-native
- `heroui-react` — https://github.com/heroui-inc/heroui/tree/master/skills/heroui-react

### htdt/godogen (1 entries)

- `godogen` — https://github.com/htdt/godogen/tree/master/skills/godogen

### microsoft/skills (1 entries)

- `azure-cost-optimization` — https://github.com/microsoft/skills/tree/main/.github/plugins/azure-skills/skills/azure-cost-optimization

### mvanhorn/last30days-skill (1 entries)

- `open` — https://github.com/mvanhorn/last30days-skill/tree/main/variants/open

### nuxt/ui (1 entries)

- `nuxt-ui` — https://github.com/nuxt/ui/tree/master/skills/nuxt-ui

### openai/skills (1 entries)

- `imagegen` — https://github.com/openai/skills/tree/main/skills/.curated/imagegen

### sophieluu-glitch/brand-tone-designer-skill (1 entries)

- `brand-tone-designer-skill` — https://github.com/sophieluu-glitch/brand-tone-designer-skill

### vercel-labs/agent-browser (3 entries)

- `dogfood` — https://github.com/vercel-labs/agent-browser/tree/main/skills/dogfood
- `electron` — https://github.com/vercel-labs/agent-browser/tree/main/skills/electron
- `slack` — https://github.com/vercel-labs/agent-browser/tree/main/skills/slack

## Notes

- **No high-risk entries** found in v3 — all offensive tools were removed in the v2 audit (2026-04-09)
- **No Chinese character URLs** — feishu series was removed in v2 audit
- **CharlesWiltgen/Axiom** accounts for 82 of 108 removals — the repo restructured its skill paths
- **No false positives** — all 404s confirmed via GitHub Contents API with authentication
- The 3 Convex URLs (weather, google-calendar, monday) were temporarily rate-limited but confirmed alive
