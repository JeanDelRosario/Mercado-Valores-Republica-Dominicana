library(tidyverse)
# library(rvest)
library(readxl)

desc <-
  "https://www.bancentral.gov.do/estadisticas_economicas/sector_real/pib_gasto_2007.xls?s=1527605339138"

p1f <- tempfile()
download.file(desc, p1f, mode = "wb")

df <- read_excel(p1f, sheet = 1, skip = 7)
