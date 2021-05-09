(module
  (import "console" "log" (func $console_log (param i32)))

  (memory $mem 1)
  (export "memory" (memory $mem))

  (start $start)

  (func $start (export "start")
    (call $console_log
      (i32.const 0x30)
    )
  )

  (func $unused0
    (drop (i32.const 0x30)) ;; 41301a
  )

  (func $unused1
    (drop (i32.const 0x31)) ;; 41311a
  )

  (func $unused2
    (drop (i32.const 0x32)) ;; 41312a
  )

  (data (i32.const 0)
    "<marks>"
    "41301a\n"
    "41311a\n"
    "41321a\n"
    "</marks>"
  )
)
