from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.amboss.space/graphql")

query = """
    query GetStats {
        getStats{
            channels{
                metrics {
                    sum
                } 
            }
        }
    }
    """
def amboss_get_LN_capacity():
    result = client.execute(query=query)
    LN_capacity_in_sats = int(result['data']['getStats']['channels']['metrics']['sum'])
    global LN_capacity_in_BTC
    LN_capacity_in_BTC = int(round(LN_capacity_in_sats / 100000000,0))
    # print("Current LN channel capacity: ",str(capacity_btc) + "BTC")
    return int(LN_capacity_in_BTC)

amboss_get_LN_capacity()

# print(str(LN_capacity_in_btc))
