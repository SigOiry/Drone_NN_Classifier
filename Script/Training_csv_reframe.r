
library(tidyverse)
library(readr)

df <- "Data/Training/DISCOV_BiCOME_Training.csv" %>% 
    read.csv2()

df2 <- df  %>% 
mutate(True_Class = case_when(True_Class == "MPB" ~ "Bacillariophyceae",
                              True_Class == "Magnoliosida" ~ "Magnoliopsida",
                              True_Class == "Rhodphyta" ~ "Rhodophyta",
                              True_Class == "Bare_Sediment" ~ "Sediment", 
                              True_Class == "Deep_Sediment" ~ "Sediment", 
                              True_Class == "Low_SPC" ~ "Magnoliopsida", 
                              True_Class == "Clorophyta" ~ "Chlorophyta", 
                              TRUE ~ True_Class))


utils::write.table(df2, "Data/Training/DISCOV_BiCOME_Training_reframed.csv", sep = ";", quote = FALSE, row.names = FALSE)
