*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${BASE_URL}       http://127.0.0.1:8000
${EXPENSES_UI}    ${BASE_URL}/expenses/
${BROWSER}        Chrome

*** Test Cases ***

Test Add Expense via DRF UI
    [Tags]        UI
    Open DRF Expense Page
    Fill Content Text Area
    Click POST Button
    Verify New Expense Is Added

*** Keywords ***

Open DRF Expense Page
    Open Browser    ${EXPENSES_UI}    ${BROWSER}
    Page Should Contain    Expense List Create


Fill Content Text Area
    Input Text    xpath=//*[@id="id__content"]   {"user": 1, "title": "New Expense ID", "amount": 50.5, "date": "2024-11-22", "category": "Food"}

Click POST Button
    Click Button    xpath=//button[contains(text(), 'POST')]

Verify New Expense Is Added
    Wait Until Page Contains    New Expense ID
    Close Browser
