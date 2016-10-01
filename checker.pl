#!/usr/bin/env perl
#==============================================================================
#
#         FILE: checker.pl
#
#        USAGE: ./checker.pl cmd hostname id flag
#
#  DESCRIPTION: O'Foody service checker
#
#      OPTIONS: ---
# REQUIREMENTS: ---
#         BUGS: ---
#        NOTES: ---
#       AUTHOR: Vladislav A. Retivykh (var), firolunis@riseup.net
# ORGANIZATION: keva
#      VERSION: 0.2
#      CREATED: 05/21/2015 08:44:35 AM
#     REVISION: ---
#==============================================================================

use strict;
use warnings FATAL => 'all';
use utf8;

use LWP::UserAgent;
use Digest::MD5;

my $PORT = 3000;
my $SALT = '$|8iRcTf2o|S';
my %EXIT_CODES = (
    'Need more args'    => 110,
    'Host unreachable'  => 104,
    'Bad answer'        => 103,
    'Flag not found'    => 102,
    'OK'                => 101
);

#===  FUNCTION  ===============================================================
#         NAME: _encode
#      PURPOSE: Encoding strings
#   PARAMETERS: String
#      RETURNS: Encoded string
#  DESCRIPTION: Encode string with salt via MD5
#       THROWS: ---
#     COMMENTS: ---
#     SEE ALSO: ---
#==============================================================================
sub _encode {
    my $string  = shift or return 0;
    my $md5     = Digest::MD5->new;
    $md5->add($string . $SALT);
    return $md5->b64digest;
}

#===  FUNCTION  ===============================================================
#         NAME: _random_string
#      PURPOSE: Generating random strings
#   PARAMETERS: Length
#      RETURNS: Random string
#  DESCRIPTION: Generate random string
#       THROWS: ---
#     COMMENTS: ---
#     SEE ALSO: ---
#==============================================================================
sub _random_string {
    my $length  = shift or return 0;
    my @chars   = ("A".."Z", "a".."z");
    my $string;
    $string .= $chars[rand @chars] for 1..$length;
    return $string
}

#===  FUNCTION  ===============================================================
#         NAME: _check
#      PURPOSE: Checking service
#   PARAMETERS: hostname
#      RETURNS: Exit code
#  DESCRIPTION: Check service
#       THROWS: ---
#     COMMENTS: ---
#     SEE ALSO: ---
#==============================================================================
sub _check {
    my $hostname = shift or return $EXIT_CODES{'Need more args'};
    if (system("ping -c 1 -t 3 $hostname > /dev/null 2>&1")) {
        return $EXIT_CODES{'Host unreachable'};
    }
    my $ua          = LWP::UserAgent->new();
    my $page        = $ua->get("http://$hostname:$PORT");
    my $content     = $page->decoded_content();
    if (0+($content =~ m/Runaway/g)) {
        return $EXIT_CODES{'OK'};
    } else {
        return $EXIT_CODES{'Bad answer'};
    }
}

#===  FUNCTION  ===============================================================
#         NAME: _put
#      PURPOSE: Putting flag
#   PARAMETERS: hostname, id, flag
#      RETURNS: Exit code
#  DESCRIPTION: Put flag
#       THROWS: ---
#     COMMENTS: ---
#     SEE ALSO: ---
#==============================================================================
sub _put {
    my $hostname    = shift or return $EXIT_CODES{'Need more args'};
    my $id          = shift or return $EXIT_CODES{'Need more args'};
    my $flag        = shift or return $EXIT_CODES{'Need more args'};
    my $password    = _encode($id);
    my $address     = _random_string(16);
    my $review      = _random_string(24);
    my $ua          = LWP::UserAgent->new();
    my $page        = $ua->post("http://$hostname:$PORT/users", {
        'name'  => $id,
        'address'   => $address,
        'email'    => $id . '@example.com',
        'password'  => $password,
        'password_confirm' => $password,
    });
    my $content     = $page->decoded_content();

    $page           = $ua->post("htpp://$hostname:$PORT/tracks", {
        'name' => _random_string(16),
        'description' => _random_string(31) . '=',
        ''
    });

    if (0+($content =~ m/User $id was registered/g)) {
        return $EXIT_CODES{'OK'};
    } else {
        return $EXIT_CODES{'Bad answer'};
    }
}

#===  FUNCTION  ===============================================================
#         NAME: _get
#      PURPOSE: Getting flags
#   PARAMETERS: hostname, id, flag
#      RETURNS: Exit code
#  DESCRIPTION: Get flag
#       THROWS: ---
#     COMMENTS: ---
#     SEE ALSO: ---
#==============================================================================
sub _get {
    my $hostname    = shift or return $EXIT_CODES{'Need more args'};
    my $id          = shift or return $EXIT_CODES{'Need more args'};
    my $flag        = shift or return $EXIT_CODES{'Need more args'};
    my $password    = _encode($id);
    my $ua          = LWP::UserAgent->new();
    $ua->cookie_jar({});
    my $page        = $ua->post("http://$hostname:$PORT/login", {
        'username'  => $id,
        'password'  => $password
    });
    my %cookie      = %{($ua->cookie_jar())};
    $page           = $ua->get(
        "http://$hostname:$PORT/profile?username=$id"
    );
    my $content     = $page->decoded_content();
    $content        =~ s/.*<table class="table">[^<]*(.*)[^<]*<\/table.*/$1/s;
    $content        =~ s/[^<\w]*<[^>]+>//g;
    $content        =~ s/\n\s+/\n/g;
    $content        =~ s/^\s*//g;
    $content        =~ s/^([^\n]*\n){3}([^\n]*)\n.*/$2/s;
    if (0+($content =~ m/$flag/g)) {
        return $EXIT_CODES{'OK'};
    } else {
        return $EXIT_CODES{'Flag not found'};
    }
}

#===  FUNCTION  ===============================================================
#         NAME: main
#      PURPOSE: Choosing action
#   PARAMETERS: cmd, hostname, id, flag
#      RETURNS: Exit code
#  DESCRIPTION: Choose action
#       THROWS: ---
#     COMMENTS: ---
#     SEE ALSO: ---
#==============================================================================
sub main {
    my $cmd         = shift or return $EXIT_CODES{'Need more args'};
    my $hostname    = shift or return $EXIT_CODES{'Need more args'};
    my $id;
    my $flag;
    if ($cmd eq 'put' or $cmd eq 'get') {
        $id     = shift or return $EXIT_CODES{'Need more args'};
        $flag   = shift or return $EXIT_CODES{'Need more args'};
    }

    if ($cmd eq 'check') {
        return _check($hostname);
    } elsif ($cmd eq 'put') {
        return _put($hostname, $id, $flag);
    } elsif ($cmd eq 'get') {
        return _get($hostname, $id, $flag);
    } else {
        return $EXIT_CODES{'Need more args'};
    }
}

exit main(@ARGV) unless caller;
