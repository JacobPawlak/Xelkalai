#!/usr/bin/perl
print "Content-type: text/html\n\n";

my @names = split (/&/, $ENV{QUERY_STRING});

foreach my $i (@names) {
	my($fieldname, $data) = split(/=/, $i);
	print "$fieldname = $data<br>\n";
}
