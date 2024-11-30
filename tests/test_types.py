"""Test the types, classes, and structures used by the qbreader library."""

import qbreader as qb
from qbreader.types import Bonus, Tossup, PacketMetadata, SetMetadata


class TestTossup:
    """Test the Tossup class."""

    tu_json = {
        "_id": "64046cc6de59b8af97422da5",
        "question": "<b>Radiative power is inversely proportional to this quantity cubed, times 6-pi-epsilon, according to the Larmor formula. This quantity is in the numerator in the formula for the index of refraction. When a charged particle exceeds this quantity while in a medium, it produces Cherenkov radiation. This </b>(*) quantity is equal to one divided by the square root of the product of the vacuum permittivity and permeability. This quantity is constant in all inertial reference frames. For 10 points, name this value symbolized <i>c</i>, that is about 30 million meters per second.",
        "answer": "<b><u>Speed of Light</u></b>",
        "category": "Science",
        "subcategory": "Physics",
        "packet": {"_id": "64046cc6de59b8af97422da2", "name": "03", "number": 3},
        "set": {
            "_id": "64046cc6de59b8af97422d4f",
            "name": "2017 WHAQ",
            "year": 2017,
            "standard": True,
        },
        "createdAt": "2023-03-05T10:19:50.469Z",
        "updatedAt": "2024-11-24T22:47:40.013Z",
        "difficulty": 3,
        "number": 3,
        "answer_sanitized": "Speed of Light",
        "question_sanitized": "Radiative power is inversely proportional to this quantity cubed, times 6-pi-epsilon, according to the Larmor formula. This quantity is in the numerator in the formula for the index of refraction. When a charged particle exceeds this quantity while in a medium, it produces Cherenkov radiation. This (*) quantity is equal to one divided by the square root of the product of the vacuum permittivity and permeability. This quantity is constant in all inertial reference frames. For 10 points, name this value symbolized c, that is about 30 million meters per second.",
    }

    def test_from_json(self):
        """Test the from_json() classmethod."""
        assert Tossup.from_json(self.tu_json)

    def test_eq(self):
        """Test the __eq__ method."""
        tu1 = Tossup.from_json(self.tu_json)
        tu2 = Tossup.from_json(self.tu_json)
        assert tu1 == tu2
        assert tu1 != self.tu_json

    def test_str(self):
        """Test the __str__ method."""
        tu = Tossup.from_json(self.tu_json)
        assert str(tu) == tu.question


class TestBonus:
    """Test the Bonus class."""

    b_json = {
        "_id": "673ec00f90236da031c2cedb",
        "leadin": "With George Jean Nathan, H. L. Mencken co-founded a newspaper called<i> The</i> [this adjective]<i> Mercury</i>, which eventually fell under far-right leadership. For 10 points each:",
        "leadin_sanitized": "With George Jean Nathan, H. L. Mencken co-founded a newspaper called The [this adjective] Mercury, which eventually fell under far-right leadership. For 10 points each:",
        "parts": [
            "Name this adjective in the title of a Mencken book that pays homage to Noah Webster. That book claims that the sentence “who are you talking to” is “doubly” this adjective since it forgoes “whom” and puts a preposition at the end of a sentence.",
            "<i> The Baltimore Sun</i> sent Mencken to cover one of these events in Dayton, Tennessee, where he gave it a famous nickname. That event of this type was fictionalized in the play<i> Inherit the Wind</i>.",
            "At the end of<i> Inherit the Wind</i>, Henry Drummond picks up a book by Darwin in one hand and this book with the other. Mencken claimed to have coined the term for a “Belt” in the Southern United States named for this text.",
        ],
        "parts_sanitized": [
            'Name this adjective in the title of a Mencken book that pays homage to Noah Webster. That book claims that the sentence "who are you talking to" is "doubly" this adjective since it forgoes "whom" and puts a preposition at the end of a sentence.',
            "The Baltimore Sun sent Mencken to cover one of these events in Dayton, Tennessee, where he gave it a famous nickname. That event of this type was fictionalized in the play Inherit the Wind.",
            'At the end of Inherit the Wind, Henry Drummond picks up a book by Darwin in one hand and this book with the other. Mencken claimed to have coined the term for a "Belt" in the Southern United States named for this text.',
        ],
        "answers": [
            "<b><u>American</u></b> [accept<i> The</i> <i><b><u>American</u></b> Mercury</i> or<i> The</i> <i><b><u>American</u></b> Language</i>]",
            "<b><u>trial</u></b> [accept Scopes <b><u>trial</u></b> or Scopes Monkey <b><u>trial</u></b>]",
            "the <b><u>Bible</u> </b>",
        ],
        "answers_sanitized": [
            "American [accept The American Mercury or The American Language]",
            "trial [accept Scopes trial or Scopes Monkey trial]",
            "the Bible",
        ],
        "updatedAt": "2024-11-21T05:07:27.318Z",
        "category": "Literature",
        "subcategory": "American Literature",
        "alternate_subcategory": "Misc Literature",
        "values": [10, 10, 10],
        "difficultyModifiers": ["h", "m", "e"],
        "number": 1,
        "createdAt": "2024-11-21T05:07:27.318Z",
        "difficulty": 7,
        "packet": {
            "_id": "673ec00f90236da031c2cec6",
            "name": "A - Claremont A, Edinburgh A, Haverford A, Georgia Tech B, Illinois C, Michigan B",
            "number": 1,
        },
        "set": {
            "_id": "673ec00f90236da031c2cec5",
            "name": "2024 ACF Winter",
            "year": 2024,
            "standard": True,
        },
    }

    def test_from_json(self):
        """Test the from_json() classmethod."""
        assert Bonus.from_json(self.b_json)

    def test_eq(self):
        """Test the __eq__ method."""
        b = Bonus.from_json(self.b_json)
        b = Bonus.from_json(self.b_json)
        assert b == b
        assert b != self.b_json

    def test_str(self):
        """Test the __str__ method."""
        b = Bonus.from_json(self.b_json)
        assert str(b) == "\n".join(b.parts)


class TestPacket:
    """Test the Packet class."""

    packet = qb.Sync().packet("2023 MRNA", 5)

    def test_eq(self):
        """Test the __eq__ method."""
        p1 = p2 = self.packet
        assert p1 == p2
        assert p1 != "not a packet"

    def test_str(self):
        """Test the __str__ method."""
        assert str(self.packet)

    def test_iter(self):
        """Test the __iter__ method."""
        for i, (tu, b) in enumerate(self.packet):
            assert tu == self.packet.tossups[i]
            assert b == self.packet.bonuses[i]


class TestPacketMetadata:
    """Test the PacketMetadata class."""

    packetMetadata = PacketMetadata.from_json(TestTossup.tu_json["packet"])

    def test_eq(self):
        """Test the __eq__ method."""
        p1 = p2 = self.packetMetadata
        assert p1 == p2
        assert p1 != "not packet metadata"

    def test_str(self):
        """Test the __str__ method."""
        assert str(self.packetMetadata)


class TestSetMetadata:
    """Test the SetMetadata class."""

    setMetadata = SetMetadata.from_json(TestTossup.tu_json["set"])

    def test_eq(self):
        """Test the __eq__ method."""
        s1 = s2 = self.setMetadata
        assert s1 == s2
        assert s1 != "not set metadata"

    def test_str(self):
        """Test the __str__ method."""
        assert str(self.setMetadata)


class TestQueryResponse:
    """Test the QueryResponse class."""

    query = qb.Sync().query(queryString="spacecraft", maxReturnLength=1)

    def test_str(self):
        """Test the __str__ method."""
        assert str(self.query)


class TestAnswerJudgement:
    """Test the AnswerJudgement class."""

    judgement = qb.Sync().check_answer("spacecraft", "spacecraft")

    def test_str(self):
        """Test the __str__ method."""
        assert str(self.judgement)
