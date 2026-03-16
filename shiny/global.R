
library(shiny)
library(shinydashboard)
library(shinyWidgets)
library(tidyverse)
library(leaflet)
library(DT)
library(scales)
library(sf)

chemin_proc <- "processed"

sitadel_com  <- readRDS(file.path(chemin_proc, "sitadel_idf_communes.rds"))
sitadel_dept <- readRDS(file.path(chemin_proc, "sitadel_idf_dept.rds"))
sitadel_idf  <- readRDS(file.path(chemin_proc, "sitadel_idf_total.rds"))

dept_labels <- c("75"="Paris","77"="Seine-et-Marne","78"="Yvelines",
                 "91"="Essonne","92"="Hauts-de-Seine",
                 "93"="Seine-Saint-Denis","94"="Val-de-Marne","95"="Val-d Oise")

sitadel_dept <- sitadel_dept |>
  mutate(dept_lib = dept_labels[dept])

palette_type <- c(
  "Tous"         = "#185FA5",
  "Collectif"    = "#A32D2D",
  "Indiv_pur"    = "#EF9F27",
  "Indiv_groupe" = "#1D9E75",
  "Residence"    = "#7F77DD"
)

annees_dispo <- sort(unique(sitadel_idf$annee))
depts_dispo  <- sort(unique(sitadel_dept$dept))

