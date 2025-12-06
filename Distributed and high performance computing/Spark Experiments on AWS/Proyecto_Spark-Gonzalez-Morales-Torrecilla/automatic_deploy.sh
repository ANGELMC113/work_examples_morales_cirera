#!/bin/bash

#usage: ./automatic_deployment.sh path_to_aws_key ip1 ip2 .... ipn

keypath=$1
shift

for ip in $@; do
   	ssh -o StrictHostKeyChecking=no -i $keypath ubuntu@$ip 'sudo apt-get update; sudo apt-get install openjdk-8-jre -y; wget https://dlcdn.apache.org/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz;tar xvfz spark-3.5.5-bin-hadoop3.tgz; rm -f spark-3.5.5-bin-hadoop3.tgz; ssh-keygen -t rsa -N "" -f .ssh/id_rsa'
	 scp -i $keypath ubuntu@$ip:./.ssh/id_rsa.pub $ip.txt
done

rm -f authorized

for ip in $@; do
   cat $ip.txt >> authorized
done

for ip in $@; do
   scp -i $keypath authorized ubuntu@$ip:./.ssh
   ssh -i $keypath ubuntu@$ip 'cat .ssh/authorized >> .ssh/authorized_keys;rm -f .ssh/authorized'
   rm -f $ip.txt
done

rm -f authorized


