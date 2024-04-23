
library(tidyverse)
library(tidyterra)
library(terra)
library(patchwork)
library(Utilities.Package)


BiCOME_Gaf <- "Output/Pred/Gafanha_Low_BiCOME_reframed_pred.tif" %>% 
    rast()

values(BiCOME_Gaf)[values(BiCOME_Gaf) == 0] = NA
BiCOME_Gaf <- as.factor(BiCOME_Gaf)
NAflag(BiCOME_Gaf) <- 32767
names(BiCOME_Gaf) <- "layer"

InvaSea_Gaf <- "Output/Pred/Gafanha_Low_invasea_V3_reframed_pred.tif" %>%
    rast()
values(InvaSea_Gaf)[values(InvaSea_Gaf) == 0] = NA
values(InvaSea_Gaf)[values(InvaSea_Gaf) > 8] = NA
InvaSea_Gaf <- as.factor(InvaSea_Gaf)
NAflag(InvaSea_Gaf) <- 32767
names(InvaSea_Gaf) <- "layer"

BiCOME_Belon <- "Output/Pred/Belon_1004_MS_BiCOME_reframed_pred.tif" %>%
    rast()
values(BiCOME_Belon)[values(BiCOME_Belon) == 0] = NA
BiCOME_Belon <- as.factor(BiCOME_Belon)
NAflag(BiCOME_Belon) <- 32767
names(BiCOME_Belon) <- "layer"

InvaSea_Belon <- "Output/Pred/Belon_1004_MS_invasea_V3_reframed_pred.tif" %>%
    rast()
values(InvaSea_Belon)[values(InvaSea_Belon) == 0] = NA
values(InvaSea_Belon)[values(InvaSea_Belon) > 8] = NA
InvaSea_Belon <- as.factor(InvaSea_Belon)
NAflag(InvaSea_Belon) <- 32767
names(InvaSea_Belon) <- "layer"

############## 
plot_Gaf_BiCOME <- ggplot()+
    tidyterra::geom_spatraster(data = BiCOME_Gaf, 
                               mapping = aes(fill = layer),
                               maxcell = 500832*8)+
    coord_sf(crs = 4326)+
    scale_fill_manual(breaks = c(1,2,3,4,5,6,7,8),
                    values=c("#DAA520", "#b3ff1a", "#389318","#873e23","#b3002d", "#70543e","white","#42c9bc"),
                    na.value = NA,
                    name = "",
                    labels = c("Bacillariophyceae",
                               "Chlorophyceae",
                               "Magnoliopsida",
                               "Phaeophyceae",
                               "Rhodophyceae",
                               "Sediment",
                               "SunGlint",
                               "Water"))+
    ggtitle("BiCOME's model")+
    theme_Bede_Map()+
    theme(plot.title = element_text(size = 20, face = "bold"))

plot_Gaf_InvaSea <- ggplot()+
    tidyterra::geom_spatraster(data = InvaSea_Gaf, 
                               mapping = aes(fill = layer),
                               maxcell = 500832*8)+
    coord_sf(crs = 4326)+
    scale_fill_manual(breaks = c(1,2,3,4,5,6,7,8),
                    values=c("#DAA520", "#b3ff1a", "#389318","#873e23","#b3002d", "#70543e","white","#42c9bc"),
                    na.value = NA,
                    name = "",
                    labels = c("Bacillariophyceae",
                               "Chlorophyceae",
                               "Magnoliopsida",
                               "Phaeophyceae",
                               "Rhodophyceae",
                               "Sediment",
                               "SunGlint",
                               "Water"))+
    theme_Bede_Map()+
    ggtitle("InvaSea's Model")+
    theme(plot.title = element_text(size = 20, face = "bold"))

plots_Gaf <- plot_Gaf_BiCOME + plot_Gaf_InvaSea +
  plot_layout(guides = 'collect')

########################

plot_Belon_BiCOME <- ggplot()+
    tidyterra::geom_spatraster(data = BiCOME_Belon, 
                               mapping = aes(fill = layer),
                               maxcell = 500832*8)+
    coord_sf(crs = 4326)+
    scale_fill_manual(breaks = c(1,2,3,4,5,6,7,8),
                    values=c("#DAA520", "#b3ff1a", "#389318","#873e23","#b3002d", "#70543e","white","#42c9bc"),
                    na.value = NA,
                    name = "",
                    labels = c("Bacillariophyceae",
                               "Chlorophyceae",
                               "Magnoliopsida",
                               "Phaeophyceae",
                               "Rhodophyceae",
                               "Sediment",
                               "SunGlint",
                               "Water"))+
    ggtitle("BiCOME's model")+
    theme_Bede_Map()+
    theme(plot.title = element_text(size = 20, face = "bold"))

plot_Belon_InvaSea <- ggplot()+
    tidyterra::geom_spatraster(data = InvaSea_Belon, 
                               mapping = aes(fill = layer),
                               maxcell = 500832*8)+
    coord_sf(crs = 4326)+
    scale_fill_manual(breaks = c(1,2,3,4,5,6,7,8),
                    values=c("#DAA520", "#b3ff1a", "#389318","#873e23","#b3002d", "#70543e","white","#42c9bc"),
                    na.value = NA,
                    name = "",
                    labels = c("Bacillariophyceae",
                               "Chlorophyceae",
                               "Magnoliopsida",
                               "Phaeophyceae",
                               "Rhodophyceae",
                               "Sediment",
                               "SunGlint",
                               "Water"))+
    theme_Bede_Map()+
    ggtitle("InvaSea's Model")+
    theme(plot.title = element_text(size = 20, face = "bold"))

plots_Belon <- plot_Belon_BiCOME + plot_Belon_InvaSea +
  plot_layout(guides = 'collect')




ggsave("Output/Plots/Belon_BiCOME_InvaseaV3.png",plots_Belon, dpi = 300)
ggsave("Output/Plots/Gafanha_BiCOME_InvaseaV3.png",plots_Gaf, dpi = 300)





