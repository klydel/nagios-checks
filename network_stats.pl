#!/usr/bin/perl
# Author(s): Clyde Lingenfelter <klydel@gmail.com>
#simple script to grab network interface stats
#use interface as the argument
#example output: 
#OK - collisions=0: multicast=6: rx_bytes=16756639755735: rx_compressed=0: rx_crc_errors=0: rx_dropped=0: rx_errors=0: rx_fifo_errors=0: rx_frame_errors=0: rx_length_errors=0: rx_missed_errors=25731: rx_over_errors=0: rx_packets=39310580998: tx_aborted_errors=0: tx_bytes=20133836511769: tx_carrier_errors=0: tx_compressed=0: tx_dropped=0: tx_errors=0: tx_fifo_errors=0: tx_heartbeat_errors=0: tx_packets=46496395859: tx_window_errors=0: 
use warnings;

my $dev = @ARGV ? shift : 'eth0';
my $dir = "/sys/class/net/$dev/statistics";
my %stats = do {
    opendir +(my $dh), $dir;
    local @_ = readdir $dh;
    closedir $dh;
    map +($_, []), grep !/^\.\.?$/, @_;
};
sub get_iface_stats() {
    @stats = map {
        chomp (my ($stat) = slurp("$dir/$_"));
        my $line = " ", $_, "=", $stat, ";";
    } sort keys %stats;
}

sub slurp {
    local @ARGV = @_;
    local @_ = <>;
    @_;
}
get_iface_stats();
print "OK - "; 
print @stats;
print " | ";
print @stats;

