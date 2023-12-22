#!/usr/bin/env expect
# This script will either induce a state lock in terraform and succeed, or fail
# with a state-already-locked error.
if { [ array get ::env DEBUG ] ne "" } {
  exp_internal 1
}

proc on_error { label } {
  upvar expect_out expect_out
  if {
    [ info exists expect_out(buffer) ] &&
    $expect_out(buffer) ne ""
  } {
    puts stderr $expect_out(buffer)
  } else {
  puts stderr "error: $label"
  }
  exit 1
}

log_user 0
spawn terraform console

set timeout 11

expect {
  "\r> " {
    # got prompt; exit un-gracefully
    exit 0
  }
  timeout { on_error timeout }
  eof { on_error eof }
}

exit 123
