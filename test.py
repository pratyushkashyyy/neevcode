import requests

class api:
    def register(self):
        url = "http://172.20.10.2:5000/register"

        data = {
            "username" : "pratyushkashy",
            "password" : "password",
            "first_name" : "pratyush",
            "last_name" : "kashyap",
            "phoneno" : "8406909448"

        }


        response = requests.post(url, data=data)
        print(response.text)

    def add_product(self):
        url = "http://172.20.10.2:5000/add_product"

        data = {
            "product_name" : "CyberSec",
            "price" : "2500",
            "image_url" : "https://cdn-icons-png.flaticon.com/512/1754/1754435.png",
            "description" : "hello this is cybersec course blaah blahh blahh .....",
            "level" : "beginner",
            "classes" : '30 days',
            "audience" : 'child',
            "rating" : '4'
        }
        response = requests.post(url,data=data)
        if response.status_code == 200:
            print("Course Added !!")
        else:
            print("some error occured")
api_instance = api()
api_instance.add_product()