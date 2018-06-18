library(tidyverse)
# library(rvest)
library(readxl)
library(janitor)

source("src/carga.R")

colnames(df)[1] <- "Componentes"

inicio <- 2007
lim <- grep("Producto Interno Bruto", df$Componentes)[1] - 2
df <- df[1:lim,]

filtrar <- c(
  "Consumo Privado",
  "Consumo Público",
  "Formación Bruta de Capital Fijo",
  "Variación de Existencias",
  "Exportaciones",
  "Importaciones"
)

df_clean <- df %>%
  remove_empty("rows") %>%
  remove_empty("cols") %>%
  gather(trimestre, val, "E-M":"O-D__10") %>%
  separate(trimestre, c("tri", "año"), "__") %>%
  mutate(
    año = if_else(is.na(año), inicio, as.numeric(año) + inicio),
    val = if_else(
      Componentes == "Importaciones",
      -as.numeric(val),
      as.numeric(val)
    )
  ) %>%
  filter(Componentes %in% filtrar)


df_clean %>%
  group_by(año, tri) %>%
  summarize(totals = sum(val)) %>%
  View()
