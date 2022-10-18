# from datetime import datetime
# from email.utils import parsedate_to_datetime
# import json
# import grequests
# from urllib.parse import urlparse, parse_qs

# def getDetails(tokens):
#     proxies = {
#         'http': 'http://jdowell:Qwe123_country-us@geo.iproyal.com:22323',
#         'https': 'http://jdowell:Qwe123_country-us@geo.iproyal.com:22323'
#     }

#     headers = {
#         'authority': 'i3zwhsu375dqllo5srv5vn35ba.appsync-api.us-west-2.amazonaws.com',
#         'accept': '*/*',
#         'accept-language': 'en-US,en;q=0.9',
#         'origin': 'https://www.defined.fi',
#         'referer': 'https://www.defined.fi/',
#         'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"Windows"',
#         'sec-fetch-dest': 'empty',
#         'sec-fetch-mode': 'cors',
#         'sec-fetch-site': 'cross-site',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
#         'x-amz-user-agent': 'aws-amplify/3.0.4',
#         'x-api-key': 'da2-vkmqkh3wlngdfktfeybq6j44li',
#     }

#     all_requests = (grequests.post('https://i3zwhsu375dqllo5srv5vn35ba.appsync-api.us-west-2.amazonaws.com/graphql?internal_outsize_id=' + str(token['internal_id']),
#                         headers=headers,
#                         json={
#                             'operationName': 'GetBars',
#                             'variables': {
#                                 'symbol': token['symbol'],
#                                 'from': token['from'],
#                                 'to': token['to'],
#                                 'resolution': token['resolution'],
#                                 'currencyCode': token['currencyCode']
#                             },
#                             'query': 'query GetBars($symbol: String!, $from: Int!, $to: Int!, $resolution: String!, $currencyCode: String) {\n  getBars(\n    symbol: $symbol\n    from: $from\n    to: $to\n    resolution: $resolution\n    currencyCode: $currencyCode\n  ) {\n    o\n    h\n    l\n    c\n    t\n    s\n    volume\n    __typename\n  }\n}\n',
#                         },
#                         # proxies=proxies,
#                         timeout=10) for token in tokens)

#     all_responses = grequests.map(all_requests)

#     results = {}

#     for response in all_responses:
#         try:
#             parsed_request_url = urlparse(response.url)
#             internal_id = parse_qs(parsed_request_url.query)['internal_outsize_id'][0]

#             # pair_id = json.loads(response.request.body)['variables']['symbol']
#             prices_per_minute = json.loads(response.text)['data']['getBars']['c']

#             last_index = 1440 if len(prices_per_minute) == 1441 else 1439
            
#             prices = {
#                 "0": prices_per_minute[0], "1": prices_per_minute[60],  "2": prices_per_minute[120],  "3": prices_per_minute[180],  "4": prices_per_minute[240],  "5": prices_per_minute[300], "6": prices_per_minute[360],
#                 "7": prices_per_minute[420],  "8": prices_per_minute[480],  "9": prices_per_minute[540],  "10": prices_per_minute[600], "11": prices_per_minute[660], "12": prices_per_minute[720],
#                 "13": prices_per_minute[780], "14": prices_per_minute[840], "15": prices_per_minute[900], "16": prices_per_minute[960], "17": prices_per_minute[1020], "18": prices_per_minute[1080],
#                 "19": prices_per_minute[1040], "20": prices_per_minute[1100], "21": prices_per_minute[1160], "22": prices_per_minute[1240], "23": prices_per_minute[1300], "24": prices_per_minute[1360],
#                 "25": prices_per_minute[last_index]
#             }

#             results[internal_id] = prices

#         except Exception as e:
#             print(e)

#     return results

# tokens = [
#     {'symbol': '0x7418f5a2621e13c05d1efbd71ec922070794b90a:42161', 'from': 1665617473, 'to': 1665703873, 'resolution': '1', 'currencyCode': 'USD', 'internal_id': 'test'},
#     {'symbol': '0x7418f5a2621e13c05d1efbd71ec922070794b90a:42161', 'from': 1665617473, 'to': 1665703873, 'resolution': '1', 'currencyCode': 'USD', 'internal_id': 'best'}
# ]

# results = getDetails(tokens)

# print(results['best'])