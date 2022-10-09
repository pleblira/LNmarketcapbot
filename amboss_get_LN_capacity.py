from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.amboss.space/graphql")

query = """
    query {
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
    LN_capacity_in_BTC = int(round(LN_capacity_in_sats / 100000000,0))
    # print(LN_capacity_in_BTC)
    return int(LN_capacity_in_BTC)

if __name__ == "__main__":
    amboss_get_LN_capacity()