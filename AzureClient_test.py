from AzureClient import client

def test_client():
    response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": "This is a test message. Answer 'Test Succeeded' if you can read this."}]
    )
    assert response.choices[0].message.content == "Test Succeeded"