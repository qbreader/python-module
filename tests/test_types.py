"""Test the types, classes, and structures used by the qbreader library."""


import qbreader as qb
from qbreader.types import Bonus, Tossup


class TestTossup:
    """Test the Tossup class."""

    tu_json = {
        "_id": "64a0ccb31634f2d5eb7df02a",
        "question": "This general class of devices could move between hypothetical castles via up and down escalators in a cycler. These devices can transfer their angular momentum to two “yo-yo” masses attached with cords in order to decrease their rotation rate. The Oberth effect describes how these devices gain kinetic energy more efficiently while at (*) periapsis. Hohmann transfers and bi-elliptic transfers are used to adjust the altitude of these devices. The trajectory-dependent delta-v budget of one of these devices can be reduced by using a slingshot maneuver. Station-keeping can help these objects remain geosynchronous. For 10 points, name this general class of devices used to collect astronomical data, such as Voyager 1.",  # noqa: E501
        "formatted_answer": "<b><u>spacecraft</u></b> [or <b><u>spaceship</u></b>s; accept <b><u>space probe</u></b>s, <b><u>satellite</u></b>s, or <b><u>space station</u></b>s, or <b><u>space vehicle</u></b>s; prompt with <u>rocket</u>s or <u>thruster</u>s with, “To what devices are rockets attached?”] (The first clue describes the Aldrin cycle, proposed by Buzz Aldrin.)",  # noqa: E501
        "answer": "spacecraft [or spaceships; accept space probes, satellites, or space stations, or space vehicles; prompt with rockets or thrusters with, “To what devices are rockets attached?”] (The first clue describes the Aldrin cycle, proposed by Buzz Aldrin.)",  # noqa: E501
        "category": "Science",
        "subcategory": "Other Science",
        "packet": "64a0ccb31634f2d5eb7df01e",
        "set": "64a0ccb31634f2d5eb7deed5",
        "setName": "2023 MRNA",
        "setYear": 2023,
        "type": "tossup",
        "packetNumber": 9,
        "packetName": "09",
        "questionNumber": 12,
        "createdAt": "2023-07-02T01:02:43.628Z",
        "updatedAt": "2023-07-02T01:03:31.712Z",
        "difficulty": 7,
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
        "_id": "644932c99f0045ff841d6792",
        "leadin": "Using this metal as a charge carrier avoids both cross-contamination and electrodeposition because it has four stable oxidation states: plus-two, plus-three, plus-four, and plus-five. For 10 points each:",  # noqa: E501
        "parts": [
            "Name this transition metal used as the charge carrier in the most common redox flow battery for electric grids.",  # noqa: E501
            "To balance charge between the pipes, redox flow batteries rely on one of these semipermeable barriers made of Nafion. They also separate the compartments of fuel cells.",  # noqa: E501
            "The electrolyte of a vanadium redox flow battery is a solution of this compound. This “acid” in a lead-acid battery is prepared using a vanadium catalyst in the contact process.",  # noqa: E501
        ],
        "values": [],
        "answers": [
            "vanadium [or V]",
            "proton-exchange membranes [or PEMs; or polymer-electrolyte membranes; prompt on membranes orion-exchange membranes]",  # noqa: E501
            "sulfuric acid [or H2SO4]",
        ],
        "formatted_answers": [
            "<b><u>vanadium</u></b> [or <b><u>V</u></b>]",
            "<b><u>proton-exchange membrane</u></b>s [or <b><u>PEM</u></b>s; or polymer-<b><u>electrolyte membrane</u></b>s; prompt on <u>membrane</u>s orion-exchange <u>membrane</u>s]",  # noqa: E501
            "<b><u>sulfuric</u></b> acid [or <b><u>H2SO4</u></b>]",
        ],
        "category": "Science",
        "subcategory": "Chemistry",
        "packet": "644932c99f0045ff841d6777",
        "set": "644932c99f0045ff841d66fb",
        "setName": "2023 ACF Nationals",
        "setYear": 2023,
        "type": "bonus",
        "packetNumber": 4,
        "packetName": "Finals 2. Editors 12",
        "questionNumber": 7,
        "createdAt": "2023-04-26T14:18:49.683Z",
        "updatedAt": "2023-04-26T14:19:23.999Z",
        "difficulty": 9,
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
