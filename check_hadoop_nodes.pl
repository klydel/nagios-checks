#!/usr/bin/perl
#script to check number of nodes active in hadoop
#use lib '/opt/nagios/perl_lib';
use Nagios::Plugin::Functions;
use strict;
use LWP;

my $numnodes;
my $host=shift;
my $port = shift;
my $ua = LWP::UserAgent->new;
my $request = HTTP::Request->new(GET => "http://$host:$port/jobtracker.jsp");
my $result = $ua->request($request);
#print $result->content;
#<a href="machines.jsp?type=active">100</a> 
$result->content =~ m|type=active">(\d*)</a>|;
$numnodes = $1;
if (( $numnodes < 100 )) 
{
    #print "Shit\n";
    nagios_exit('CRITICAL',": Nodes: $numnodes");
}
else
{
    nagios_exit('OK',": Nodes: $numnodes");
}
