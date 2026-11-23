# FR #187 — PlanAgent.msi only

plan-v1.0.5 had both PlanAgent.msi (CI) and a manual plan.msi alias with the same digest.
Future releases and site redirects use PlanAgent.msi (+ .sha256) only. Do not upload plan.msi.