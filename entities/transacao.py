from dataclasses import dataclass, fields
from datetime import datetime


@dataclass(frozen=True)
class Transacao:
    id: str
    customer: str
    customer_name: str
    billing_type: str
    value: float
    due_date: datetime
    status: str
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transacao | None":
        try:
            return cls(
                id=data['id'],
                customer=data['customer'],
                customer_name=data['customerName'],
                billing_type=data['billingType'],
                value=float(data['value']),
                due_date=datetime.fromisoformat(data['dueDate']),
                status=data['status']
            )
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Dados inválidos: {e}") from e
            