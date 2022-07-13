import requests
from bs4 import BeautifulSoup

showSteps = True
showValues = True
checkURL = True #Make false if the target website has bot detection

class Target():
  def __init__(self, html: str):
    self.html = BeautifulSoup(html, "html.parser")
    self.directions = []
  
  def narrow(self):
    print(self.html.prettify())
    element = str(input("What is the next element?"))
    lis = self.html.find_all(element)
    print(len(lis))
    for index, value in enumerate(lis): print(f"{index}: {value.prettify()}\n")
    IOE = int(input("What is the index of the target element? ")) #Index of Element
    self.html = lis[IOE]
    self.directions.append([element, IOE])
    again = str(input("Do you wish to continue (y/n)? "))
    if again == "y":
      return True
    elif again == "n":
      return False
    else:
      print("Invalid Answer. Please use a \"y\" for yes and a \"n\" for no.")
      print("Assuming that another level is needed.")
      return True

  def deepdive(self):
    again = True
    while again:
      again = self.narrow()
      
def followDirections(html, directions):
  html = BeautifulSoup(html, "html.parser")
  for i in directions:
    html = html.find_all(i[0])[i[1]]
  return html

class Website():
  def __init__(self, URL: str, checkURL=False):
    if checkURL:
      try:
        requests.get(URL) # checks that the url is valid
      except requests.models.MissingSchema or NameError or ConnectionError:
        return "Invalid URL"
    self.URL = URL
    self.headers = {}
    self.cookies = {}
  
  def getHeaders(self, headers: str, method: str): #This method does as the name suggests, it creates the headers and separates them in the self.headers dictionary by method.
    headers_dict = {}
    head = headers.split(": ")
    head = [i.split(" ") for i in head]
    next = []
    for i in range(len(head)):
      if i >= len(head)-2:
        equal = ""
        for l in head[i+1]:
          equal += f"{l} "
        equal = equal[:-1]
        if head[i][-1][0] == ":":
          head[i][-1] = head[i][-1][1:]
        headers_dict[head[i][-1]] = equal
        break
      else:
        equal = ""
        for l in head[i+1][:-1]:
          equal += f"{l} "
        equal = equal[:-1]
        if head[i][-1][0] == ":":
          head[i][-1] = head[i][-1][1:]
        headers_dict[head[i][-1]] = equal
    if "cookies" in headers_dict.keys():
      self.getCookies(headers_dict["cookies"])
      del headers_dict["cookies"]
    if "accept-encoding" in headers_dict.keys():
      if "br" in headers_dict["accept-encoding"]:
        hello = headers_dict["accept-encoding"].split(", ")
        hello.remove("br")
        end = ""
        for i in hello:
          end += f"{i}, "
        end = end[:-2]
        headers_dict["accept-encoding"] = end
    self.headers[method] = headers_dict

  def getCookies(self, cookies: str): #"Extension" of the getHeaders method. Makes a dictionary for cookies, but not separated by method.
    cookies_dict = {}
    for i in cookies.split("&"):
      datum = i.split("=")
      cookies_dict[datum[0]] = datum[1]
    self.cookies = cookies_dict

  def get(self):
    return requests.get(self.URL, headers=self.headers["GET"], cookies=self.cookies)
  
  def post(self):
    return requests.post(self.URL, data={}, json={}, headers=self.headers["POST"], cookies=self.cookies) #TODO: update POST method to actually have data :)

if __name__ == "__main__":
  website = Website(input("Hello\nWhat website would you like to scrape? "), checkURL=True)
  #-------------Above is fine-------------
  website.getHeaders(input("Please paste an example of the headers of a request to the website:\n"), "GET")
  if showSteps: print("Headers object created")
  if showValues: print(website.headers)
  html = website.get()
  if showSteps: print(f"----------------------------- Status: {html.status_code} -----------------------------")
  if True:#"content_type" in html.headers.keys() and html.headers["content-type"].split("; ")[0] == "text/html":
    targets = []
    n = int(input("How many elements do you wish to scrape?\n"))
    for i in range(n):
      target = Target(html.text)
      target.deepdive()
      targets.append(target)
    for i in targets:
      print(i.directions)
      print(followDirections(html.text, i.directions).text)
