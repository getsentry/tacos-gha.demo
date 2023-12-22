#!/usr/bin/env sed -nruf
1,/^Lock Info:$/ d
/^  /! {
  x
  s/\n//g
  p
  q
}
s/^  /"/
s/: +/": "/
s/$/",/
H
