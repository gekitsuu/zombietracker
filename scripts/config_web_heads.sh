DBIP=`ifconfig eth1|grep 'inet addr'|awk '{print $2}'|awk -F':' '{print $2}'`
salt 'www*' cmd.run "sed -i -e \"s/%IP%/EliteZombieTracker:impossiblepassword@$DBIP/\" /home/zombietracker/zombietracker/configs/dbcreds.json"
salt 'www*' cmd.run "service apache2 restart"
