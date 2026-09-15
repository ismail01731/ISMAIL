"""
ISMAIL AI - Computer Agent Verification Engine
Task 12E
This module verifies agent results in a safe,
non-destructive way.
IMPORTANT:
No real computer action is executed here.
"""
from backend.computer.agent.dry_run import dry_run_action
VALID_VERIFICATION_STATUS = {
    "verified",
    "not_verified",
    "failed",
}
def verify_agent_result(
    query,
    user_confirmed=False,
):
    """
    Verify the result of a dry-run agent operation.
    Since Task 12 execution is still disabled,
    dry-run operations are marked as NOT_VERIFIED
    rather than falsely claiming real success.
    """
    dry_result = dry_run_action(
        query,
        user_confirmed=user_confirmed
    )
    status = dry_result.get("status")
    if status == "blocked":
        verification_status = "failed"
        verification_reason = (
            "The requested action was blocked before execution."
        )
    elif status == "confirmation_required":
        verification_status = "not_verified"
        verification_reason = (
            "Verification cannot proceed because "
            "user confirmation is required."
        )
    elif status == "simulated":
        verification_status = "not_verified"
        verification_reason = (
            "The action was simulated only. "
            "No real computer change occurred, "
            "so real execution cannot be verified."
        )
    else:
        verification_status = "not_verified"
        verification_reason = (
            "The operation result could not be verified."
        )
    return {
        "request": dry_result.get("request", ""),
        "status": verification_status,
        "verification_status": verification_status,
        "verification_reason": verification_reason,
        "dry_run_status": status,
        "simulated": dry_result.get(
            "simulated",
            False
        ),
        "execution_allowed": False,
        "verified": verification_status == "verified",
        "plan": dry_result.get("plan"),
    }
def get_verification_summary(
    query,
    user_confirmed=False,
):
    """
    Return a human-readable verification report.
    """
    result = verify_agent_result(
        query,
        user_confirmed=user_confirmed
    )
    lines = [
        "Computer Agent Verification",
        "Request: " + result.get("request", ""),
        "Verification Status: "
        + result.get("verification_status", ""),
        "Dry Run Status: "
        + str(result.get("dry_run_status", "")),
        "Verified: "
        + str(result.get("verified", False)),
        "Execution Allowed: "
        + str(result.get("execution_allowed", False)),
        "Reason: "
        + result.get("verification_reason", ""),
    ]
    return "\n".join(lines)
