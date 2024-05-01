import matplotlib.pyplot as plt
from ib_insync import IB, util, Forex, Order

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)


def create_contract(symbol):
    return Forex(symbol)


def fetch_and_visualize(symbol, duration, barSize):
    contract = create_contract(symbol)

    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=duration,
        barSizeSetting=barSize,
        whatToShow='MIDPOINT',
        useRTH=True,
        formatDate=1
    )

    ib.disconnect()

    if bars:
        df = util.df(bars)
        plot_data(df, symbol)


def plot_data(df, symbol):
    df.set_index('date', inplace=True)
    plt.figure(figsize=(10, 5))
    plt.plot(df['close'], label='Close Price', color='blue')
    plt.title(f'Historical Data for {symbol}')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.grid(True)
    plt.legend()
    plt.show()


def make_contract():
    symbol = input("Enter the symbol: ")
    contract = create_contract(symbol)
    print(f"\nContract created for: Symbol: {contract.symbol}, "
          f"Type: {contract.secType}, "
          f"Exchange: {contract.exchange}, "
          f"Currency: {contract.currency}")


def request_historical_data():
    symbol = input("Enter the symbol: ")
    contract = create_contract(symbol)
    # 1 D, 1 W, 1 M, 1 Y
    duration = input("Enter the duration (e.g., 1 M): ")
    # 1 min, 1 hour, 1 day
    bar_size = input("Enter the bar size (e.g., 1 day): ")

    fetch_and_visualize(symbol, duration, bar_size)
    print(f"Requested historical data for {contract.symbol}")


def place_order():
    symbol = input("Enter the symbol: ")
    contract = create_contract(symbol)
    action = input("Enter the action (BUY/SELL): ")
    quantity = int(input("Enter the quantity: "))
    price = float(input("Enter the price or 0 for MKT: "))
    order_type = 'LMT' if price != 0 else 'MKT'

    order = Order(
        orderType=order_type,
        action=action,
        totalQuantity=quantity,
        lmtPrice=price if price != 0 else None
    )
    trade = ib.placeOrder(contract, order)

    print(f"Order placed for: "
          f"Symbol: {contract.symbol}, "
          f"Type: {order_type}, "
          f"Action: {action}, "
          f"Quantity: {quantity}, "
          f"Price: {'Market' if price == 0 else price}, "
          f"Status: {trade.orderStatus.status}")

    def fill_event(trade, fill):
        print(f"Trade status {trade.orderStatus} filled for {fill.execution.shares} shares at {fill.execution.price}")

    trade.fillEvent += fill_event


def print_orders():
    open_orders = ib.reqOpenOrders()

    if open_orders:
        print("Open Orders:")
        for order_obj in open_orders:
            order = order_obj.order
            contract = order_obj.contract
            print(f"OrderId: {order.orderId}, "
                  f"PermId: {order.permId}, "
                  f"ClientId: {order.clientId}, "
                  f"Account: {order.account}, "
                  f"Symbol: {contract.symbol}, "
                  f"SecType: {contract.secType}, "
                  f"Exchange: {contract.exchange}, "
                  f"Action: {order.action}, "
                  f"OrderType: {order.orderType}, "
                  f"TotalQty: {order.totalQuantity}, "
                  f"CashQty: {getattr(order, 'cashQty', 'N/A')}, "
                  f"LmtPrice: {order.lmtPrice if order.orderType == 'LMT' else 'Market'}, "
                  f"AuxPrice: {getattr(order, 'auxPrice', 'N/A')}, ")
    else:
        print("No open orders.")


def cancel_order():
    order_id = int(input("Enter the order ID to cancel: "))
    print("Cancelling order...")
    orders = ib.openOrders()
    if not orders:
        print("No open orders.")
        return

    for order in orders:
        if order.orderId == order_id:
            ib.cancelOrder(order)
            print(f"Order {order_id} cancelled")
            return
    print(f"Order {order_id} not found")


def main_menu():
    try:
        while True:
            print("\nMain Menu:")
            print("1. Make Contract")
            print("2. Request Historical Data")
            print("3. Place Order")
            print("4. Print Orders")
            print("5. Cancel Order")
            print("Type 'exit' to quit")
            option = input("Choose an option: ")

            if option == '1':
                make_contract()
            elif option == '2':
                request_historical_data()
            elif option == '3':
                place_order()
            elif option == '4':
                print_orders()
            elif option == '5':
                cancel_order()
            elif option.lower() == 'exit':
                print("Goodbye!")
                break
            else:
                print("Invalid option")
    except Exception as e:
        print(f"Error: {e}")


main_menu()
