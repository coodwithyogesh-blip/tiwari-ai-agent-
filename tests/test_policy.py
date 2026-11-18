from backend.policy import plan_command


def test_train_booking_requires_final_confirmation():
    plan = plan_command("Mere liye Mumbai se Pune train ticket book karo")
    assert plan["service"] == "rail"
    assert plan["approval_required"] is True
    assert plan["execution"] == "not_configured"


def test_train_status_lookup_can_run_automatically():
    plan = plan_command("Mera PNR status check karo")
    assert plan["service"] == "rail"
    assert plan["approval_required"] is False


def test_sms_send_is_marked_as_sensitive():
    plan = plan_command("Papa ko SMS bhejo ki main aa raha hoon")
    assert plan["service"] == "sms"
    assert plan["approval_required"] is True


def test_github_read_only_action_can_run_automatically():
    plan = plan_command("GitHub Actions build status dikhao")
    assert plan["service"] == "github"
    assert plan["approval_required"] is False


def test_purchase_requires_confirmation_and_never_claims_success():
    plan = plan_command("Zepto se milk order kar do")
    assert plan["service"] == "shopping"
    assert plan["approval_required"] is True
    assert plan["execution"] == "not_configured"


def test_unknown_command_is_not_executed():
    plan = plan_command("mere liye kuch bhi kar do")
    assert plan["service"] == "general"
    assert plan["execution"] == "not_configured"
