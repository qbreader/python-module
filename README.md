# python-module
Accessing the API with a python module.



## Documentation

#### Search the QBreader database

```
  query()
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `questionType` | `string` | The type of question to search for. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `searchType` | `string` | The type of search to perform. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `queryString` | `string` | The string to search for. Defaults to "". |
| `regex` | `string` | Whether or not to use regular expressions for the queryString. Defaults to "false". |
| `randomize` | `string` | Whether or not to randomize the order of the results. Defaults to "false". |
| `setName` | `string` | The difficulties to search for. Defaults to []. Leave as an empty list to search all. Must be a list of ints from 1 to 10. |
| `difficulties` | `list` | The string to search for. Defaults to "". |
| `categories` | `list` | The categories to search for. Defaults to []. Leave as an empty list to search all. |
| `subcategories` | `list` | The subcategories to search for. Defaults to []. Leave as an empty list to search all. |
| `maxQueryReturnLength` | `int` | The maximum number of questions to return. Defaults to None. Leave blank to return 50. Anything over 200 will not work. |


#### Get a random question from the QBreader database

```
  random_question()
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `questionType` | `string` | The type of question to search for. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `difficulties` | `list` | The string to search for. Defaults to "". |
| `categories` | `list` | The categories to search for. Defaults to []. Leave as an empty list to search all. |
| `subcategories` | `list` | The subcategories to search for. Defaults to []. Leave as an empty list to search all. |
| `number` | `int` | The number of questions to return. Defaults to None. Leave blank to return 1.|
