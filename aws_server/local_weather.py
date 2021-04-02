import requests, json
def get_weather(lng, lat):
    key = "1d12e6fca4c00e1cf768ac0434ee4eee"
    url = "http://api.openweathermap.org/data/2.5/weather?lat=%s&lon=%s&units=%s&APPID=%s" % (lat, lng, "imperial", key)
    res = json.loads(requests.get(url).text)
    weather= res["weather"][0]
    desc = weather["description"]
    main = res["main"]
    temp = main["temp"]
    return (temp, desc)
