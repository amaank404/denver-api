"""
A Library that will allow you to create simple and fast DataBase.

This library uses flask as the base and then it creates a simple
flask app using the database provided.

Database allow certain good features to be used. It is constucted in a thread
safe manner. Implementation for Database can also be implemented in other
languages and frameworks (but we chose Flask because of its simplicty, I 
was too late into its development when I found out about FastApi)

Example on creating and hosting a database

```python
from denverapi import database as db
import os

if not os.path.exists("hworld.db"):  # If the database does not exist
    db.create_database("HelloWorld", "hworld.db", ["lang", "code"], "lang", {"somemeta": 129})

hworld = db.Database("hworld.db")
hworld.start_db(force_flask=True)
```

and here goes example of using database client

```python
from denverapi import database as db

dbc = db.DatabaseClient("http://localhost:2400/")
id1 = dbc.append(lang="python3", code="print('Hello, World')")
id2 = dbc.append(lang="python2", code="print 'Hello World'")

print(dbc[id1])
```
"""

import json
from typing import Any, Callable, Dict, IO, List, Tuple, Union
import flask
import os
from threading import Lock
import re
import secrets
import requests
from functools import partial
import argparse


WRITABLE_DB = 1
READABLE_DB = 1 << 1
APPENDABLE_DB = 1 << 2
REMOVABLE_DB = 1 << 3


_json_dump: Callable[[Any, IO], None] = partial(json.dump, separators=(",", ":"))


class Database:
    """
    A Database objects provides utilitites to work with databases. You can specify the permissions for the database
    by providing the following arguments:
    
    * `writable`
    * `appendable`
    * `removable`
    * `readable`
    
    `token_length` is the length of generated hex id.

    the app serves a flask app when its method `Database.start_db` is called.

    The following paths are by default available:
    
    * `GET /get_meta`
    * `GET /get_permissions`
    
    The following paths are available when Database is writable:
    
    * `POST /modify`

    The following paths are available when Database is appendable:
    
    * `POST /new`

    The following paths are available when Database is readable (default):
    
    * `POST /get`
    * `POST /get_all`
    * `POST GET /download`
    * `POST /get_col`
    * `POST /get_id`
    * `POST /query`

    The following paths are available when Database is removable:
    
    * `POST /remove`
    """
    def __init__(self, dir: str, writable: bool=False, appendable: bool=False, removable: bool=False, token_length: int = 32, readable: bool = True):
        print("[DATABASE] Reading Meta")
        with open(f"{dir}/meta.json") as file:
            self.db_info = json.load(file)
        self.db_data = []
        self.db_dir = dir
        ref = [x for x in os.listdir(f"{dir}/data") if os.path.isfile(f"{dir}/data/{x}")]
        ref_len = len(ref)
        self.db_data_id = ref
        print(f"\r[{self.db_info['name']}] Reading Database Info 0/{ref_len}", flush=True, end="")
        c = 0
        for file_name in ref:
            with open(f"{dir}/data/{file_name}") as file:
                self.db_data.append(json.load(file))
                c += 1
                print(f"\r[{self.db_info['name']}] Reading Database Info {c}/{ref_len}", flush=True, end="")
        print(f"\n[{self.db_info['name']}] Initialising Flask Web App")
        self.webapp = flask.Flask("db")
        self.webapp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self.write_lock = Lock()
        self.token_length = token_length
        self.flags = 0
        if writable:
            self.flags |= WRITABLE_DB
        if readable:
            self.flags |= READABLE_DB
        if removable:
            self.flags |= REMOVABLE_DB
        if appendable:
            self.flags |= APPENDABLE_DB

        # Error Handler
        self.webapp.errorhandler(404)(self.error_404)

        # Initialising Paths
        if readable:
            self.get = self.webapp.route('/get', methods=["POST"])(self.get)
            self.get_all = self.webapp.route('/get_all', methods=["POST"])(self.get_all)
            self.download = self.webapp.route('/download', methods=["GET", "POST"])(self.download)
            self.get_col = self.webapp.route("/get_col", methods=['POST'])(self.get_col)
            self.get_id = self.webapp.route("/get_id", methods=["POST"])(self.get_id)
            self.query = self.webapp.route("/query", methods=["POST"])(self.query)

        if writable:
            self.modify_value = self.webapp.route("/modify", methods=["POST"])(self.modify_value)

        if appendable:
            self.new = self.webapp.route('/new', methods=['POST'])(self.new)

        if removable:
            self.remove = self.webapp.route("/remove", methods=["POST"])(self.remove)
        
        self.get_meta = self.webapp.route("/get_meta", methods=["GET"])(self.get_meta)
        self.get_permissions = self.webapp.route("/get_permissions", methods=["GET"])(self.get_permissions)

        # Response Modifier
        self.response_modfier = self.webapp.after_request(self.response_modfier)
    
    def get_meta(self):
        return flask.jsonify(self.db_info)

    def get_permissions(self):
        return flask.jsonify(flags=self.flags)

    def get_col(self):
        json_data = flask.request.get_json(force=True)
        col = json_data.get('column', self.db_info['default_column'])
        col_i = self.db_info['columns'].index(col)
        return flask.jsonify(data=[x[col_i] for x in self.db_data])
    
    def get_id(self):
        return flask.jsonify(data=self.db_data_id)
    
    def remove(self):
        json_data = flask.request.get_json(force=True)
        id = json_data.get("id", None)
        with self.write_lock:
            if id not in self.db_data_id:
                return flask.jsonify(errorstr="Key not in data", error_id="key_not_found")
            os.remove(f"{self.db_dir}/data/{id}")
            self.db_data.pop(self.db_data_id.index(id))
            self.db_data_id.remove(id)
        return flask.jsonify({})
    
    def query(self):
        json_data = flask.request.get_json(force=True)
        response_mod = json_data.get("response", {})
        return_value = response_mod.get("return_value", True)
        return_slice = response_mod.get("result_slice", [0, None])
        search = json_data['search']
        search_type = json_data.get("search_type", "equiv")
        if search_type == "regex":
            search_q = re.compile(search)
        columns = json_data.get("columns", [self.db_info['default_column']])
        result = {}
        for col_i in [self.db_info['columns'].index(x) for x in columns]:
            for x, id in zip(self.db_data, self.db_data_id):
                c = x[col_i]
                if search_type == "regex" and isinstance(c, str):
                    if search_q.search(c):
                        result[id] = x
                if search_type == "equiv":
                    if search == c:
                        result[id] = x
                if search_type == "contains_str" and isinstance(c, str):
                    if search in c:
                        result[id] = x
                if search_type == "greater_than" and isinstance(x, (str, int, float, bool)):
                    if search > c:
                        result[id] = c
                if search_type == "lesser_than" and isinstance(x, (str, int, float, bool)):
                    if search < c:
                        result[id] = c
        if not return_value:
            return flask.jsonify(exists = (result != {}))
        else:
            if return_slice == [None, None]:
                return flask.jsonify(exists = (result != {}), data=result)
            elif return_slice[0] is None:
                return flask.jsonify(exists = (result != {}), data={k: v for k, v in (list(result.items())[:return_slice[1]])})
            elif return_slice[1] is None:
                return flask.jsonify(exists = (result != {}), data={k: v for k, v in (list(result.items())[return_slice[0]:])})
            else:
                return flask.jsonify(exists = (result != {}), data={k: v for k, v in (list(result.items())[return_slice[0]:return_slice[1]])})


    def get(self):
        json_data = flask.request.get_json(force=True)
        key = json_data.get('key', None)
        col = json_data.get('column', self.db_info['default_column'])
        key_id = json_data.get('id', None)
        col_i = self.db_info['columns'].index(col)
        if key is not None:
            for x, id in zip(self.db_data, self.db_data_id):
                if key == x[col_i]:
                    return flask.jsonify(data=x, id=id)
        else:
            if key_id not in self.db_data_id:
                return flask.jsonify(errorstr="Key not in data", error_id="key_not_found")
            return flask.jsonify(data=self.db_data[self.db_data_id.index(key_id)], id=key_id)
        return flask.jsonify(errorstr="Database does not contain any such key", error_id="key_not_found")

    
    def get_all(self):
        json_data = flask.request.get_json(force=True)
        key = json_data['key']
        col = json_data.get('column', None)
        res = []
        ids = []
        if col is None:
            col = self.db_info['default_column']
        col_i = self.db_info['columns'].index(col)
        for x, id in zip(self.db_data, self.db_data_id):
            if key == x[col_i]:
                res.append(x)
                ids.append(id)
        return flask.jsonify(data=res, id=ids)

    def download(self):
        return flask.jsonify(data=self.db_data, id=self.db_data_id)
    
    def modify_value(self):
        json_data = flask.request.get_json(force=True)
        key = json_data['id']
        data = json_data['data']
        with self.write_lock:
            if not isinstance(data, list):
                return flask.jsonify(errorstr="Value for 'data' must be a instance of list", error_id="data_type_error")
            if len(data) != len(self.db_info['columns']):
                return flask.jsonify(errorstr="Length for 'data' must be the length of available columns", error_id="data_length_error")
            if key not in self.db_data_id:
                return flask.jsonify(errorstr="Key not in data", error_id="key_not_found")
            self.db_data[self.db_data_id.index(key)] = data
        return flask.jsonify({})
    
    def new(self):
        json_data = flask.request.get_json(force=True)
        data = json_data['data']
        if not isinstance(data, list):
            return flask.jsonify(errorstr="Value for 'data' must be a instance of list", error_id="data_type_error")
        if len(data) != len(self.db_info['columns']):
            return flask.jsonify(errorstr="Length for 'data' must be the length of available columns", error_id="data_length_error")
        with self.write_lock:
            while True:
                d_name = secrets.token_hex(self.token_length)
                if d_name not in self.db_data_id:
                    break
            with open(f"{self.db_dir}/data/{d_name}", "w") as file:
                _json_dump(data, file)
            self.db_data_id.append(d_name)
            self.db_data.append(data)
        return flask.jsonify(id=d_name)

    def error_404(self, err):
        return flask.Response('{"errorstr": "Unable to find requested path", "error_id": "not_found"}', 404, mimetype="application/json")
    
    def start_db(self, force_flask=False, host="127.0.0.1", port=2400):
        """
        Starts the database application. It prefers using gevent over flask's server. Flask server is used
        when gevent library is not installed or `force_flask` is True. `host` is by default localhost (`127.0.0.1`)
        and default port 2400.
        """
        flask_run = partial(self.webapp.run, port=port, host=host)
        try:
            from gevent.pywsgi import WSGIServer
            gevent_run = partial(WSGIServer((host, port), self.webapp).serve_forever)
        except ImportError:
            gevent_run = None
        if gevent_run is None or force_flask:
            flask_run()
        else:
            gevent_run()
    
    def response_modfier(self, r):
        if "Cache-Control" in r.headers:
            del r.headers['Cache-Control']
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers['Cache-Control'] = 'public, max-age=0, no-cache, no-store, must-revalidate'
        return r


class DbPermissions:
    """
    DbPermissions objects are usually returned by a client. They can be used
    to convert raw values into a set of booleans. This class supplies four boolean
    values:

    * `writable` - If the database allows modification of database
    * `readable` - If the database allows reading from it
    * `appendable` - If the database allows adding new entries
    * `removable` - If the database allows removing entries
    """
    def __init__(self, i=0):
        self.writable = bool(i & WRITABLE_DB)
        self.readable = bool(i & READABLE_DB)
        self.appendable = bool(i & APPENDABLE_DB)
        self.removable = bool(i & REMOVABLE_DB)
        self.raw = i
    
    def __repr__(self):
        return f"<DbPermissions{' writable' if self.writable else ''}{' readable' if self.readable else ''}{' appendable' if self.appendable else ''}{' removable' if self.removable else ''}>"

    def __int__(self):
        return self.raw


class DbMeta:
    """
    DbMeta objects are usually returned by a client. They can be used to convert
    response from `GET /get_meta` into a more clean and pythonic class interface.

    ### Attributes
    
    * `columns` - returns a list of column names.
    * `default_column` - returns the default used column that is used by database.
    * `meta` - returns a dictionary that is custom metadata provided by server.
    * `name` - returns the common name for the database. ForEg: `Car Database 2021`
    """
    def __init__(self, m={}):
        self.columns = m.get("columns", [])
        self.default_column = m.get("default_column", "")
        self.meta = m.get("meta", {})
        self.name = m.get("name", "")
    
    def __repr__(self):
        return f"<DbMeta name=\"{self.name}\" default_column=\"{self.default_column}\">"


class DbRow:
    """
    DbRow objects are usually returned by a client but can also be created. Changes to a DbRow
    object does not apply live changes to DataBase.

    `dbcolumns` can be provided if you want to have a dictionary like read and write access.
    
    `id` is also optional and can be provided but does not effect much. Can be left None if manually
    constructing the object.

    `row_data` is the actual data of the row.
    """
    def __init__(self, row_data: List[str] = None, id: Union[str, None] = None, dbcolumns: list = []):
        self.id = id
        if row_data is None:
            row_data = [None for _ in range(len(dbcolumns))]
        self.row_data = row_data
        self.dbcolumns = dbcolumns

    def __repr__(self) -> str:
        return f"<DbRow {repr(self.row_data)}>"
    
    def __setitem__(self, name: Union[str, int], value: Any) -> None:
        self.row_data[self.dbcolumns.index(name) if isinstance(name, str) else name] = value
    
    def __getitem__(self, name: Union[str, int]) -> Any:
        return self.row_data[self.dbcolumns.index(name) if isinstance(name, str) else name]
    
    def __iter__(self):
        return zip(self.dbcolumns, self.row_data)

    def update(self, d: dict):
        for k, v in d.items():
            self[k] = v
    

class DbResponseError(Exception):
    """
    This Exception is raised by DatabaseClient when server raises a exception
    """


class DbKeyNotFound(DbResponseError):
    """
    Raised when key is not found is server
    """


class DbDataTypeError(DbResponseError):
    """
    Raised when the data provided to database is not a list of objects respective to their columns
    """


class DbDataLengthError(DbResponseError):
    """
    Raised when the length of provided data is does not match up to the columns required
    """


class DbNotFound(DbResponseError):
    """
    Raised when incorrect path is used in query or if the path is not available. Used for 404 responses
    """


class DatabaseClient:
    """
    DatabaseClient implements a cleaner and more pythonic interface to Database server
    instead of using API endpoints.
    """
    def __init__(self, address):
        self.addr = address+("/" if not address.endswith("/") else "")
        self.info = DbMeta(requests.get(self.addr+"get_meta").json())
        self.permissions = DbPermissions(requests.get(self.addr+"get_permissions").json()['flags'])
    
    def __setitem__(self, name: str, value: Union[List[str], Dict[str, Any]]) -> None:
        if isinstance(value, list):
            self.modify(name, *value)
        elif isinstance(value, dict):
            self.modify(name, **value)
        elif isinstance(value, DbRow):
            self.modify(name, value)
        else:
            raise TypeError("Value must be a list or dict")
    
    def __delitem__(self, name: str):
        self.remove(name)
    
    def __getitem__(self, name: str):
        return self.get_by_id(name)

    def modify(self, id: str, *data, **kwdata):
        """
        Sends a `POST /modify` request to the server.
        """
        if not self.permissions.writable:
            raise PermissionError("Can not write to this database without write permission")
        if len(data)>0 and len(kwdata)>0:
            raise ValueError("Both Data in positional form and data in keyword form can not be provided together in one call")
        if data != ():
            if isinstance(data[0], DbRow):
                data = data[0].row_data
            if len(data) != len(self.info.columns):
                raise IndexError(f"Length of data is not enough to satisfy all columns, (required: {len(self.info.columns)}, given: {len(data)})")
        else:
            if len(kwdata) != len(self.info.columns):
                raise IndexError(f"Length of kwdata is not enough to satisfy all columns, (required: {len(self.info.columns)}, given: {len(kwdata)})")
            data = []
            for x in self.info.columns:
                if x not in kwdata:
                    raise KeyError(f"Required Column {x} is not provided within kwdata")
                data.append(kwdata[x])
        query = {
            "id": id,
            "data": data
        }
        response = requests.post(self.addr+"modify", json=query).json()
        _check_server_response(response)
    
    def append(self, *data, **kwdata) -> str:
        """
        Sends a `/POST new` request to the server and then returns the id of the newly created value
        """
        if not self.permissions.appendable:
            raise PermissionError("Can not write to this database withour permissions append permission")
        if not self.permissions.writable:
            raise PermissionError("Can not write to this database without write permission")
        if len(data)>0 and len(kwdata)>0:
            raise ValueError("Both Data in positional form and data in keyword form can not be provided together in one call")
        if data != ():
            if isinstance(data[0], DbRow):
                data = data[0].row_data
            if len(data) != len(self.info.columns):
                raise IndexError(f"Length of data is not enough to satisfy all columns, (required: {len(self.info.columns)}, given: {len(data)})")
        else:
            if len(kwdata) != len(self.info.columns):
                raise IndexError(f"Length of kwdata is not enough to satisfy all columns, (required: {len(self.info.columns)}, given: {len(kwdata)})")
            data = []
            for x in self.info.columns:
                if x not in kwdata:
                    raise KeyError(f"Required Column {x} is not provided within kwdata")
                data.append(kwdata[x])
        query = {
            "data": data
        }
        response = requests.post(self.addr+"new", json=query).json()
        _check_server_response(response)
        return response['id']

    def get_by_value(self, value: str, column: Union[None, str] = None, return_all: bool = False) -> Union[DbRow, List[DbRow]]:
        """
        Returns a List of DbRow objects or a single DbRow object after sending `POST /get`
        or `POST /get_all` if `return_all` is True.
        """
        if not self.permissions.readable:
            raise PermissionError("Unreadable Database")
        query = {
            "key": value,
        }
        if column is not None:
            query['column'] = column
        if return_all:
            response = requests.post(self.addr+"get_all", json=query).json()
            _check_server_response(response)
            r = []
            for v, id in zip(response['data'], response['id']):
                r.append(DbRow(v, id, self.info.columns))
            return r
        else:
            response = requests.post(self.addr+"get", json=query).json()
            _check_server_response(response)
            return DbRow(response['data'], response['id'], self.info.columns)

    def get_by_id(self, id: str) -> DbRow:
        """
        Returns a DbRow object after sending `POST /get`
        """
        if not self.permissions.readable:
            raise PermissionError("Unreadable Database")
        query = {
            "id": id
        }
        response = requests.post(self.addr + "get", json=query).json()
        _check_server_response(response)
        return DbRow(response['data'], response['id'], self.info.columns)

    def download(self) -> List[DbRow]:
        """
        Download the complete database and return a list of DbRow objects
        """
        if not self.permissions.readable:
            raise PermissionError("Unreadable Database")
        response = requests.post(self.addr + "download").json()
        _check_server_response(response)
        r = []
        for v, id in zip(response['data'], response['id']):
            r.append(DbRow(v, id, self.info.columns))
        return r
    
    def get_column(self, column: Union[str, None] = None) -> List[Any]:
        """
        Get and return values of a column
        """
        if not self.permissions.readable:
            raise PermissionError("Unreadable Database")
        query = {}
        if column is not None:
            column['column'] = column
        response = requests.post(self.addr + "get_col", json=query).json()
        _check_server_response(response)
        return response['data']
    
    def get_ids(self):
        """
        Get and return all available ids inside the server database
        """
        if not self.permissions.readable:
            raise PermissionError("Unreadable Database")
        response = requests.post(self.addr + "get_id").json()
        _check_server_response(response)
        return response['data']
    
    def remove(self, id: str):
        """
        Remove entry by its `id`
        """
        if not self.permissions.removable:
            raise PermissionError("Database does not allow removal of entries")
        query = {"id": id}
        response = requests.post(self.addr + "remove", json=query).json()
        _check_server_response(response)
    
    def query(self, query: Any, search_type: str = "equiv", columns: Union[List[str], None] = None, return_value: bool = None, result_slice: Tuple[Union[int, None], Union[int, None]] = None):
        """
        Query database to search for query in one of the following `search_type`s:
        
        * `equiv` The server checks for equality
        * `regex` Searches for regex pattern str `query`
        * `contains_str` Checks if values contains the str `query`
        * `greater_than` Applies Greater than operator on values
        * `lesser_than` Applies Lesser than operator on values

        if `return_value` is true it returns the list values found or None if not found
        but if its false then returns a boolean value indicating if the value exists or not

        `columns` indicates a list of columns to search the value in, by default that is a default column

        `result_slice` indicates the amount of results returned it can be one of the following forms:
        
        * None
        * (int, None)
        * (None, int)
        * (None, None)
        * (int, int)
        """
        if not self.permissions.readable:
            raise PermissionError("Unreadable Database")
        query = {
            "response": {},
            "search": query,
            "search_type": search_type
        }
        if columns is not None:
            query['columns'] = columns
        if return_value is not None:
            query['response']['return_value'] = return_value
        if result_slice is not None:
            query['response']['return_value'] = result_slice
        response = requests.post(self.addr+"query", json=query).json()
        _check_server_response(response)
        if return_value:
            return [DbRow(v, k, self.info.columns) for k, v in response['data'].items()]
        else:
            return response['exists']


def _check_server_response(data: dict):
    if "error_id" in data and "errorstr" in data:
        ex_name = "Db"+data['error_id'].replace("_", " ").title().replace(' ', '').strip()
        ex = globals().get(ex_name, DbResponseError)
        raise ex(data['errorstr'])


def create_database(name: str, dir: str, columns: List[str], default_column: str, metadata: dict = {}):
    """
    Create a Database with the provided name with non existing directory `dir`. `columns`
    is the columns in database. `default_column` is used for default search column.
    `metadata` is a dictionary of custom data which is by default a empty dictionary.
    """
    if default_column not in columns:
        raise ValueError(f"{default_column} is not there in {columns}")
    os.mkdir(dir)
    os.mkdir(f"{dir}/data")
    db = {
        "columns": columns,
        "default_column": default_column,
        "meta": metadata,
        "name": name
    }
    with open(f"{dir}/meta.json", "w") as file:
        _json_dump(db, file)


def clear_database(db: Union[str, DatabaseClient]):
    """
    Remove all values from a given database | addr
    """
    dbc = DatabaseClient(db) if isinstance(db, str) else db
    for x in dbc.get_ids():
        del dbc[x]


def cli():
    """
    Command Line interface for database management
    """
    parser = argparse.ArgumentParser("database")
    commands = parser.add_subparsers(title="Commands", dest="command_")
    host = commands.add_parser("host", help="Host a database")
    host.add_argument("db_dir_name", metavar="DATBASE_DIRECTORY", help="Database to load")
    host.add_argument("-H", "--host", help="host name or IPv4 Address to host on", default="localhost")
    host.add_argument("-p", "--port", help="Port to use", default=2400, type=int)
    host.add_argument("--flask", help="Force flask server instead of gevent", action="store_true")
    host.add_argument("-r", help="Permission Readable", action="store_true")
    host.add_argument("-w", help="Permission Writable", action="store_true")
    host.add_argument("-a", help="Permission Appendble", action="store_true")
    host.add_argument("-x", help="Permission Removable", action="store_true")
    host.add_argument("-t", "--token-length", help="Token Length for random generation of id for values", type=int, default=32)
    
    args = parser.parse_args()
    if args.command_ == "host":
        db = Database(args.db_dir_name, args.w, args.a, args.x, args.token_length, args.r)
        db.start_db(args.flask, args.host, args.port)


if __name__ == "__main__":
    cli()
