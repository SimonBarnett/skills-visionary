# VIS-07 / FR #142 evidence

Standalone MSI build: `python tools/build_plan_agent_msi.py` writes `tools/out/PlanAgent.msi`.

The file is a Windows Installer database (OLE header) with product name `Plan Agent`, a stable product code, and at least one File row (`PlanAgent.exe` payload). It is the Plan product MSI, not a Bob ear installer.

Optional second argument: path to a real `PlanAgent.exe` to stage instead of the built-in MZ stub.

GitHub Release upload and the plan.ntsa.uk download link are the publish step measured by the same S1 row. This change produces the MSI asset those steps ship. `tools/out/` is not committed.
