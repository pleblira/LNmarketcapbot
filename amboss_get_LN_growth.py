from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.amboss.space/graphql")

query = """
{
    getStats {
        network_growth {
            new_channels {
                week_change {
                    capacity
                }
            }
        }
    }
}    
"""
def amboss_get_LN_growth():
    result = client.execute(query)
    print(result)
    LN_growth_weekly_in_sats = int(result['data']['getStats']['network_growth']['new_channels']['week_change']['capacity'])
    print(LN_growth_weekly_in_sats)
    LN_growth_weekly_in_BTC = (f"{LN_growth_weekly_in_sats/100000000:.2f}")
    print(LN_growth_weekly_in_BTC)
    # return int(LN_capacity_in_BTC)

if __name__ == "__main__":
    amboss_get_LN_growth()