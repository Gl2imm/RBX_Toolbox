import pytest

from pyjwt_key_fetcher.utils import unsigned_int_to_urlsafe_b64 as int_to_b64
from pyjwt_key_fetcher.utils import urlsafe_b64_to_unsigned_int as b64_to_int


@pytest.mark.parametrize(
    "r",
    [
        range(256),
        range(1023, 1025),
        range(65534, 65537),
    ],
)
def test_urlsafe_b64_range(r):
    for i in r:
        assert i == b64_to_int(int_to_b64(i))


@pytest.mark.parametrize(
    "b64,n",
    [
        ("AQAB", 65537),
        (
            "0DHxYa34gOatw7Swjbaz3Q8WnCXj_l41ua5bAiMHJxERNYeUbRbD4ZNNq3-v45EZCJSaHAdVbI"
            "CjdaZlJMbVAJQjtGPaYgDUljcJkyUE5MTNzyPAsgngoxUfHrU41fe3uKQiKHRmAJwGyaiUBrrT"
            "JNHRYEXJJ1MFJgizvcs-yCraO1cv3avivTt11cqEsuSp55pMLzqyIpY25WoMqL0IeGIKNjp1dw"
            "oyR7pDfEzZZ0t_HhxMWeNxlUvM2r3fJw03kh0F6xrgoTggOjCeh3washg8_ho9skUooxaJ8kel"
            "k4qsdR8cLdrmQQYTAHBPAVikyW5hzXylsKNgZp_hu3nLdQ",
            int(
                "2628219519320300764339518752236154305720277346740633174778610362176818"
                "7352908803787663496643793861385879314431513265520431475673167797780714"
                "0523435400761548582649753235056621680542037921516141071771521768378340"
                "5068936943241746252535929916933808667671818597994703183333289425171865"
                "2065847391841275698356610229540681225062805781551455046411174885228243"
                "5211561828298583402269373480588622335765357651784722409142704622125897"
                "3452167940344329182958136271774466353500459556940824396308810334507365"
                "8418381614749247702588819966141309494029193213216098713406891901830543"
                "427446028147125258919165162321999893002443015723977132917"
            ),
        ),
    ],
)
def test_urlsafe_b64_known_values(b64, n):
    assert n == b64_to_int(b64)
    assert b64 == int_to_b64(n)
