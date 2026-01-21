import random
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
from agency.models import Sale, Supplier, Agent

User = get_user_model()

def run():
    print("Generating 30 test sales...")
    
    # Ensure dependencies exist
    user, _ = User.objects.get_or_create(username='test_salesman', defaults={'role': 'SALESMAN'})
    supplier, _ = Supplier.objects.get_or_create(name='Test Airline', defaults={'contact_info': '123'})
    agent, _ = Agent.objects.get_or_create(name='Test Agent', defaults={'contact_info': '456'})
    
    # Generate 30 sales
    sales_to_create = []
    for i in range(30):
        is_agent = random.choice([True, False])
        ticket_type = random.choice(['AIRTICKET', 'TOUR', 'UMRA'])
        curr = random.choice(['USD', 'UZS'])
        
        purchase_price = Decimal(random.randint(100, 500))
        sold_price = purchase_price + Decimal(random.randint(10, 100))
        
        sale = Sale(
            salesman=user,
            supplier=supplier,
            ticket_type=ticket_type,
            destination=f"City {i}",
            quantity=1,
            purchase_price=purchase_price,
            purchase_currency=curr,
            sales_channel='AGENT' if is_agent else 'INDIVIDUAL',
            agent=agent if is_agent else None,
            sold_price=sold_price,
            sold_currency=curr,
            comment=f"Auto-generated sale {i+1}"
        )
        sales_to_create.append(sale)
    
    # Bulk create doesn't call save() so signals/custom save logic (like profit calc) won't run.
    # We must iterate and save.
    for s in sales_to_create:
        s.save()
        
    print(f"Successfully created {Sale.objects.count()} sales (total in DB).")

if __name__ == '__main__':
    run()
