# skills-visionary

High-reasoning new-product intake skill. See `docs/vision.md`.

Home: `.grok/skills/visionary/SKILL.md`

Copy to the agent home:

```
copy .grok\skills\visionary\SKILL.md %USERPROFILE%\.grok\skills\visionary\SKILL.md
```

Park/create/webhook stay `bob-spec-intake` in `agentic_build`. Harvest
learnings back here (`harvest-skills-visionary`).

## Vision-pack gate

Before park or dispatch, run the validator on the vision markdown (and
mocks directory when shape is not UNKNOWN):

```
python tools/validate-vision-pack.py docs/vision.md --mocks-dir docs/mocks
```

`bob-spec-intake` (in `agentic_build`) must invoke this command (or
equivalent path) and refuse park/dispatch when exit code is non-zero.
CI runs the same check via `.github/workflows/vision-pack.yml`.
