set SUB_DIRECTORIES=austin_kernel boot_loader common/inc debug_unlock drivers mars nvstorage second_boot_loader tbase_sdk tbase-300-r2 zp_ccp mcm_test_harness
c:\cygwin64\bin\find.exe %SUB_DIRECTORIES% -iname "*.[chSs]" -print > cscope.files
c:\cygwin64\bin\find.exe %SUB_DIRECTORIES% -iname "*.inc" -print >> cscope.files
c:\cygwin64\bin\cscope.exe -b -q -k
