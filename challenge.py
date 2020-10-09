import time
import pyRofex
import sys

try:
    if ((len(sys.argv) == 8) & (sys.argv[2]=='-u') & (sys.argv[4]=='-p') & (sys.argv[6]=='-a')):
        instrument = sys.argv[1]
        user = sys.argv[3]
        password = sys.argv[5]
        account = sys.argv[7]
            
    bid_price_default = 75.25

    # Initialize the environment
    print("Iniciando sesión en Remarkets")
    pyRofex.initialize(user = user,
                       password = password,
                       account = account,
                       environment=pyRofex.Environment.REMARKET)

    # Initialize Websocket Connection
    pyRofex.init_websocket_connection()

    # Subscribes to receive market data messages for a list of valid instruments
    entries = [pyRofex.MarketDataEntry.BIDS,
               pyRofex.MarketDataEntry.LAST]

    print("Consultando símbolo")

    try:
        pyRofex.market_data_subscription(tickers=instrument, entries=entries)
        md = pyRofex.get_market_data(ticker=instrument, entries=[pyRofex.MarketDataEntry.LAST])
        md["marketData"]
        try:
            LP = md["marketData"]["LA"]["price"]
            print("Último precio operado: $", LP)
        except:
            print("Último precio operado: ", None)
    
        print("Consultando BID")
        try:
            md = pyRofex.get_market_data(ticker=instrument, entries=[pyRofex.MarketDataEntry.BIDS])
            BID = md["marketData"]["BI"][0]["price"]
            print("Precio de BID: $", BID)
            print("Ingresando orden a $", BID-0.01)
            # Send an order to check that order_report_handler is called
            pyRofex.send_order(ticker=instrument,
                                side=pyRofex.Side.BUY,
                                size=1,
                                price=BID-0.01,
                                order_type=pyRofex.OrderType.LIMIT)
        except:
            print("No hay BIDs activos")
            print("Ingresando orden a $", bid_price_default)
            # Send an order to check that order_report_handler is called
            pyRofex.send_order(ticker=instrument,
                                side=pyRofex.Side.BUY,
                                size=1,
                                price=bid_price_default,
                                order_type=pyRofex.OrderType.LIMIT)
    except:
        print("Símbolo inválido")

    #Wait 1 sec then close the connection
    print("Cerrando sesión en Remarkets")
    time.sleep(1)
    pyRofex.close_websocket_connection()

except:
    print("Error - Por favor, introduzca los argumentos correctamente")
    print('Ejemplo: python challenge.py DODic20 -u juampylaza5129 -p taymsD2% -a REM5129')
    sys.exit()