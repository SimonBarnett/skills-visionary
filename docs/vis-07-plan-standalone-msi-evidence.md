# VIS-07 / FR #142 evidence

Standalone MSI build: `python tools/build_plan_agent_msi.py` writes `tools/out/PlanAgent.msi`.

The file is a Windows Installer database (OLE header) with product name `Plan Agent` and a stable product code. It is the Plan product MSI, not a Bob ear installer.

GitHub Release upload and the plan.ntsa.uk download link are the publish step measured by the same S1 row. This change produces the MSI asset those steps ship. `tools/out/` is not committed.
