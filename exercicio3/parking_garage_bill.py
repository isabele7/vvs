from datetime import datetime
from decimal import Decimal

class ParkingGarageBilling:
    def calculate_fee(
        self,
        entry_time: datetime,
        exit_time: datetime,
        lost_ticket: bool = False,
    ) -> Decimal:
        if exit_time == entry_time:
            raise ValueError("Horário de saída não pode ser igual ao horário de entrada.")
        if exit_time < entry_time:
            raise ValueError("Horário de saída não pode ser anterior ao horário de entrada.")
        if lost_ticket:
            return Decimal("300.00")

        duration = exit_time - entry_time
        total_minutes = duration.total_seconds() / 60

        if total_minutes <= 30:
            return Decimal("0.00")

        full_days = int(total_minutes // 1440)
        remaining_minutes = total_minutes - (full_days * 1440)
        fee = Decimal(full_days) * Decimal("100.00")

        if remaining_minutes > 30:
            hours = (remaining_minutes - 30) / 60
            partial_fee = Decimal("5.00") * Decimal(hours)
            if partial_fee > Decimal("100.00"):
                partial_fee = Decimal("100.00")
            fee += partial_fee

        # Desconto noturno para entradas entre 22h e 6h
        if entry_time.hour >= 22 or entry_time.hour <= 6:
            fee -= Decimal("10.00")
            if fee < Decimal("0.00"):
                fee = Decimal("0.00")

        # Desconto de fim de semana
        if entry_time.weekday() >= 5:
            fee *= Decimal("0.8")

        return round(fee, 2)

def calculate_billing(entry_time_str: str, exit_time_str: str, lost_ticket: bool = False) -> Decimal:
    entry_time = datetime.strptime(entry_time_str, "%Y-%m-%d %H:%M:%S")
    exit_time = datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S")
    billing = ParkingGarageBilling()
    return billing.calculate_fee(entry_time, exit_time, lost_ticket)
