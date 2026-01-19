#!/usr/bin/perl
use strict;
use warnings;
my @arrsudo;
open(my$fh, "-|", "grep -E 'sudo:.*session opened' /var/log/auth.log 2>/dev/null")
  or exit 1;
while (my $line = <$fh>){
push @arrsudo, $line;
}
close($fh);

print scalar (@arrsudo);
