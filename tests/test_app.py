from racing_pkg import report
import json

def test_landing(client):

    landing = client.get("api/v1/report?format=yaml")
    html = landing.data.decode()

    assert landing.status_code == 200
    assert "please, check your request" in html
  

def test_landing_rep_xml(client):

    landing_rep_desc = client.get("api/v1/report?format=xml")
    xml = landing_rep_desc.data.decode()

    assert landing_rep_desc.status_code == 200
    assert landing_rep_desc.headers["Content-Type"] == "application/xml; charset=utf-8"
    assert "<root>" in xml
    assert '<Name type="str">' in xml
    assert "</Result_Time>" in xml
  

def test_landing_rep_json(client):

    landing_rep_desc = client.get("api/v1/report")
    json_text = json.loads(landing_rep_desc.data.decode())

    assert landing_rep_desc.status_code == 200
    assert landing_rep_desc.headers["Content-Type"] == "application/json"

    assert "Abbreviation" in json_text[1]
    assert "Company" in json_text[1]
    assert "Name" in json_text[1]
  

def test_landing_rep_desc(client):

    landing_rep_desc = client.get("api/v1/report?format=xml&order=desc")
    xml = landing_rep_desc.data.decode()
    assert landing_rep_desc.headers["Content-Type"] == "application/xml; charset=utf-8"
    assert landing_rep_desc.status_code == 200
    assert "<root>" in xml
    assert '<Name type="str">' in xml
    assert "</Result_Time>" in xml


def test_landing_rep_descjson(client):

    landing_rep_desc = client.get("api/v1/report?format=json&order=desc")
    
    json_text = json.loads(landing_rep_desc.data.decode())
    assert landing_rep_desc.headers["Content-Type"] == "application/json"

    assert landing_rep_desc.status_code == 200

    assert "Abbreviation" in json_text[1]
    assert "Company" in json_text[1]
    assert "Name" in json_text[1]


def test_driverxml(client):
   
    landing_driver = client.get("api/v1/detail?driver_id=CLS&format=xml")
    xml = landing_driver.data.decode()
     
    assert landing_driver.status_code == 200
    assert landing_driver.headers["Content-Type"] == "application/xml; charset=utf-8"
    
    assert "<root>" in xml
    assert '<Name type="str">' in xml
    assert "</Result_Time>" in xml
    assert '<Name type="str">Charles Leclerc</Name>' in xml
    assert '<Company type="str">SAUBER FERRARI</Company>' in xml


def test_driverjson(client):
   
    landing_driver = client.get("api/v1/detail?driver_id=CLS&format=json")
    json_text = json.loads(landing_driver.data.decode())
     
    assert landing_driver.status_code == 200
    assert landing_driver.headers["Content-Type"] == "application/json"

    assert json_text["Abbreviation"] == 'CLS'
    assert json_text["Company"] == "SAUBER FERRARI"
    assert json_text["Name"] == "Charles Leclerc"
  
  
def test_landing_driver(client):

    landing = client.get("api/v1/detail?driver_id=CLS&format=yaml")
    html = landing.data.decode()

    assert landing.status_code == 200
    assert "please check your request" in html 


def test_driverjson_fail(client):
   
    landing_driver = client.get("api/v1/detail?driver_id=XXX&format=json")
    html = landing_driver.data.decode()
     
    assert landing_driver.status_code == 200
    assert "there is no such driver" in html


def test_driverxml_fail(client):
   
    landing_driver = client.get("api/v1/detail?driver_id=XXX&format=xml")
    html = landing_driver.data.decode()
     
    assert landing_driver.status_code == 200
    assert "there is no such driver" in html
 