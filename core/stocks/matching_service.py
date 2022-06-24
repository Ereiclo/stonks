from doctest import DocFileSuite
from .models import Portfolio,IncompleteOrder,CompleteOrder,Order




#compra
def matching_service_buy(order,relevant_orders):
    buyer = order.client_dni
    try:
        buyer_portfolio = Portfolio.objects.get(client_dni = buyer, company_ruc = order.company_ruc)
    except Portfolio.DoesNotExist:
        buyer_portfolio = Portfolio.objects.create(client_dni = buyer,company_ruc=order.company_ruc,quantity= 0)

    total_sold = 0
    total_quantity = 0
    matched = False
    
    for current_order in relevant_orders:  	
        seller = current_order.client_dni
        seller_portfolio = Portfolio.objects.get(client_dni = seller, company_ruc = current_order.company_ruc)
        quantity_sold = min(order.quantity_left, current_order.quantity_left)
        price = current_order.price

        if buyer.money < quantity_sold * price:
            break

        current_total_sold = (current_order.quantity - current_order.quantity_left) * current_order.avg_price
        current_total_sold += quantity_sold * price

        seller_total_sold = seller_portfolio.quantity * seller_portfolio.avg_price
        buyer_total_sold = buyer_portfolio.quantity * buyer_portfolio.avg_price

        current_order.quantity_left -= quantity_sold
        seller_portfolio.quantity -= quantity_sold
        buyer_portfolio.quantity += quantity_sold
        order.quantity_left -= quantity_sold
        current_order.avg_price = current_total_sold / (current_order.quantity - current_order.quantity_left)

        seller_total_sold -= quantity_sold * price
        buyer_total_sold += quantity_sold * price
        buyer_portfolio.avg_price = buyer_total_sold / buyer_portfolio.quantity

        buyer.money -= quantity_sold * price
        seller.money += quantity_sold * price
        total_sold += quantity_sold * price
        total_quantity += quantity_sold
        matched = True
    
        if current_order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = current_order.id).delete()
            CompleteOrder.objects.create(order_id=current_order)
        

        if seller_portfolio.quantity != 0:
            seller_portfolio.avg_price = seller_total_sold / seller_portfolio.quantity
            seller_portfolio.save()
        else:
            seller_portfolio.delete()

        current_order.save()
        seller.save()
        buyer_portfolio.save()
        order.save()

        if order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = order.id).delete()
            CompleteOrder.objects.create(order_id=order)
            break

    if matched:
        order.company_ruc.latest_price = price
        order.company_ruc.save()


    order.avg_price = total_sold / total_quantity
    buyer.save()
    order.save()




#venta
def matching_service_sell(order,relevant_orders):
    seller = order.client_dni
    total_bought = 0
    total_quantity = 0
    matched = False

    try:
        seller_portfolio = Portfolio.objects.get(client_dni = seller, company_ruc = order.company_ruc)
    except Portfolio.DoesNotExist:
        seller_portfolio = Portfolio.objects.create(client_dni = seller,company_ruc=order.company_ruc,quantity= 0)
    
    for current_order in relevant_orders:  	
        buyer = current_order.client_dni
        buyer_portfolio = Portfolio.objects.get(client_dni = buyer, company_ruc = current_order.company_ruc)
        quantity_sold = min(order.quantity_left, current_order.quantity_left)
        price = current_order.price

        if buyer.money < quantity_sold * price:
            continue	
            #break

        current_total_sold = (current_order.quantity - current_order.quantity_left) * current_order.avg_price
        current_total_sold += quantity_sold * price

        seller_total_sold = seller_portfolio.quantity * seller_portfolio.avg_price
        buyer_total_sold = buyer_portfolio.quantity * buyer_portfolio.avg_price

        current_order.quantity_left -= quantity_sold
        seller_portfolio.quantity -= quantity_sold
        buyer_portfolio.quantity += quantity_sold
        order.quantity_left -= quantity_sold
        current_order.avg_price = current_total_sold / (current_order.quantity - current_order.quantity_left)

        seller_total_sold -= quantity_sold * price
        
        buyer_total_sold += quantity_sold * price
        buyer_portfolio.avg_price = buyer_total_sold / buyer_portfolio.quantity

        buyer.money -= quantity_sold * price
        seller.money += quantity_sold * price
        total_bought += quantity_sold * price
        total_quantity += quantity_sold
        matched = True
    
        if current_order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = current_order.id).delete()
            CompleteOrder.objects.create(order_id=current_order)
        

        if seller_portfolio.quantity != 0:
            seller_portfolio.avg_price = seller_total_sold / seller_portfolio.quantity
            seller_portfolio.save()
        else:
            seller_portfolio.delete()

        current_order.save()
        seller.save()
        buyer_portfolio.save()
        order.save()

        if order.quantity_left == 0:
            IncompleteOrder.objects.filter(pk = order.id).delete()
            CompleteOrder.objects.create(order_id=order)
            break

    if matched:
        order.company_ruc.latest_price = price
        order.company_ruc.save()

    order.avg_price = total_bought / total_quantity
    seller.save()
    order.save()


def matching_service(order):
      	#lock()
    company_orders = Order.objects.filter(company_ruc = order.company_ruc_id).exclude(client_dni_id = order.client_dni_id).exclude( transaction_type__startswith = order.transaction_type[0])
    if order.transaction_type[0] == 'B':  # compra 
        company_orders.filter(price__lte = order.price).order_by("price","date")
        matching_service_buy(order,company_orders)
    elif order.transaction_type[0] == 'S':	# venta
        company_orders.filter(price__gte = order.price).order_by("-price","date")
        matching_service_sell(order,company_orders)
#unlock()



