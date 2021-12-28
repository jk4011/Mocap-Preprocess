#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

::rpa::Robotic Process Automation

; tip : return 이 꼭 있어야 함.

shift_ctrl_f7() {
  

  Run C:\Users\unist\Documents\Macro_Recorder\2222.mrf
  Send, ^{F5}

  Sleep, 1000

  Run C:\Users\unist\Documents\Macro_Recorder\whole_file_cubic_fill_all.mrf
  a = 0
  While a < 5
  {
    Send, ^{F5}
    Sleep, 7000
    a += 1
  }
  Run C:\Users\unist\Documents\Macro_Recorder\3333.mrf
  Send, ^{F5}

  Sleep, 1000

  Run C:\Users\unist\Documents\Macro_Recorder\whole_file_cubic_fill_all.mrf
  a = 0
  While a < 5
  {
    Send, ^{F5}
    Sleep, 7000
    a += 1
  }
  Run C:\Users\unist\Documents\Macro_Recorder\4444.mrf
  Send, ^{F5}

  Sleep, 1000

  Run C:\Users\unist\Documents\Macro_Recorder\whole_file_cubic_fill_all.mrf
  a = 0
  While a < 5
  {
    Send, ^{F5}
    Sleep, 7000
    a += 1
  }
  Run C:\Users\unist\Documents\Macro_Recorder\5555.mrf
  Send, ^{F5}

  Sleep, 1000

  Run C:\Users\unist\Documents\Macro_Recorder\whole_file_cubic_fill_all.mrf
  a = 0
  While a < 5
  {
    Send, ^{F5}
    Sleep, 7000
    a += 1
  }
  Run C:\Users\unist\Documents\Macro_Recorder\6666.mrf
  Send, ^{F5}

  Sleep, 1000

  Run C:\Users\unist\Documents\Macro_Recorder\whole_file_cubic_fill_all.mrf
  a = 0
  While a < 5
  {
    Send, ^{F5}
    Sleep, 7000
    a += 1
  }
}

^+F7::
shift_ctrl_f7()

Esc::Reload

^F7::
Run C:\Users\unist\Documents\Macro_Recorder\whole_file_cubic_fill_all.mrf
a = 0
While a < 200
{
  Send, ^{F5}
  Sleep, 4000
  a += 1
}


return

^F1::
a = 0
While a < 200
{
  Run C:\Users\unist\Documents\Macro_Recorder\down.mrf
  Sleep, 100
  Send, ^{F5}
  Sleep, 700
  a += 1
}
return

F1::

Run C:\Users\unist\Documents\Macro_Recorder\star.mrf
Sleep, 100
Send, ^{F5}
return

; --macro--
F12::
Run C:\Users\unist\Documents\Macro_Recorder\cubic_fill_all.mrf
Sleep, 100
Send, ^{F5}
return

F11::
Run C:\Users\unist\Documents\Macro_Recorder\cubic_fill_selection.mrf
Sleep, 100
Send, ^{F5}
return


^F12::
Run C:\Users\unist\Documents\Macro_Recorder\pattern_fill_all.mrf
Sleep, 100
Send, ^{F5}
return

^F11::
Run C:\Users\unist\Documents\Macro_Recorder\pattern_fill_selection.mrf
Sleep, 100
Send, ^{F5}
return
