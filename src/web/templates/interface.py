import httplib
conn = httplib.HTTPConnection("46.101.225.178","5000")
conn.request("GET", "/api/v1/hr/lexicon")
r1 = conn.getresponse()
print r1.status, r1.reason

data1 = r1.read()

conn.close()