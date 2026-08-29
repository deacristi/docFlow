# Root Cause Analysis — Visual Data-Flow Trace Guide

**Version**: 1.0.0 | **Last Updated**: 2026-02-24

---

## Purpose

Every root cause analysis document **MUST** include a Visual Data-Flow Trace — an ASCII diagram that shows the exact runtime path from the user action (or trigger) to the point of failure. This makes bugs immediately understandable to any reader without requiring them to read the surrounding prose first.

The trace should be the **first thing** in the "Detailed Root Cause Analysis" section.

---

## Required Format

### Structure

```
Trigger / Entry Point
  → Step 1 (component)
    → Step 2 (component)
      → Step 3 (component)                    ← BUG HERE
        → What the code does
        → What the code expects vs. what actually happens
        ← What is returned (showing the broken value)
      ← What propagates up (showing the consequence)
    → How the consumer reacts to the broken value
  → Final user-visible outcome
```

### Rules

1. **Use `→` for forward flow** (calls going deeper into the stack)
2. **Use `←` for return flow** (values propagating back up)
3. **Mark the bug location** with `← BUG HERE` on the right side
4. **Indent to show call depth** — each nested call adds 2 spaces
5. **Show actual values** — don't say "returns error", say `returns None` or `returns "null"`
6. **Include component names** in parentheses — `(component)` or `file.py L99`
7. **Show the contrast** — what was expected vs. what happened
8. **End with the user-visible consequence** at the top level

---

## Examples

### Example 1: Data Key Mismatch (ISSUE-007)

```
User Question
  → ExpertOrchestrator
    → ExpertSelector (keyword routing)
      → BaseExpert.process()
        → ReActEngine.run() (up to 5 iterations)
          → Tool.execute(params)                          ← BUG HERE
            → tradepulse_core function(params)
              → Returns {"success": True, "tickers": [...]}
            ← Tool.execute does: data=result.get("data")  ← "data" key not found → None
            ← Returns ToolResult(success=True, data=None)
          → ReActEngine formats: json.dumps(None) → "null"
          → Observation: "SUCCESS: null"
        → LLM interprets: "Tool executed successfully but no data was available"
      → LLM generates generic/hallucinated response
    → Consensus engine merges responses
  → User receives plausible but data-free answer
```

### Example 2: Cascading API Rate Limit (ISSUE-008)

```
User asks: "Which sectors are rotating?"
  → ExpertOrchestrator starts 3 experts in parallel (asyncio.gather)
    → Regime Expert: ReAct iteration 1
      → get_sector_performance()
        → Polygon API call 1/5 (XLK) → OK (T=3s)
        → Polygon API call 2/5 (XLV) → rate limited, waiting...  ← BOTTLENECK
        → Polygon API call 3/5 (XLF) → rate limited, waiting...
        → ...5 sequential calls, each potentially delayed 12s
      ← Returns after 35s → "SUCCESS: null" (ISSUE-007 bug)
    → Regime Expert: ReAct iteration 2 (wasted — tries another API-heavy tool)
      → get_market_breadth() → 5 more API calls → rate limited again
      ← Returns after 30s → "SUCCESS: null" (same bug)
    → Regime Expert: ReAct iteration 3...
  → 90s timeout reached
  → User receives: "Request timed out"
```

### Example 3: Parameter Binding Failure (IP-033)

```
User asks: "What's the sentiment on VIR?"
  → CommunityExpert.process()
    → ReActEngine selects tool: get_ticker_sentiment
      → LLM generates: {"symbol": "VIR", "hours": 24}
      → Tool.execute(symbol="VIR", hours=24)              ← BUG HERE
        → community.get_ticker_sentiment(symbol="VIR", hours=24)
        ← Function signature: get_ticker_sentiment(ticker, timeframe_hours)
        ← TypeError: unexpected keyword argument 'symbol'
      ← Returns ToolResult(success=False, error="TypeError...")
    → ReActEngine: iteration 2 → retries with same wrong params
    → ReActEngine: iteration 3 → gives up
  → LLM generates fallback: "Unable to retrieve sentiment data"
```

---

## Code Evidence Section

After the data-flow trace, include a **Code Evidence** section showing the actual code at the bug location with a comment highlighting the issue:

```python
# File: app/experts/base_expert.py lines 95-105
async def execute(self, **kwargs) -> 'ToolResult':
    try:
        result = await self.func(**kwargs)
        if isinstance(result, dict):
            return ToolResult(
                success=result.get("success", True),
                data=result.get("data"),          # ← BUG: only extracts "data" key
                error=result.get("error"),
                tool_name=self.name,
                execution_time_ms=0
            )
```

---

## Anti-Patterns (Do NOT Do This)

### ❌ Too vague — no actual values shown
```
User sends request
  → System processes it
    → Tool runs
      → Data is lost                    ← BUG
    → Response generated
  → User gets wrong answer
```

### ❌ Too detailed — drowns the signal in noise
```
User sends HTTP POST to /api/v1/chat/message with headers...
  → FastAPI middleware validates JWT token...
    → CORS check passes...
      → Request body parsed via Pydantic model ChatRequest...
        → ChatService.__init__ loads 47 dependencies...
          → ... (20 more irrelevant steps)
            → The actual bug
```

### ✅ Right level — shows the path, marks the bug, shows actual values
```
User Question
  → ExpertOrchestrator
    → Tool.execute(params)                                ← BUG HERE
      → function returns {"tickers": [...]}
      ← data=result.get("data") → None (key mismatch)
    → Observation: "SUCCESS: null"
  → LLM generates hallucinated response
```

---

## Checklist

Before submitting a root cause analysis, verify your data-flow trace:

- [ ] Starts from the trigger (user action, API call, scheduled task)
- [ ] Ends at the user-visible consequence
- [ ] Bug location is clearly marked with `← BUG HERE`
- [ ] Actual values are shown (not just "error" but `None`, `"null"`, `TypeError`)
- [ ] The contrast between expected and actual behavior is visible
- [ ] Nesting depth reflects call depth (2-space indentation per level)
- [ ] Irrelevant middleware/framework layers are omitted
- [ ] A code evidence snippet follows the trace
