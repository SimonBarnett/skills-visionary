"""Plan Agent product CLI (VIS-01/VIS-02 surface).

VIS-02 owns the model/context/effort settings flags. VIS-01 wraps this
entry as the PlanAgent.exe product binary.
"""

__all__ = ["VALID_EFFORTS", "build_parser", "cli_settings_args", "main"]
