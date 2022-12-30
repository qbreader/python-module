# QBreader Python API wrapper module
Accessing the QBreader API with a python wrapper module.

## Documentation

#### Search the QBreader database

```
  query()
```
This function searches the QBreader database for questions that match the parameters specified.

| Parameter | Type     |Values| Description                |
| :-------- | :------- |:----------|:------------------------- |
| `questionType` | `string` | The type of question to search for. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `searchType` | `string` | The type of search to perform. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `queryString` | `string` | The string to search for. Defaults to "". |
| `regex` | `bool` | Whether or not to use regular expressions for the queryString. Defaults to "False". |
| `randomize` | `bool` | Whether or not to randomize the order of the results. Defaults to "False". |
| `setName` | `string` | The difficulties to search for. Defaults to []. Leave as an empty list to search all. Must be a list of ints from 1 to 10. |
| `difficulties` | `list` | The string to search for. Defaults to "". |
| `categories` | `list` | The categories to search for. Defaults to []. Leave as an empty list to search all. |
| `subcategories` | `list` | The subcategories to search for. Defaults to []. Leave as an empty list to search all. |
| `maxQueryReturnLength` | `int` | The maximum number of questions to return. Defaults to None. Leave blank to return 50. Anything over 200 will not work. |


#### Get a random question from the QBreader database

```
  random_question()
```
This function gets a random question from the QBreader database.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `questionType` | `string` | The type of question to search for (tossup or bonus). If one of the two is not set, returns a 400 Bad Request. |
| `difficulties` | `list` | The string to search for. Defaults to "". |
| `categories` | `list` | The categories to search for. Defaults to []. Leave as an empty list to search all. |
| `subcategories` | `list` | The subcategories to search for. Defaults to []. Leave as an empty list to search all. |
| `number` | `int` | The number of questions to return. Defaults to None. Leave blank to return 1.|

#### Generate a random name 

```
  random_question()
```
This function Generates an adjective-noun pair (used in multiplayer lobbies)

#### Get questions from a packet from the QBreader database

```
  packet()
```
This function gets questions from a packet from the QBreader database.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `setName` | `string` | The name of the set to search. Can be obtained from set_list().|
| `packetNumber` | `int` | The number of the packet to search for.|

#### Get a packet's tossups from the QBreader database

```
  packet_tossups()
```
This function gets a packet's tossups from the QBreader database. Twice as fast as using packet().

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `setName` | `string` | The name of the set to search. Can be obtained from set_list().|
| `packetNumber` | `int` | The number of the packet to search for.|

#### Get a packet's bonuses from the QBreader database

```
  packet_bonuses()
```
This function gets a packet's bonuses from the QBreader database. Twice as fast as using packet().

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `setName` | `string` | The name of the set to search. Can be obtained from set_list().|
| `packetNumber` | `int` | The number of the packet to search for.|

#### Get the number of packets in a set from the QBreader database

```
  packet_bonuses()
```
This function gets the number of packets in a set from the QBreader database

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `setName` | `string` | The name of the set to search. Can be obtained from set_list().|

#### Get a list of sets from the QBreader database 

```
  set_list()
```

This function gets a list of sets from the QBreader database.

#### Get a list of rooms from the QBreader database

```
  room_list()
```
This function gets a list of rooms from the QBreader database.

#### Report a question from the QBreader database

```
  report_question()
```
This function reports a question from the QBreader database.

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `_id` | `string` | The ID of the question to report.|
| `reason` | `string` | The reason for reporting the question. Defaults to None. |
| `description` | `string` | A description of the reason for reporting the question. Defaults to None.|
