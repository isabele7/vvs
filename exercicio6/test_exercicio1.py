def can_approve_loan(income, credit_score, has_debt):
    if (income > 5000 and credit_score > 700) or not has_debt:
        return True
    return False

def test_A_true_B_true_C_true():
    assert can_approve_loan(6000, 800, True) == True

def test_A_true_B_false_C_true():
    assert can_approve_loan(6000, 600, True) == False
    
def test_A_false_B_true_C_true():
    assert can_approve_loan(4000, 800, True) == False
    
def test_A_true_B_false_C_false():
    assert can_approve_loan(6000, 600, False) == True
