from decimal import Decimal
from parking_billing import calculate_billing

def test_invalid_time():
    try:
        calculate_billing("2026-06-01 10:00:00", "2026-05-31 10:00:00")
    except ValueError as e:
        assert str(e) == "Horário de saída não pode ser anterior ao horário de entrada."

def test_exit_time_same_as_entry_time():
    try:
        calculate_billing("2026-06-01 10:00:00", "2026-06-01 10:00:00")
    except ValueError as e:
        assert str(e) == "Horário de saída não pode ser igual ao horário de entrada."

def test_29_minutes_free():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-01 10:29:00")
    assert fee == Decimal("0.00")  

def test_30_minutes_free():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-01 10:30:00")
    assert fee == Decimal("0.00") 

def test_31_minutes_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-01 10:31:00")
    assert fee == Decimal((5/60) * (31 - 30)).quantize(Decimal("0.01"))  

def test_1_hour_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-01 11:00:00")
    assert fee == Decimal((5/60) * (60 - 30)).quantize(Decimal("0.01"))  

def test_21h59_fee():
    fee = calculate_billing("2026-06-01 21:59:00", "2026-06-02 01:00:00")
    # entrada 21:59 < 22h -> sem desconto noturno
    assert fee == Decimal((5/60) * (181 - 30)).quantize(Decimal("0.01"))
        
def test_22h_fee():
    fee = calculate_billing("2026-06-01 22:00:00", "2026-06-02 02:00:00")
    # entrada 22h -> desconto noturno: proporcional − R$10
    assert fee == (Decimal((5/60) * (240 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))
    
def test_5h59_fee():
    fee = calculate_billing("2026-06-01 05:59:00", "2026-06-01 10:00:00")
    # entrada 05:59 < 6h -> desconto noturno: proporcional − R$10
    assert fee == (Decimal((5/60) * (241 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))
    
def test_6h_fee():
    fee = calculate_billing("2026-06-01 06:00:00", "2026-06-01 10:00:00")
    # entrada 06:00 = desconto noturno aplicado
    assert fee == (Decimal((5/60) * (240 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_23h59_fee():
    fee = calculate_billing("2026-06-01 00:00:00", "2026-06-01 23:59:00")
    # entrada 00h -> desconto noturno: teto(1439 min) − R$10
    assert fee == (min(Decimal((5/60) * (1439 - 30)), Decimal("100.00")) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_24h_fee():
    fee = calculate_billing("2026-06-01 00:00:00", "2026-06-02 00:00:00")
    # 1 diária (R$100) - R$10 desconto noturno = R$90
    assert fee == (Decimal("100.00") - Decimal("10.00")).quantize(Decimal("0.01"))
    
def test_24h01_fee():
    fee = calculate_billing("2026-06-01 00:00:00", "2026-06-02 00:31:00")
    # entrada 00h -> desconto noturno: (1 diária + 1 min cobrável) − R$10
    assert fee == (Decimal("100.00") * 1 + Decimal((5/60) * (31 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_25h_fee():
    fee = calculate_billing("2026-06-01 00:00:00", "2026-06-02 01:00:00")
    # entrada 00h -> desconto noturno: (1 diária + 30 min cobráveis) − R$10
    assert fee == (Decimal("100.00") * 1 + Decimal((5/60) * (60 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_lost_ticket_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-01 12:00:00", lost_ticket=True)
    assert fee == Decimal("300.00")

def test_saturday_discount():
    fee = calculate_billing("2026-04-04 10:00:00", "2026-04-04 15:00:00")
    # entrada sábado 10h: proporcional × 80% (sem desconto noturno)
    assert fee == (Decimal((5/60) * (300 - 30)) * Decimal("0.8")).quantize(Decimal("0.01"))

def test_sunday_discount():
    fee = calculate_billing("2026-04-05 10:00:00", "2026-04-05 15:00:00")
    # entrada domingo 10h: proporcional × 80% (sem desconto noturno)
    assert fee == (Decimal((5/60) * (300 - 30)) * Decimal("0.8")).quantize(Decimal("0.01"))

def test_21h59_discount():
    fee = calculate_billing("2026-06-01 21:59:00", "2026-06-02 01:00:00")
    # entrada 21:59 < 22h -> sem desconto noturno
    assert fee == Decimal((5/60) * (181 - 30)).quantize(Decimal("0.01"))

def test_22h_discount():
    fee = calculate_billing("2026-06-01 22:00:00", "2026-06-02 02:00:00")
    # entrada 22h -> desconto noturno: proporcional − R$10
    assert fee == (Decimal((5/60) * (240 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_6h_discount():
    fee = calculate_billing("2026-06-01 06:00:00", "2026-06-01 10:00:00")
    # entrada 06:00 -> desconto noturno
    assert fee == (Decimal((5/60) * (240 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))
    
def test_6h01_discount():
    fee = calculate_billing("2026-06-01 06:01:00", "2026-06-01 10:00:00")
    # entrada 06:01 -> sem desconto
    assert fee == (Decimal((5/60) * (239 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_fee_cap():
    fee = calculate_billing("2026-06-01 00:01:00", "2026-06-01 23:59:00")
    # entrada 00:01 -> desconto noturno: teto − R$10
    assert fee == (min(Decimal((5/60) * (1438 - 30)), Decimal("100.00")) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_below_fee_cap():
    fee = calculate_billing("2026-06-01 00:01:00", "2026-06-01 20:00:00")
    # entrada 00:01 -> desconto noturno: proporcional − R$10
    assert fee == (Decimal((5/60) * (1199 - 30)) - Decimal("10.00")).quantize(Decimal("0.01"))

def test_1_day_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-02 10:00:00")
    assert fee == Decimal("100.00") * 1  # 1 diária, sem desconto noturno

def test_1_day_and_29_minutes_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-02 10:29:00")
    assert fee == Decimal("100.00") * 1  

def test_1_day_and_30_minutes_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-02 10:30:00")
    assert fee == Decimal("100.00") * 1  

def test_2_days_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-03 10:00:00")
    assert fee == Decimal("100.00") * 2  # 2 diárias, sem desconto noturno

def test_enter_friday_exit_saturday_fee():
    fee = calculate_billing("2026-06-12 10:00:00", "2026-06-13 10:00:00")
    assert fee == Decimal("100.00") * 1  # entrada sexta, sem desconto

def test_enter_saturday_exit_sunday_fee():
    fee = calculate_billing("2026-06-13 00:00:00", "2026-06-14 00:00:00")
    # entrada sábado 00h: (1 diária − R$10 noturno) × 80% fim de semana
    assert fee == ((Decimal("100.00") * 1 - Decimal("10.00")) * Decimal("0.8")).quantize(Decimal("0.01"))

def test_enter_monday_exit_friday_fee():
    fee = calculate_billing("2026-06-01 10:00:00", "2026-06-05 10:00:00")
    assert fee == Decimal("100.00") * 4  # 4 diárias, sem desconto
