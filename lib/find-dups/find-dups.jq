def relpath:
  sub($pwd; ".")
;

  to_entries[]
| (.key | relpath) as $lhs
| { lhs: $lhs }
+ ( .value
  | reduce to_entries[] as $item
    ( {rhs: null, similarity: -infinite }
    ; if $item.value > .similarity
      then {rhs: ($item.key | relpath), similarity: $item.value}
      else .
      end
    )
  )
# as $item
#  (
#    { rhs: null, similarity: -infinite }
#  ; if $item.similarity > .similarity
#    then $item
#    else .
#    end
#  )
#| . + { rhs: .rhs | relpath, lhs: $lhs }
