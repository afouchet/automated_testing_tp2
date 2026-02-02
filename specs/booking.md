Scenario Bob books a movie
  Given User bob, a movie title, a theater ID and a scheduled date
  When Bob books a place at theater ID for this movie at that date
  Then We call theater's booking service
