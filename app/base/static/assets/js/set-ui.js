fetch("/api/get_theme", {
    "method": "GET",
}).then((response) => response.json())
.then((data) => {
    console.log('got theme')
    console.log(data)
    return data
});