import os
from dotenv import load_dotenv
from binance_local.main import client_factory
from binance.client import Client
import pytest
load_dotenv()

def test_retrieve_keys():
    FAKE_API_KEY = os.getenv("FAKE_API_KEY")
    FAKE_SECRET_KEY = os.getenv("FAKE_SECRET_KEY")
    print("testing if dotenv is loading correctly the values from the .environment..")
    print(f"fake api key is {FAKE_API_KEY} and expected asdedasdaewadssdaedadswdaw")
    print(f"fake secret key is {FAKE_SECRET_KEY} and expected fegtgfsgrsgrgesrg")
    assert FAKE_API_KEY == "R4tskJnmicCcVmSSCGqDhyqBAYhnOUc7kAkcGxjdkMos9717knk3dH1jACfCiO8r" and FAKE_SECRET_KEY == "uefO3EA1EqtcANZJ6CVU3PYXMMvNYAdNCbqCoTEkodmgg6DPJCoQA9qmNXk97HGg"

@pytest.mark.asyncio
async def test_client_factory():
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")
    client = await client_factory(api_key=API_KEY, secret_key=SECRET_KEY)
    assert type(client) is type(Client) 