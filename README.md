# python-module
Accessing the API with a python module.



## Documentation

#### Get all items

```
  query()
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `questionType` | `string` | The type of question to search for. Defaults to "all". <br> L|


#### Get item

```
  GET /api/items/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of item to fetch |

#### add(num1, num2)

Takes two numbers and returns the sum.

