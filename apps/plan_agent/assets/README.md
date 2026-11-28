# Plan Agent icon assets (VIS-06 / FR #281)

| File | Role |
|------|------|
| `plan-gantt-source.png` | 512×512 master art from product (issue #281); edit this, then rebuild |
| `plan-gantt.ico` | Windows exe / systray (16–256 px) |
| `plan-gantt.png` | Docs / landing (256 px) |

`plan-gantt.ico` uses BMP-style entries so `PlanAgent.csproj` `ApplicationIcon` embeds in release `PlanAgent.exe` (FR #281).

Rebuild derived icons from the checked-in source:

```text
python tools/build_plan_gantt_icon.py
```

BOB-48 (bob-ear tray) consumes `plan-gantt.ico` from the skills-visionary release (`docs/vendor/plan-agent-bob-ear.json`).