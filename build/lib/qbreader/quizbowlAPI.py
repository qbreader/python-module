import requests

base = "https://www.qbreader.org/api"

def query(questionType:str = "all", searchType:str = "all", queryString:str = "", regex:bool = False, randomize:bool = False, setName:str = "", difficulties:dict = [], categories:dict = [], subcategories:dict = [], maxQueryReturnLength:int = None) -> dict: 
    """
    Search the QBreader database.

    This function searches the QBreader database for questions that match the parameters specified.

    Parameters
    ----------
    questionType : str, must be one of "all", "tossup", "bonus"
        The type of question to search for. Defaults to "all". If one of the three is not set, returns a 400 Bad Request.
    searchType : str, must be one of "all", "answer", "question"    
        The type of search to perform. Defaults to "all". If one of the three is not set, returns a 400 Bad Request.
    queryString : str (optional)
        The string to search for. Defaults to "".
    regex : str (optional)
        Whether or not to use regular expressions for the queryString. Defaults to "false".
    randomize : str (optional)
        Whether or not to randomize the order of the results. Defaults to "false".
    setName : str (optional)
        The name of the set to search. Defaults to "". Leave as an empty string to search all.
    difficulties : list (optional)
        The difficulties to search for. Defaults to []. Leave as an empty list to search all. Must be a list of ints from 1 to 10.
    categories : list (optional) 
        The categories to search for. Defaults to []. Leave as an empty list to search all.
    subcategories : list (optional)
        The subcategories to search for. Defaults to []. Leave as an empty list to search all.
    maxQueryReturnLength : int (optional)
        The maximum number of questions to return. Defaults to None. Leave blank to return 50. Anything over 200 will not work.
    
    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    
    """
    regex_converted = str(regex).lower()
    random_converted = str(randomize).lower()
    url = base + "/query"

    data = {
        "questionType": questionType,
        "searchType": searchType,
        "queryString": queryString,
        "regex": regex_converted,
        "randomize": random_converted,
        "setName": setName,
        "categories": categories,
        "subcategories": subcategories,
        "difficulties": difficulties,
        "maxQueryReturnLength": maxQueryReturnLength

    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def random_question(questionType:str, difficulties:dict = [], categories:dict = [], subcategories:dict = [], number:int = None) -> list: 
    """
    Get a random question from the QBreader database.

    This function gets a random question from the QBreader database.

    Parameters
    ----------
    questionType : str, must be one of "all", "tossup", "bonus" 
        The type of question to search for (tossup or bonus). If one of the two is not set, returns a 400 Bad Request.
    difficulties : list (optional)
        The difficulties to search for. Defaults to []. Leave as an empty list to search all. Must be a list of ints from 1 to 10.
    categories : list (optional)
        The categories to search for. Defaults to []. Leave as an empty list to search all.
    subcategories : list (optional)
        The subcategories to search for. Defaults to []. Leave as an empty list to search all.
    number : int (optional)
        The number of questions to return. Defaults to None. Leave blank to return 1.
    
    Returns
    ----------
    list
        A list containing the results of the search.

    """
    url = base + "/random-question"

    data = {
        "questionType": questionType,
        "categories": categories,
        "subcategories": subcategories,
        "difficulties": difficulties,
        "number": number
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def random_name() -> str:
    '''
    Get a random name from the QBreader database.

    This function Generates an adjective-noun pair (used in multiplayer lobbies).

    Takes no parameters.

    Returns
    ----------
    str
        A string containing the random name.

    '''
    url = base + "/random-name"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        return str(response.status_code) + " bad request"

def packet(setName:str, packetNumber:int) -> dict:
    '''
    Get a packet from the QBreader database.

    This function gets questions from a packet from the QBreader database.

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    packetNumber : int
        The number of the packet to search for.
    
    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    '''
    url = base + "/packet"
    data = {
        "setName": setName,
        "packetNumber": packetNumber
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def packet_tossups(setName:str, packetNumber:int) -> dict:
    '''
    Get a packet's tossups from the QBreader database.

    This function gets a packet's tossups from the QBreader database. Twice as fast as using packet().

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    packetNumber : int
        The number of the packet to search for.
    
    Returns
    ----------
    dict
        A dictionary containing the results of the search.

    '''

    url = base + "/packet-tossups"
    data = {
        "setName": setName,
        "packetNumber": packetNumber
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def packet_bonuses(setName:str, packetNumber:int) -> dict:
    '''
    Get a packet's bonuses from the QBreader database.

    This function gets a packet's bonuses from the QBreader database. Twice as fast as using packet().

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    packetNumber : int
        The number of the packet to search for.
    
    Returns
    ----------
    dict
        A dictionary containing the results of the search.

    '''
    url = base + "/packet-bonuses"
    data = {
        "setName": setName,
        "packetNumber": packetNumber
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def num_packets(setName:str) -> dict:
    '''
    Get the number of packets in a set from the QBreader database.

    This function gets the number of packets in a set from the QBreader database.

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    
    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    '''
    url = base + "/num-packets"
    data = {
        "setName": setName,
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def set_list() -> list:
    '''
    Get a list of sets from the QBreader database.

    This function gets a list of sets from the QBreader database.

    Takes no parameters.

    Returns
    ----------
    list
        A list containing the results of the search.
    '''
    url = base + "/set-list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def room_list() -> dict:
    '''
    Get a list of rooms from the QBreader database.

    This function gets a list of rooms from the QBreader database.

    Takes no parameters.

    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    '''
    url = base + "/multiplayer/room-list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return str(response.status_code) + " bad request"

def report_question(_id:str, reason:str = None, description:str = None) -> int: 
    """
    Report a question from the QBreader database.
    
    This function reports a question from the QBreader database.

    Parameters
    ----------
    _id : str
        The ID of the question to report.
    reason : str (optional)
        The reason for reporting the question. Defaults to None.
    description : str (optional)
        A description of the reason for reporting the question. Defaults to None.
    
    Returns
    ----------
    int
        The status code of the request. 200 if successful, 400 if not.
    """
    url = base + "/random-question"

    data = {
        "_id": _id,
        "reason": reason,
        "description": description
    }

    response = requests.post(url, json=data)

    return response.status_code
