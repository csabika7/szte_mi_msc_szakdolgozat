from pathlib import Path


def test_prediction(client):
    resources = Path(__file__).parent / "resources"
    post_response = client.post("/v1/model/predict", data={
        "img": ((resources / "test_img.png").open("rb"), "test.png", "image/png")
    })
    assert post_response.status_code == 200
    assert post_response.data == b'1.0'
