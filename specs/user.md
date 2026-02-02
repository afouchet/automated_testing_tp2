Scenario: Create a user
  Given nothing
  When user sends username, password and email
  Then his account is created


Scenario: Authentication: get my profile
  Given authenticated user Bob
  When Bob asks his profile
  Then he receives his profile


Scenario: Authentication: unauthenticated get my profile -> error
  Given unauthenticated user
  When user asks his profile
  Then he receives 403 error

