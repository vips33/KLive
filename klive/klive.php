
<?php 

function klive_log($str)
{
	//$log_file = fopen("/volume1/web/klive/log.txt", "a");  
	//fwrite($log_file, $str."\r\n");  
	//fclose($log_file);  
}


	$log_txt = date("Y-m-d H:i:s")."|".$_SERVER['REMOTE_ADDR']."|".$_SERVER['QUERY_STRING'];
	klive_log($log_txt);

	$mode = $_GET["mode"];
	$type = $_GET["type"];
	$id = $_GET["id"];

	$php = 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];
	if ($mode == '') {
		$mode = 'm3u';
	}
	if ( $mode == 'm3u') {
		header("Content-Type: text/html; charset=UTF-8");
		$command = escapeshellcmd('python klive.py'.' '.$mode.' '.$php);
		echo shell_exec($command);	
	} else if ($mode == 'url') {
		$command = escapeshellcmd('python klive.py'.' '.$mode.' '.$type.' '.$id);
		$url = shell_exec($command);
		$url = trim($url);
		klive_log($url);
		header('Location: ' . $url);
	} else if ($mode == 'epg') {
		$command = escapeshellcmd('python klive.py'.' '.$mode);
		echo shell_exec($command);
	}

?> 


