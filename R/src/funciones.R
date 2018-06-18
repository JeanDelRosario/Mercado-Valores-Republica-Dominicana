

last_day <- function(date) {
  lubridate::ceiling_date(date, "month") - days(1)
}

