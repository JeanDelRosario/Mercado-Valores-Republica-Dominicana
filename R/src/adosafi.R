options(encoding = "iso-8859-1") #Encoding apropiado para tildes
library(tabulizer) #Se necesita tener ya instalado rJava principalmente
library(dplyr)

location <- "http://adosafi.org/wp/wp-content/uploads/2018/03/Boletin-Febrero-2018.pdf"

out <- extract_tables(location)

for(j in length(out):1){
  if(length(out[[j]])>100){
    break()
  }
}

out[j] %>% View()

table <- out[j] %>% as.data.frame()

row_start <- which(grepl("\\d", table[,3]))[1]

table <- table[row_start:nrow(table),3:ncol(table)]

# table %>% View()
table[table==""] <- NA

#Arreglando la variable Fondo
for (i in 1:nrow(table)){
  if(is.na(table[i,3]) | is.null(table[i,3])){
    if(all(is.na(table[i,]))){
      table <- table[-i,]
    }else if(!is.na(table[i+1,3])  & is.na(table[i+2,3])){
      table[i,3] <- table[i+1,3]
      table[i+2,3] <- table[i+1,3]
    }else{
      print(i)
      print("Se ha encontrado un caso nuevo")
    }
  }
}

#Arreglando la variable fecha
for (i in 1:nrow(table)){
  if(is.na(table[i,1]) | is.null(table[i,1])){
    if(all(is.na(table[i,]))){
      table <- table[-i,]
    }else if(!is.na(table[i+1,1])  & is.na(table[i+2,1])){
      table[i,1] <- table[i+1,1]
      table[i+2,1] <- table[i+1,1]
    }else{
      print(i)
      print("Se ha encontrado un caso nuevo")
    }
  }
}

#Quitando filas con mas de 3 nulos
for (i in 1:nrow(table)){
  if(sum(is.na(table[i,]))>=3){
    table <- table[-i,]
  }
}

#Arreglando columna de montos
table[,5] %<>%
  gsub("DOP","", .) %>%
  gsub("\\$","",.) %>%
  gsub(",","",.) %>%
  as.numeric()

names(table) <- c("PRIMERA_EMISION","FONDO","AFI","MONEDA","MONTO","AUTORIZADO")

#Por ahora se llamara fondo abierto a los que estan antes que el fondo GAM Energia, y todos los que 
#estan despues seran cerrados
t <- which(table$FONDO == "GAM Energía")[1]
table$TIPOFONDO <- c(rep("abierto",t-1),rep("cerrado",nrow(table)-t+1))
