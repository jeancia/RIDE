Language: English

*** Settings ***
Resource    testdata_resource.robot
Resource    ..${/}resources${/}resu.robot

*** Variables ***
@{Test Suite 1 List}  1  2
${Test Suite 1 Var}  robotista

*** Test Cases ***
My Test 
   My Keyword
   None Keyword
   Log   From builtin

*** Keywords ***
My Keyword
   No Operation

None Keyword
   No Operation
