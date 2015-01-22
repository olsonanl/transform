use JSON::XS;
use strict;
use File::Slurp;

my @bad;
print join("\t", "Script type", "External type", "KBase type", "Script name", "Script exists"), "\n";
for my $file (<plugins/configs/*.json>)
{
    my $j;
    eval {
	$j = decode_json(read_file($file));
    };
    if ($@)
    {
	warn "Error reading $file\n";
	push(@bad, $file);
	next;
    }
    my $script = $j->{script_name};
    my $exists = -s "plugins/scripts/$j->{script_type}/$script" ? "yes" : "NO";
    print join("\t", @$j{qw(script_type external_type kbase_type script_name)}, $exists), "\n";
}
print "Unparsable configs\n";
print "$_\n" foreach @bad;
