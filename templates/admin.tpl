<?xml version="1.0" ?>
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<!-- For ipad/iphone -->
		<link rel="icon" type="image/png" href="/images/logo-ipad.png">
		<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=0" />
		<meta name="apple-mobile-web-app-capable" content="yes" />
		<meta name="apple-mobile-web-app-status-bar-style" content="black" />
		<link rel="apple-touch-icon" href="/images/logo-ipad.png"/>
		<link href="/css/helpshift.css" rel="stylesheet" type="text/css" />
		<script src="/js/jquery-1.7.1.min.js"></script>
		<script src="/lib/dojo.minified/dojo.min.js" type="text/javascript" djConfig="parseOnLoad:true"></script>
		<script src="/js/helpshift.js" type="text/javascript"></script>
		<title>HelpShift Admin</title>
		<script type="text/javascript">
			window.onload = function(){setTimeout(Helpshift.Admin.get_data,1000);}
			document.ontouchmove = function(e) {
				e.preventDefault();
			}
		</script>
	</head>
	<body id="index">
		<header class="header">
			<center style="padding-top:16px;">
				<img src="/images/logo.png" width="326px" height="83px"/>
			</center>
		</header>
		<div id="mainarea">
			<div id="data">
				<div id="site_data">
					<ul id="site_data_list" style="list-style: none;padding-left: 0px;margin:5px;">
					</ul>
				</div>
				<div id="user_data">
					<ul id="user_data_list" style="list-style: none;padding-left: 0px;margin:5px;">
					</ul>
				</div>
			</div>
		</div>
		<footer class="footer">
			<center>Created by Harshniket Seta for Helpshift as a Pre-Interview Assignment</center>
		</footer>
		<!-- Extra UI structures-->
		<div id="lightbox" style="display:none;"></div>
		<img id="loadingbar" src='/images/loading.gif' style="display:none;"/>
	</body>
</html>