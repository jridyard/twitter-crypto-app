let data = await fetch_post (
    FETCH_URL = 'https://24apwohq76klnuvisso2hiyzxa0bcvzv.lambda-url.us-west-2.on.aws/',
    REQUEST_BODY = { // Pass JSON => It will get stringified in the function
        'tokens': [{"symbol": "0x7418f5a2621e13c05d1efbd71ec922070794b90a:42161", "from": 1665617473, "to": 1665703873, "resolution": "1", "currencyCode": "USD", "internal_id": "test"}]
    },
    HEADERS = {
        'content-type': 'application/json'
    }
)

async function fetch_post ( FETCH_URL, REQUEST_BODY, HEADERS, REQUEST_METHOD = 'POST' ) {

    const RESPONSE = await fetch( FETCH_URL, {
                    'method': REQUEST_METHOD,
                    'body': JSON.stringify( REQUEST_BODY ),
                    'headers': new Headers( HEADERS )
                }).then((response) => response.json())
                .then((data) => {
                    return data
                })
                .catch(err => {
                    console.error(`
                        Error occured on request for URL: ${ FETCH_URL }. \n
                        Error details: ${ err.toString() }
                    `)
                    return err
                })

    return RESPONSE

}