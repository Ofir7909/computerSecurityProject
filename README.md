# Computer Security Project

## This is the unsecure version

### Commands

#### stored XSS on section 4

Create a new client with the name `<script>alert(1)</script>`

Solution:

```python
Client.objects.create(
                name=escape(form.cleaned_data["name"]),
                email=escape(form.cleaned_data["email"]),
            )
```

#### sqli on section 1

Regitering a new user with this username `hacker', 'hacker@mail.com', true, true) RETURNING \* --` will give it admin privilages

Solution:

```python
user = User.objects.raw(
                        "INSERT INTO website_user (date_joined, is_active, first_name, last_name, password, username, email, is_staff, is_superuser) VALUES (datetime('NOW'), true, '', '', %s, %s, %s, false, false) RETURNING *",
                        [hashed_password, form.data["username"], form.data["email"]],
                    )[0]
```

#### sqli on section 3

Trying to login in with the username `a'or 1=1--` and a random password, will log us in as the first user in the database, which in our case is admin

Solution:

```python
user = User.objects.raw(
    "SELECT * from website_user where username=%s and password=%s",
    [form.data["username"], hashed_password],
)
```

#### sqli on section 4

All the following queries are on the filter field

To get list of tables and columns in each one:
`fsda' UNION SELECT tbl_name,sql,3,4 FROM sqlite_schema WHERE type='table'--`

To get the users database:
`fsda' UNION SELECT username,password,is_superuser,4 FROM website_user --`

Solution:

```python
@login_required(login_url="/login")
def system(request):
    filter_query = request.GET.get("filter", "").strip()
    like_filter_query = f"%{filter_query}%"

    if filter_query:
        clients = Client.objects.raw(
            "SELECT * from website_client WHERE id LIKE %s OR NAME LIKE %s",
            [like_filter_query, like_filter_query],
        )
    else:
        clients = Client.objects.all()

    return render(request, "system.html", {"clients": clients})
```
