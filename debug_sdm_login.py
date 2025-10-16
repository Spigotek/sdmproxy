import requests
import base64

url = "http://10.11.35.35:8050/caisd-rest/rest_access"
user = "vueuser"
password = "Vue@user123!"
b64 = base64.b64encode(f"{user}:{password}".encode()).decode()

headers = {
    "Content-Type": "application/xml;charset=UTF-8",
    "Authorization": f"Basic {b64}",
    "X-Obj-Attrs": "userid,REST_ACCESS_KEY"
}
body = "<rest_access/>"

resp = requests.post(url, headers=headers, data=body)
print("STATUS:", resp.status_code)
print("HEADERS:")
for k, v in resp.headers.items():
    print(f"  {k}: {v}")
print("\nCOOKIES:", resp.cookies.get_dict())
print("\nBODY:\n", resp.text)
