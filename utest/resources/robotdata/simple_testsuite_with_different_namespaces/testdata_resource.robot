Language: English

*** Settings ***
Resource    resources${/}inner_resource.robot

*** Variables ***
@{Resource List}  2  34
${Resource Var}  iadota

*** Keywords ***
My Keyword
    No Operation

Only From Resource
    No Operation

Keyword In Both Resources
    No Operation
