FAKE_POLICIES = {
    "billing": (
        "In-network deductible is $500 per year for individual coverage. "
        "After the deductible is met, coinsurance is 20% for covered services. "
        "Claims are typically processed within 10 business days of submission."
    ),
    "dental": (
        "In-network preventive dental cleanings and exams are covered at 100%, "
        "twice per year. Fillings are covered at 80% after the annual deductible. "
        "Orthodontia is covered at 50% up to a $1,500 lifetime maximum."
    ),
    "benefits_coverage": (
        "Annual preventive physicals are covered at 100% with no copay when "
        "performed by an in-network provider. Specialist visits require a $40 "
        "copay. Coverage eligibility begins on the first day of the month "
        "following 30 days of employment."
    ),
}


def get_policy(category: str) -> str | None:
    """Looks up fictional policy text for a given ticket category."""
    return FAKE_POLICIES.get(category)
