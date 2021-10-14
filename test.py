import requests

BASEURL = "http://127.0.0.1:5000/"

response = requests.post(BASEURL + "loginuser",{"name":"rohit","email":"rohit@gmail.com","password":"rohit"})
print(response)

#everytime we return sometype of information from our api we need to make sure that information is serializable
