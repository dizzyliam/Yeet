# Yeet

A self-hosted alternative to [dweet.io](https://dweet.io).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Although this will suffice for a live system, see deployment for notes on how to get the best out of it.

**Important: Currently only works with python2. Python3 support is the TO-DO.**

### Prerequisites

Make sure you have mongodb installed and running, then create a db with the name `yeet` and a user for that db with the name `admin` and a password of your choice. In the mongo shell, it should look something like this:

```
use yeet
db.createUser(
   {
     user: "admin",
     pwd: "<password>",
     roles: ["readWrite", "dbAdmin"]
   }
)
```

Use pip to install the requirements from requirements.txt:

```
pip install -r requirements.txt
```

### Starting Up

First, set an enviroment variable called `YEET_DB_PASS` with the password for the mongodb user you created as it's value. Optionally, you can set the enviroment variable `YEET_DB_EXPIRE` to define the number of seconds before a yeet will expire, but this will default to the sensible time of 12 hours if not set.

Once they are set, start the server:

```
python yeet.py
```

All set!

## Usage

A yeet server has two endpoints; `to` and `from`. A request to the `to` endpoint looks like this:

```
localhost:8080/to/YEETNAME?data=somesaucydata
```

With `YEETNAME` being the name of the yeet that you will use to retrieve the data, and the data parameter holding whatever data you want it to. The request will return JSON containing a machine-readable success indicator and the data that has been stored.

A request to the `from` endpoint looks like this:

```
localhost:8080/from/YEETNAME
```

With `YEETNAME` being the name of the yeet that you wish to retrieve. This request will return a machine-readable success indicator, and hopefully, the data as well as it's time of creation (UNIX timestamp) and time of retrieval.

**Important: When a yeet is successfuly retrieved, it will be deleted from the database. Options to not perform in this way are in the TO-DO.**

## Deployment

When deploying a yeet sever on a live system, make sure to point all requests to the domain directly to the running server, as Flask will differentiate between the endpoints just fine.

## Contributing

Contributions are most welcome. To contribute, fork this repo and make your edits then commit and make a pull request.

## Authors

* **Liam Scaife** - *Everything so far* - [Website](https://liamsc.com) - [Git]("https://git.liamsc.com/liam")

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
