(module
  (type (;0;) (func (param i32)))
  (type (;1;) (func (param i32 i32 i32) (result i32)))
  (type (;2;) (func (result f64)))
  (type (;3;) (func (result i64)))
  (type (;4;) (func (param i32 i32) (result i32)))
  (type (;5;) (func (result i32)))
  (type (;6;) (func (param i32) (result i32)))
  (type (;7;) (func))
  (import "a" "a" (func (;0;) (type 1)))
  (import "a" "b" (func (;1;) (type 2)))
  (func (;2;) (type 3) (result i64)
    call 1
    f64.const 0x1.f4p+9 (;=1000;)
    f64.div
    i64.trunc_sat_f64_s)
  (func (;3;) (type 4) (param i32 i32) (result i32)
    (local i32 i32 i32)
    global.get 0
    i32.const 16
    i32.sub
    local.tee 2
    global.set 0
    block  ;; label = @1
      block  ;; label = @2
        local.get 0
        i32.const 1
        i32.eq
        if  ;; label = @3
          i32.const 1227
          local.set 3
          i32.const 1227
          i32.load8_u
          local.set 0
          block  ;; label = @4
            local.get 1
            i32.load
            local.tee 4
            i32.load8_u
            local.tee 1
            i32.eqz
            br_if 0 (;@4;)
            local.get 0
            local.get 1
            i32.ne
            br_if 0 (;@4;)
            loop  ;; label = @5
              local.get 3
              i32.load8_u offset=1
              local.set 0
              local.get 4
              i32.load8_u offset=1
              local.tee 1
              i32.eqz
              br_if 1 (;@4;)
              local.get 3
              i32.const 1
              i32.add
              local.set 3
              local.get 4
              i32.const 1
              i32.add
              local.set 4
              local.get 0
              local.get 1
              i32.eq
              br_if 0 (;@5;)
            end
          end
          local.get 0
          local.get 1
          i32.eq
          br_if 1 (;@2;)
        end
        local.get 2
        i32.const 0
        i32.store8 offset=14
        i32.const 4874
        local.get 2
        i32.const 14
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      i32.const 5388
      i32.const 1
      i32.store8
      local.get 2
      i32.const 0
      i32.store8 offset=15
      i32.const 5083
      local.get 2
      i32.const 15
      i32.add
      i32.const 0
      call 0
      drop
    end
    local.get 2
    i32.const 16
    i32.add
    global.set 0
    i32.const 0)
  (func (;4;) (type 0) (param i32)
    (local i32)
    global.get 0
    i32.const 16
    i32.sub
    local.tee 1
    global.set 0
    local.get 0
    i32.const 3
    i32.eq
    if  ;; label = @1
      local.get 1
      i32.const 0
      i32.store8 offset=14
      i32.const 4505
      local.get 1
      i32.const 14
      i32.add
      i32.const 0
      call 0
      drop
    end
    i32.const 5388
    i32.const 1
    i32.store8
    local.get 1
    i32.const 0
    i32.store8 offset=15
    i32.const 5083
    local.get 1
    i32.const 15
    i32.add
    i32.const 0
    call 0
    drop
    local.get 1
    i32.const 16
    i32.add
    global.set 0)
  (func (;5;) (type 0) (param i32)
    (local i32)
    global.get 0
    i32.const 16
    i32.sub
    local.tee 1
    global.set 0
    block  ;; label = @1
      local.get 0
      i32.const 2
      i32.eq
      if  ;; label = @2
        local.get 1
        i32.const 0
        i32.store8 offset=14
        i32.const 4382
        local.get 1
        i32.const 14
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      i32.const 5388
      i32.const 1
      i32.store8
      local.get 1
      i32.const 0
      i32.store8 offset=15
      i32.const 5083
      local.get 1
      i32.const 15
      i32.add
      i32.const 0
      call 0
      drop
    end
    local.get 1
    i32.const 16
    i32.add
    global.set 0)
  (func (;6;) (type 0) (param i32)
    (local i32)
    global.get 0
    i32.const 16
    i32.sub
    local.tee 1
    global.set 0
    block  ;; label = @1
      local.get 0
      i32.const 1
      i32.eq
      if  ;; label = @2
        local.get 1
        i32.const 0
        i32.store8 offset=14
        i32.const 5261
        local.get 1
        i32.const 14
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      i32.const 5388
      i32.const 1
      i32.store8
      local.get 1
      i32.const 0
      i32.store8 offset=15
      i32.const 5083
      local.get 1
      i32.const 15
      i32.add
      i32.const 0
      call 0
      drop
    end
    local.get 1
    i32.const 16
    i32.add
    global.set 0)
  (func (;7;) (type 0) (param i32)
    (local i32)
    global.get 0
    i32.const 80
    i32.sub
    local.tee 1
    global.set 0
    block  ;; label = @1
      block  ;; label = @2
        call 2
        i32.wrap_i64
        i32.const 5384
        i32.load
        i32.sub
        i32.const 2
        i32.lt_s
        br_if 0 (;@2;)
        local.get 1
        local.get 0
        i32.store offset=16
        local.get 1
        i32.const 105
        i32.store16 offset=78 align=1
        i32.const 2655
        local.get 1
        i32.const 78
        i32.add
        local.get 1
        i32.const 16
        i32.add
        call 0
        i32.const 1
        i32.ne
        br_if 0 (;@2;)
        local.get 1
        i32.const 0
        i32.store8 offset=77
        i32.const 3794
        local.get 1
        i32.const 77
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      local.get 1
      i32.const 7367024
      i32.store offset=28 align=1
      local.get 1
      i32.const 43
      i32.store offset=4
      local.get 1
      i32.const 1
      i32.store offset=8
      local.get 1
      i32.const 1223
      i32.load align=1
      i32.store offset=71 align=1
      local.get 1
      i32.const 1216
      i64.load
      i64.store offset=64
      local.get 1
      i32.const 1208
      i64.load
      i64.store offset=56
      local.get 1
      i32.const 1200
      i64.load
      i64.store offset=48
      local.get 1
      i32.const 1192
      i64.load
      i64.store offset=40
      local.get 1
      i32.const 1184
      i64.load
      i64.store offset=32
      local.get 1
      local.get 1
      i32.const 32
      i32.add
      i32.store
      i32.const 3916
      local.get 1
      i32.const 28
      i32.add
      local.get 1
      call 0
      drop
    end
    local.get 1
    i32.const 80
    i32.add
    global.set 0)
  (func (;8;) (type 0) (param i32)
    (local i32 i32 i32)
    global.get 0
    i32.const 144
    i32.sub
    local.tee 1
    global.set 0
    local.get 1
    i32.const 32
    i32.add
    i32.const 1072
    i32.const 97
    memory.copy
    loop  ;; label = @1
      local.get 1
      i32.const 32
      i32.add
      local.get 3
      i32.add
      local.tee 2
      local.get 2
      i32.load8_u
      i32.const 170
      i32.xor
      i32.store8
      local.get 3
      i32.const 96
      i32.eq
      i32.eqz
      if  ;; label = @2
        local.get 2
        local.get 2
        i32.load8_u offset=1
        i32.const 170
        i32.xor
        i32.store8 offset=1
        local.get 2
        local.get 2
        i32.load8_u offset=2
        i32.const 170
        i32.xor
        i32.store8 offset=2
        local.get 2
        local.get 2
        i32.load8_u offset=3
        i32.const 170
        i32.xor
        i32.store8 offset=3
        local.get 3
        i32.const 4
        i32.add
        local.set 3
        br 1 (;@1;)
      end
    end
    local.get 1
    local.get 0
    i32.store
    local.get 1
    i32.const 6910057
    i32.store offset=28 align=1
    local.get 1
    i32.const 97
    i32.store offset=8
    local.get 1
    local.get 1
    i32.const 32
    i32.add
    i32.store offset=4
    block  ;; label = @1
      i32.const 2261
      local.get 1
      i32.const 28
      i32.add
      local.get 1
      call 0
      i32.const 1
      i32.ne
      if  ;; label = @2
        i32.const 5388
        i32.const 1
        i32.store8
        local.get 1
        i32.const 0
        i32.store8 offset=143
        i32.const 5083
        local.get 1
        i32.const 143
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      local.get 1
      i32.const 0
      i32.store8 offset=27
      i32.const 2537
      local.get 1
      i32.const 27
      i32.add
      i32.const 0
      call 0
      drop
    end
    local.get 1
    i32.const 144
    i32.add
    global.set 0)
  (func (;9;) (type 0) (param i32)
    (local i32)
    global.get 0
    i32.const 80
    i32.sub
    local.tee 1
    global.set 0
    local.get 1
    i32.const 6910057
    i32.store offset=28 align=1
    local.get 1
    local.get 0
    i32.store
    local.get 1
    i32.const 43
    i32.store offset=8
    local.get 1
    i32.const 1063
    i32.load align=1
    i32.store offset=71 align=1
    local.get 1
    i32.const 1056
    i64.load
    i64.store offset=64
    local.get 1
    i32.const 1048
    i64.load
    i64.store offset=56
    local.get 1
    i32.const 1040
    i64.load
    i64.store offset=48
    local.get 1
    i32.const 1032
    i64.load
    i64.store offset=40
    local.get 1
    i32.const 1024
    i64.load
    i64.store offset=32
    local.get 1
    local.get 1
    i32.const 32
    i32.add
    i32.store offset=4
    block  ;; label = @1
      i32.const 1862
      local.get 1
      i32.const 28
      i32.add
      local.get 1
      call 0
      i32.const 1
      i32.eq
      if  ;; label = @2
        local.get 1
        i32.const 0
        i32.store8 offset=27
        i32.const 2139
        local.get 1
        i32.const 27
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      i32.const 5388
      i32.const 1
      i32.store8
      local.get 1
      i32.const 0
      i32.store8 offset=79
      i32.const 5083
      local.get 1
      i32.const 79
      i32.add
      i32.const 0
      call 0
      drop
    end
    local.get 1
    i32.const 80
    i32.add
    global.set 0)
  (func (;10;) (type 0) (param i32)
    (local i32)
    global.get 0
    i32.const 16
    i32.sub
    local.tee 1
    global.set 0
    local.get 1
    local.get 0
    i32.store
    local.get 1
    i32.const 105
    i32.store16 offset=13 align=1
    block  ;; label = @1
      i32.const 1242
      local.get 1
      i32.const 13
      i32.add
      local.get 1
      call 0
      i32.const 1
      i32.eq
      if  ;; label = @2
        local.get 1
        i32.const 0
        i32.store8 offset=12
        i32.const 1740
        local.get 1
        i32.const 12
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      i32.const 5388
      i32.const 1
      i32.store8
      local.get 1
      i32.const 0
      i32.store8 offset=15
      i32.const 5083
      local.get 1
      i32.const 15
      i32.add
      i32.const 0
      call 0
      drop
    end
    local.get 1
    i32.const 16
    i32.add
    global.set 0)
  (func (;11;) (type 5) (result i32)
    global.get 0)
  (func (;12;) (type 6) (param i32) (result i32)
    global.get 0
    local.get 0
    i32.sub
    i32.const -16
    i32.and
    local.tee 0
    global.set 0
    local.get 0)
  (func (;13;) (type 0) (param i32)
    local.get 0
    global.set 0)
  (func (;14;) (type 0) (param i32)
    (local i32 i64)
    global.get 0
    i32.const 16
    i32.sub
    local.tee 1
    global.set 0
    call 2
    local.set 2
    local.get 1
    i32.const 0
    i32.store8 offset=15
    i32.const 4976
    local.get 1
    i32.const 15
    i32.add
    i32.const 0
    call 0
    drop
    block  ;; label = @1
      call 2
      i32.wrap_i64
      local.get 2
      i32.wrap_i64
      i32.ne
      if  ;; label = @2
        i32.const 5388
        i32.load8_u
        i32.eqz
        br_if 1 (;@1;)
        local.get 1
        i32.const 0
        i32.store8 offset=14
        i32.const 4990
        local.get 1
        i32.const 14
        i32.add
        i32.const 0
        call 0
        drop
        br 1 (;@1;)
      end
      i32.const 5384
      call 2
      i64.store32
      local.get 0
      call 6
    end
    local.get 1
    i32.const 16
    i32.add
    global.set 0)
  (func (;15;) (type 7))
  (memory (;0;) 258 258)
  (global (;0;) (mut i32) (i32.const 70928))
  (export "c" (memory 0))
  (export "d" (func 15))
  (export "e" (func 14))
  (export "f" (func 10))
  (export "g" (func 9))
  (export "h" (func 8))
  (export "i" (func 7))
  (export "j" (func 5))
  (export "k" (func 4))
  (export "l" (func 3))
  (export "m" (func 13))
  (export "n" (func 12))
  (export "o" (func 11))
  (data (;0;) (i32.const 1025) "asm\01\00\00\00\01\06\01`\01\7f\01\7f\03\02\01\00\07\0a\01\06_oh_no\00\00\0a\09\01\07\00 \00A\03F\0b\00\00\00\00\00\aa\cb\d9\c7\ab\aa\aa\aa\ab,***\aa\ab\ca\ab\d5\ab\d5\a9(***\aa\ab\aa\ae.***\aa\ab\da\aa\aa\af)***\aa\ab\aa\ab\ac+***\aa\aa\ad8***\aa\a8\ac\c7\cf\c7\c5\d8\d3\a8\aa\af\c5\c2\f5\c4\c5\aa\aa\a0'***\aa\ab-***\aa\aa\8a\aa\eb\ad\ec\a1")
  (data (;1;) (i32.const 1185) "asm\01\00\00\00\01\06\01`\01\7f\01\7f\03\02\01\00\07\0e\01\0a_stage_one\00\00\0a\05\01\03\00\00\0b./this.program"))
